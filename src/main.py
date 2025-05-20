import sys
import requests
from bs4 import BeautifulSoup

start_url, target_url = sys.argv[1], sys.argv[2]

# Checks if a link is a valid wikipedia link, returns true or false.
def is_valid_link(url):
    if url is None:
        return False
    if not url.startswith('/wiki/'):
        return False
    return True

def format_url(url):
    return 'https://en.wikipedia.org' + url

def deformat_url(url):
    return url.replace('https://en.wikipedia.org', '')

# Gets all links from a page and returns a list of the valid ones. Expects string url and list of urls to exclude.
def get_all_links(url, exclude):

    request = requests.get(url)
    soup = BeautifulSoup(request.content, 'html.parser')

    links = []
    for href in soup.find_all('a'):
        link = href.get('href')
        # if link in exclude:
            # print("EXCLUDE", link)
        if is_valid_link(link) and link not in exclude:
            links.append(format_url(link))
            # print("adding", link)
    return links


def BFS(source, destination, depth):
    queue = []
    visited = []

    queue.append(source)

    while queue:
        current = queue.pop(0)
        print("Searching", current)
        visited.append(deformat_url(current))
        # print(visited)
        adjacents = get_all_links(current, visited)

        for link in adjacents:
            if link == destination:
                print("found")
                return
            else:
                queue.append(link)

BFS(start_url, target_url, -1)