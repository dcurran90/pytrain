''' This is the multiprocessing library. This uses multiple processes and built
    in collection methods in order to parrallize the fetching and sorting.

    Basic runtime: ~24s on my 4 core mac book air
'''

import re
import multiprocessing
from functools import partial
import urllib2
from BeautifulSoup import BeautifulSoup as soup

def find_urls(url):
    page_source = soup(urllib2.urlopen(url).read())
    url = re.sub('(?<=[^/])$', '/', url)
    return [re.sub('^/', url, tag.attrMap['href']) for tag in page_source.findAll('a', {'href': True}) if tag.attrMap['href'] != '']
    

def fetch(search_text, url):
    try:
        body = urllib2.urlopen(url).read()
    except urllib2.HTTPError as uhe:
        body = ''
    if search_text in body:
        return url


def spider_search_url_root(search_text, root):
    urls = find_urls(root)
    worker_pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() * 4)
    fetch_wrap = partial(fetch, search_text)
    return [result for result in worker_pool.map_async(fetch_wrap, urls).get() if result != None]



print spider_search_url_root("OpenStack", "http://rackspace.com")

