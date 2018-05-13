import sys
import json
import random


def main():
    if len(sys.argv) < 3:
        print(('Missing arguments!\n'
               f'Usage: python {sys.argv[0]} <json file> <output size>'))
        exit(0)
    with open(sys.argv[1], 'r') as f:
        length = int(sys.argv[2])
        map = json.load(f)
        samples = random.sample(map.items(), length)
        output = {k: v for (k, v) in samples}
        print(json.dumps(output, indent=4))


if __name__ == '__main__':
    main()
