#!/usr/bin/env python

import os
import sys
import re
from time import sleep
from urllib.parse import urljoin
import datetime

import requests
from lxml import etree

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def check_response(document_url):
    return requests.get(document_url, timeout=10).status_code

def main(argv):
    urls = {
        'kamervragen': 'https://www.tweedekamer.nl/kamerstukken/kamervragen',
        'brieven_regering': 'https://www.tweedekamer.nl/kamerstukken/brieven_regering'
    }

    for k, url in urls.items():
        html = etree.HTML(requests.get(url, timeout=10).content)
        links = html.xpath('//a[@href]/@href')
        counts = {}
        total_count = 0
        for l in [x for x in links if x.startswith('/kamerstukken/%s/detail?' % (k,))]:
            full_l = urljoin(url, l)
            s = check_response(full_l)
            try:
                counts[s] += 1
            except LookupError as e:
                counts[s] = 1
            if s != 200:
                eprint(full_l)
            total_count += 1
            sleep(1)
        pct_correct = counts[200] / total_count * 100.0
        codes = ','.join(["%s: %s" % (s, counts[s],) for s in sorted(counts.keys())])

        print("%s: %s: %s%% %s" % (datetime.datetime.now().isoformat()[0:19], k, pct_correct, codes,))
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
