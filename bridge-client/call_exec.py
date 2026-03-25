#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from urllib import request


def fetch_json(url: str):
    with request.urlopen(url) as resp:
        return json.loads(resp.read().decode('utf-8'))


def post_json(url: str, payload: dict):
    body = json.dumps(payload).encode('utf-8')
    req = request.Request(url, data=body, headers={'Content-Type': 'application/json'}, method='POST')
    with request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))


def main():
    parser = argparse.ArgumentParser(description='Send Python code to Fusion Bridge')
    parser.add_argument('file', nargs='?', help='Python file to execute in Fusion')
    parser.add_argument('--base-url', default='http://127.0.0.1:8765')
    parser.add_argument('--timeout', type=int, default=120)
    parser.add_argument('--state', action='store_true', help='Read /state instead of executing code')
    parser.add_argument('--logs', action='store_true', help='Read /logs instead of executing code')
    args = parser.parse_args()

    if args.state:
        print(json.dumps(fetch_json(f'{args.base_url}/state'), indent=2, ensure_ascii=False))
        return

    if args.logs:
        print(json.dumps(fetch_json(f'{args.base_url}/logs'), indent=2, ensure_ascii=False))
        return

    if not args.file:
        parser.error('file is required unless --state or --logs is used')

    code = Path(args.file).read_text(encoding='utf-8')
    response = post_json(f'{args.base_url}/exec', {
        'code': code,
        'timeoutSeconds': args.timeout,
    })
    print(json.dumps(response, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
