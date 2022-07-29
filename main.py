from crawler import Crawler
from pprint import pprint
import argparse
import json


def main():

    parser = argparse.ArgumentParser(description='A tjrj crawler. Developed by Guilherme Paixao.')
    parser.add_argument('--timeout', type=float, nargs='?', help='Set timeout for sockets conections.')
    args = parser.parse_args()


    with open('lasts.json') as f:
        lasts = json.load(f)

    crawler = Crawler(lasts, timeout=args.timeout)
    crawler.start() #starts threads for each serv


if __name__ == '__main__':
    main()
