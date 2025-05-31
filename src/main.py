# import sys
import requests
from bs4 import BeautifulSoup

# start_url, target_url = sys.argv[1], sys.argv[2]

# Checks if a link is a valid wikipedia link, returns true or false.
def is_valid_link(url):
    if url is None or ':' in url or not url.startswith('/wiki/'):
        return False
    return True

def format_url(url):
    return 'https://en.wikipedia.org' + url

def deformat_url(url):
    return url.replace('https://en.wikipedia.org', '')

# Gets all links from a page and returns a list of the valid ones. Expects string url and list of urls to exclude.
# Input URLs are formatted without domain name
def get_all_links(url, exclude):

    request = requests.get(format_url(url))
    soup = BeautifulSoup(request.content, 'html.parser')

    links = []
    for href in soup.find_all('a'):
        link = href.get('href')
        # if link in exclude:
            # print("EXCLUDE", link)
        if is_valid_link(link) and link not in exclude and link not in links:
            links.append(link)
            # print("adding", link)
    return links

# Backtracks from target to the source, reading parent urls from the parents_dict, to find the path BFS took
# Returns path as an array
def trace_path(parents_dict, start):
    current = start
    path = []
    while current:
        if current == 'root':  # exit condition; found the top
            return path
        else:  # Haven't found the top yet, keep adding parents
            next = parents_dict[current]
            path.insert(0, current.replace('/wiki/', ''))  # Remove the "/wiki/" from the string
            current = next
    print("error")
    path.insert(0, 'error')
    return path

# BFS algorithm that searches pages in its queue for "adjacent" links (links on the webpage). Excludes already-visited pages.
# It searches starting with the source until it finds the destination and returns the path it took between them.
# URLs are stored in format: /wiki/[TOPIC], full url only used for requests
def BFS(source, destination, depth):
    queue = []
    parents = {}

    queue.append(source)
    parents[source] = 'root'

    while queue:
        current = queue.pop(0)
        print("Searching", current)
        adjacents = get_all_links(current, parents.keys())

        for link in adjacents:
            if link == destination:  # Target found, now we can backtrack the path and return it
                print("found")
                parents[link] = current
                return trace_path(parents, link)  # Return the path
            else:
                queue.append(link)
                parents[link] = current


def main():
    print("Enter a url to start from (full url please): ")
    start_url = input()
    print("Now enter a target url: ")
    target_url = input()
    path = BFS(deformat_url(start_url), deformat_url(target_url), -1)
    print(" -> ".join(path or []))

if __name__ == "__main__":
    main()