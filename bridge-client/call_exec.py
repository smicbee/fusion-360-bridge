#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from urllib import request


def main():
    parser = argparse.ArgumentParser(description='Send Python code to Fusion Bridge')
    parser.add_argument('file', help='Python file to execute in Fusion')
    parser.add_argument('--url', default='http://127.0.0.1:8765/exec')
    args = parser.parse_args()

    code = Path(args.file).read_text(encoding='utf-8')
    payload = json.dumps({'code': code}).encode('utf-8')
    req = request.Request(args.url, data=payload, headers={'Content-Type': 'application/json'}, method='POST')

    with request.urlopen(req) as resp:
        print(resp.read().decode('utf-8'))


if __name__ == '__main__':
    main()
