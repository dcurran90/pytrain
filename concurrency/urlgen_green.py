''' This is the eventlet library. This uses pseudo-thread pools and and built in
    collection methods in order to parrallize the fetching and sorting.

    Basic runtime: ~23s on my 4 core mac book air
'''


import eventlet
eventlet.monkey_patch()
import re
from eventlet.green import urllib2
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

def spider_search_url_root(search_text, root):
    urls = find_urls(root)
    pile = eventlet.GreenPile()
    for url in find_urls(root):
        pile.spawn(fetch, search_text, url)
    return [p for p in pile if p is not None]


print spider_search_url_root("OpenStack", "http://rackspace.com")

