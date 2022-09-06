#!/usr/bin/env python

import os
import sys
import re
from time import sleep
from urllib.parse import urljoin

import requests
from lxml import etree

def check_response(document_url):
    return requests.get(document_url).status_code

def main(argv):
    urls = {
        'kamervragen': 'https://www.tweedekamer.nl/kamerstukken/kamervragen',
        'brieven_regering': 'https://www.tweedekamer.nl/kamerstukken/brieven_regering'
    }

    for k, url in urls.items():
        html = etree.HTML(requests.get(url).content)
        links = html.xpath('//a[@href]/@href')
        counts = {}
        for l in [x for x in links if x.startswith('/kamerstukken/%s/detail?' % (k,))]:
            print(l)
            full_l = urljoin(url, l)
            try:
                counts[check_response(full_l)] += 1
            except LookupError as e:
                counts[check_response(full_l)] = 1
            sleep(1)
        print(counts)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
