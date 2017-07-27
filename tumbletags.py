"""Scrape tumblr blogs for tags"""
import argparse
import csv
import sys
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def main():
    parser = argparse.ArgumentParser(description='Scrape a Tumblr blog for tags.')
    parser.add_argument('url', metavar='URL', type=str,
                        help='The URL to parse, ex: http://myblog.tumblr.com')
    parser.add_argument('--no-sleep', dest='sleep', action='store_false',
                        help="Disable the 500ms pause before each request")
    parser.set_defaults(sleep=True)
    parser.add_argument('-v', dest='verbose', action='store_true',
                        help="Print information to the console while scraping.")
    parser.set_defaults(verbose=False)
    args = parser.parse_args()

    url = cleanurl(args.url)
    with open(urlparse(url).netloc + '.csv', 'w', encoding='utf-8', newline='\n') as f:
        writer = csv.writer(f)
        writer.writerow(['tags', 'post'])
        url_loop = url + '/archive'

        while True:
            resp = requests.get(url_loop)
            if resp.status_code != 200:
                break
            soup = BeautifulSoup(resp.content, 'lxml')
            nextpage = soup.find('a', {'id': 'next_page_link'})
            if nextpage is None:
                print("Reached end of blog! Closing.")
                sys.exit(0)
            url_loop = url + nextpage['href']
            if args.verbose:
                print('Scraping: {0}'.format(url_loop))

            tags = soup.find_all('span', 'tags')
            for tag in tags:
                tags, post = tag.text.strip(), tag.parent.parent['href']
                if args.verbose:
                    print('Found: "{0}" on post: {1}'.format(tags, post))
                writer.writerow([tags, post])
            f.flush()
            if args.sleep:
                time.sleep(0.5)

def cleanurl(url):
    """Check if URL is missing a protocol, if so, add it"""
    if not url.startswith('https://') and not url.startswith('http://'):
        return "http://" + url
    else:
        return url

if __name__ == '__main__':
    main()
