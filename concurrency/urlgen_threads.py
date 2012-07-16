''' This is the threading library. This uses real thread pools to parrallize 
    the fetching and sorting.

    Basic runtime: ~23s on my 4 core mac book air
'''

import re
import threading
import urllib2
import math
import Queue
from BeautifulSoup import BeautifulSoup as soup

def find_urls(url):
    page_source = soup(urllib2.urlopen(url).read())
    url = re.sub('(?<=[^/])$', '/', url)
    return [re.sub('^/', url, tag.attrMap['href']) 
            for tag in page_source.findAll('a', {'href': True}) 
            if tag.attrMap['href'] != '']

class url_crawler(threading.Thread):
    def __init__(self, search_text, in_queue, out_queue):
        threading.Thread.__init__(self)
        self.search_text = search_text
        self.in_queue = in_queue
        self.out_queue = out_queue

    def _fetch(self, url):
        try:
            body = urllib2.urlopen(url).read()
        except urllib2.HTTPError as uhe:
            body = ''
        if self.search_text in body:
            return url

    def run(self):
        while self.in_queue.unfinished_tasks > 0:
            urls = self.in_queue.get()
            for url in urls:                
                match_url = self._fetch(url)
                if match_url != None:
                    self.out_queue.put(match_url)
            self.in_queue.task_done()


def spider_search_url_root(search_text, root):
    worker_queue = Queue.Queue()
    return_queue = Queue.Queue()

    # add in the urls list in chunks of 10 entries
    urls = find_urls(root)
    for i in range(int(math.ceil(len(urls)/10.0))):
        worker_queue.put(urls[i*10:i*10+9])

    # spawn 8 threads to process the worker_queue
    for i in range(8):
        uc = url_crawler(search_text, worker_queue, return_queue)
        uc.setDaemon(True)
        uc.start()

    # wait for threads to finish their queue
    worker_queue.join()

    # roll up the results into a list for return
    results = []
    while return_queue.unfinished_tasks > 0:
        entry = return_queue.get()
        results.append(entry)
        return_queue.task_done()
    return results


print spider_search_url_root("OpenStack", "http://rackspace.com")

