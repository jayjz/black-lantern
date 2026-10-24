"""Read GGUF metadata or benchmark the authorized loopback server; stdlib only."""
import argparse
import hashlib
import http.client
import json
from pathlib import Path
import struct
import subprocess
import time


def metadata(path):
    """Skip large tokenizer arrays; never load tensor data or execute model content."""
    with path.open('rb') as f:
        def unpack(fmt):
            size = struct.calcsize('<' + fmt)
            data = f.read(size)
            if len(data) != size:
                raise ValueError('truncated GGUF')
            return struct.unpack('<' + fmt, data)[0]

        def string():
            size = unpack('Q')
            if size > 16 * 1024 * 1024:
                raise ValueError('GGUF string exceeds audit bound')
            data = f.read(size)
            if len(data) != size:
                raise ValueError('truncated string')
            return data.decode('utf-8')

        def value(kind, depth=0):
            if depth > 2:
                raise ValueError('nested metadata exceeds audit bound')
            if kind == 8:
                return string()
            if kind == 9:
                subtype, count = unpack('I'), unpack('Q')
                if count > 2_000_000:
                    raise ValueError('metadata array exceeds audit bound')
                for _ in range(count):
                    value(subtype, depth + 1)
                return {'array_type': subtype, 'count': count}
            formats = {0: 'B', 1: 'b', 2: 'H', 3: 'h', 4: 'I', 5: 'i',
                       6: 'f', 7: '?', 10: 'Q', 11: 'q', 12: 'd'}
            return unpack(formats[kind])

        if f.read(4) != b'GGUF':
            raise ValueError('not GGUF')
        version, tensors, count = unpack('I'), unpack('Q'), unpack('Q')
        if version != 3 or count > 10000:
            raise ValueError('unsupported GGUF header')
        fields = {}
        for _ in range(count):
            key = string()
            fields[key] = value(unpack('I'))
    with path.open('rb') as f:
        digest = hashlib.file_digest(f, 'sha256').hexdigest()
    return {'gguf_version': version, 'tensor_count': tensors,
            'bytes': path.stat().st_size, 'sha256': digest, 'metadata': fields}


def gpu():
    result = subprocess.run(['nvidia-smi', '--query-gpu=memory.total,memory.used,memory.free',
                             '--format=csv,noheader,nounits'], capture_output=True,
                            text=True, timeout=10, check=True)
    total, used, free = map(int, result.stdout.splitlines()[0].split(','))
    return dict(total_mib=total, used_mib=used, free_mib=free)


def request(port, method, route, body=None):
    # http.client uses no system proxy and does not follow redirects.
    connection = http.client.HTTPConnection('127.0.0.1', port, timeout=60)
    try:
        connection.request(method, route, None if body is None else json.dumps(body),
                           {'Content-Type': 'application/json'})
        response = connection.getresponse()
        data = response.read(2 * 1024 * 1024 + 1)
        if response.status != 200 or len(data) > 2 * 1024 * 1024:
            raise RuntimeError(f'HTTP status/size rejected: {response.status}')
        return json.loads(data)
    finally:
        connection.close()


def benchmark(port):
    props = request(port, 'GET', '/props')
    if (props['default_generation_settings']['n_ctx'] != 4096
            or props['total_slots'] != 1
            or props['model_alias'] != 'Dolphin3.0-Llama3.1-8B-abliterated.Q4_K_M.gguf'):
        raise RuntimeError('baseline identity/context/slot mismatch')
    samples = []
    # One warmup and three measured identical requests, cache disabled each time.
    # Synthetic text only; no tools, actor I/O, or interpretation of generated text.
    prompt = ('<|im_start|>system\nComplete synthetic text only.<|im_end|>\n'
              '<|im_start|>user\n' + 'The synthetic lantern is blue. ' * 240
              + '\nContinue describing this fictional lantern.<|im_end|>\n<|im_start|>assistant\n')
    for index in range(4):
        before = gpu()
        started = time.monotonic()
        result = request(port, 'POST', '/completion', dict(
            prompt=prompt, n_predict=64, temperature=0, seed=1234,
            cache_prompt=False, stream=False, ignore_eos=True))
        timings = result['timings']
        if timings['prompt_n'] < 1000 or timings['predicted_n'] != 64:
            raise RuntimeError('unexpected token counts')
        samples.append(dict(warmup=index == 0, wall_seconds=time.monotonic() - started,
                            timings=timings, gpu_before=before, gpu_after=gpu()))
    return {'context_capacity': 4096, 'total_slots': 1, 'model_alias': props['model_alias'],
            'build_info': props['build_info'], 'requests': samples,
            'vram_scope': 'whole GPU before/after; not per-process or continuous peak',
            'scope': 'existing server; no loading test or launcher execution'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--metadata', type=Path)
    action.add_argument('--benchmark', action='store_true')
    parser.add_argument('--port', type=int, default=8080, choices=range(1024, 65536))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('choose a fresh output file')
    report = metadata(args.metadata) if args.metadata else benchmark(args.port)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8') as output:
        json.dump(report, output, indent=2)
        output.write('\n')
    print(f'Wrote {args.output}')
