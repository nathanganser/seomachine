#!/usr/bin/env python3
"""Sanity-check Nuxt Content MDC files: fence balance, frontmatter, title/description length.

Usage: python3 validate_mdc.py <file.md> [...]   (paths relative to cwd or absolute)
Exit code 1 if any file fails.
"""
import re
import sys

import yaml

OPEN = re.compile(r'^\s*::[a-zA-Z]')
CLOSE = re.compile(r'^\s*::\s*$')


def check(path):
    errs = []
    text = open(path, encoding='utf-8').read()
    lines = text.split('\n')
    # frontmatter
    if not text.startswith('---'):
        errs.append('no frontmatter')
    else:
        end = text.find('\n---', 3)
        try:
            fm = yaml.safe_load(text[3:end]) or {}
            t, d = fm.get('title', ''), fm.get('description', '')
            if not t:
                errs.append('missing title')
            elif len(t) > 60:
                errs.append(f'title {len(t)} chars')
            if not d:
                errs.append('missing description')
            elif len(d) > 160:
                errs.append(f'description {len(d)} chars')
        except yaml.YAMLError as e:
            errs.append(f'frontmatter YAML: {e}')
    # fences: track a stack by indentation
    stack = []
    for i, line in enumerate(lines, 1):
        if OPEN.match(line):
            stack.append((i, len(line) - len(line.lstrip())))
        elif CLOSE.match(line):
            if not stack:
                errs.append(f'stray closer line {i}')
            else:
                stack.pop()
    if stack:
        errs.append('unclosed openers at lines ' + ', '.join(str(s[0]) for s in stack))
    for bad in ('MwSt', 'MWSt', 'ß'):
        n = text.count(bad)
        if n:
            errs.append(f'{bad} x{n}')
    return errs


def main():
    failed = 0
    for p in sys.argv[1:]:
        try:
            e = check(p)
        except FileNotFoundError:
            continue
        if e:
            failed += 1
            print(f'FAIL {p}: ' + '; '.join(e))
    print(f'{len(sys.argv) - 1} files checked, {failed} failed')
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
