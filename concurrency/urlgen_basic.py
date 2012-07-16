''' This is the basic library. No parallelizing of operations, it just runs thru serially.

    Basic runtime: ~2m20s on my 4 core mac book air
'''

import re
import urllib2
from BeautifulSoup import BeautifulSoup as soup

def find_urls(url):
    page_source = soup(urllib2.urlopen(url).read())
    url = re.sub('(?<=[^/])$', '/', url)
    return [re.sub('^/', url, tag.attrMap['href']) 
            for tag in page_source.findAll('a', {'href': True}) 
            if tag.attrMap['href'] != '']

def fetch(search_text, url):
    try:
        body = urllib2.urlopen(url).read()
    except urllib2.HTTPError as uhe:
        body = ''
    if search_text in body:
        return url


def spider_search_urls(search_text, root):
    return [url for url in find_urls(root) if fetch(search_text, url) != None]




print spider_search_urls("OpenStack", "http://rackspace.com")
