import json
import random
import sys


def randdict(d, size):
    samples = random.sample(d.items(), size)
    result = {k: v for (k, v) in samples}
    return result


def main():
    if len(sys.argv) < 3:
        print('Missing arguments!\n'
              f'Usage: python {sys.argv[0]} <json file> <output size>'
              ' [<output file>]\n'
              'Optional arguments are enclosed with "[]"')
        exit(0)

    with open(sys.argv[1], 'r') as f:
        d = json.load(f)

    size = int(sys.argv[2])
    result = randdict(d, size)

    if len(sys.argv) > 3:
        with open(sys.argv[3], 'w') as o:
            json.dump(result, o, indent=4)
    else:
        print(json.dumps(result, indent=4))


if __name__ == '__main__':
    main()
