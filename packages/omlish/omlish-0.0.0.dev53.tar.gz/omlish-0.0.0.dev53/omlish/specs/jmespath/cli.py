#!/usr/bin/env python3
import argparse
import json
import pprint
import sys

from . import exceptions
from .parser import compile
from .parser import search


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('expression')
    parser.add_argument(
        '-f',
        '--filename',
        help='The filename containing the input data.  If a filename is not given then data is read from stdin.',
    )
    parser.add_argument(
        '--ast',
        action='store_true',
        help='Pretty print the AST, do not search the data.',
    )
    args = parser.parse_args()

    expression = args.expression
    if args.ast:
        # Only print the AST
        expression = compile(args.expression)
        sys.stdout.write(pprint.pformat(expression.parsed))
        sys.stdout.write('\n')
        return 0

    if args.filename:
        with open(args.filename) as f:
            data = json.load(f)
    else:
        data = sys.stdin.read()
        data = json.loads(data)

    try:
        sys.stdout.write(json.dumps(search(expression, data), indent=4, ensure_ascii=False))
        sys.stdout.write('\n')

    except exceptions.ArityError as e:
        sys.stderr.write(f'invalid-arity: {e}\n')
        return 1

    except exceptions.JmespathTypeError as e:
        sys.stderr.write(f'invalid-type: {e}\n')
        return 1

    except exceptions.JmespathValueError as e:
        sys.stderr.write(f'invalid-value: {e}\n')
        return 1

    except exceptions.UnknownFunctionError as e:
        sys.stderr.write(f'unknown-function: {e}\n')
        return 1

    except exceptions.ParseError as e:
        sys.stderr.write(f'syntax-error: {e}\n')
        return 1


if __name__ == '__main__':
    sys.exit(_main())
