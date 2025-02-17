# -*- coding: utf-8 -*-
"""
Auto imports all crawlers from the current package directory.
To be recognized, your crawler file should meet following conditions:
    - file does not starts with an underscore
    - file ends with .py extension
    - file contains a class that extends `lncrawl.utils.crawler.Crawler`
    - the class extending `lncrawl.utils.crawler.Crawler` has a global variable `base_url`
    - `base_url` contains a valid url or a list of urls supported by the crawler

For example, see any of the files inside this directory.
"""

import importlib
import os
import re

from lncrawl.core.crawler import Crawler

rejected_sources = {
    'https://chrysanthemumgarden.com/': 'Removed on request of the owner (Issue #649)',
    'https://novelplanet.com/': 'Site is closed',
    'http://gravitytales.com/': 'Domain is expired',
    'http://fullnovel.live/': "This site can’t be reached",
    'http://moonbunnycafe.com/': "Does not follow uniform format",
    'https://anythingnovel.com/': 'Site broken',
    'https://indomtl.com/': "Does not like to be crawled",
    'https://lnindo.org/': "Does not like to be crawled",
    'https://myoniyonitranslations.com/': "522 - Connection timed out",
    'https://www.jieruihao.cn/': "Unavailable",
    'https://www.noveluniverse.com/': "Site is down",
    'https://www.novelupdates.com/': "Does not host any novels",
    'https://www.novelv.com/': "Site is down",
    'https://www.rebirth.online/': 'Site moved',
    'https://mtled-novels.com/': 'Domain is expired',
    'http://4scanlation.xyz/': 'Site moved',
    'https://pery.info/': 'Site is down',
    'http://writerupdates.com/': 'Site is down',
    'https://www.centinni.com/': 'Site is down',
    'https://fsapk.com/': 'Site is not working',
    'https://bestoflightnovels.com/': 'Site moved',
    'https://novelcrush.com/': 'Site is down',
    'https://888novel.com/': 'Gets IP banned for using crawler',
    'https://novelraw.blogspot.com/': 'Site closed down',
    'https://www.novelspread.com/': 'Site is down',
    'https://www.translateindo.com/': 'Site is down',
    'https://dsrealmtranslations.com/': 'Site is down'
}

# this list will be auto-generated
crawler_list = {}

# auto-import all submodules in the current directory
__sources_dir = os.path.dirname(__file__)
__module_regex = re.compile(r'^([^_.][^.]+).py[c]?$', re.I)
__url_regex = re.compile(r'^^(https?|ftp)://[^\s/$.?#].[^\s]*$', re.I)


def load_crawler_file(file_path, local_module=False):
    global crawler_list

    basename = os.path.basename(file_path)
    regex_result = __module_regex.findall(basename)
    if len(regex_result) != 1:  # does not contains a module
        return
    # end if

    module_name = regex_result[0]
    if local_module:
        module = importlib.import_module('.' + module_name, package=__package__)
    else:
        module = importlib.import_module(module_name, package=__package__)

    for key in dir(module):
        item = getattr(module, key)
        if type(item) != type(Crawler) or item.__base__ != Crawler:
            continue
        # end if

        if not hasattr(item, 'base_url'):
            raise Exception('No `base_url` for `%s`' % key)
        # end if

        base_url = getattr(item, 'base_url')
        if isinstance(base_url, str):
            base_url = [base_url]
        # end if

        if not isinstance(base_url, list):
            raise Exception('Unexpected `base_url` type in `%s`' % key)
        # end if

        for url in base_url:
            if not __url_regex.match(url):
                raise Exception('Invalid `base_url` in `%s`: %s' % (key, url))
            # end if
            if not url.endswith('/'):
                url += '/'
            # end if
            if url in rejected_sources:
                continue
            # end if
            crawler_list[url] = item
        # end for
    # end for
# end def


for entry in os.listdir(__sources_dir):
    file_path = os.path.join(__sources_dir, entry)
    if os.path.isfile(file_path):
        load_crawler_file(file_path, True)
    # end if
# end for
