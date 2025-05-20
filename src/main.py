import sys
import requests
from bs4 import BeautifulSoup

start_url, target_url = sys.argv[1], sys.argv[2]

def is_valid_link(url):
    print("Checking:", url)
    if url is None:
        return False
    if '/wiki/' not in url:
        return False
    if '#' in url:
        return False
    return True

def get_all_links(url):

    request = requests.get(url)
    soup = BeautifulSoup(request.content, 'html.parser')

    links = []
    for href in soup.find_all('a'):
        link = href.get('href')
        if is_valid_link(link):
            links.append(link)
    return links

print(get_all_links(start_url))

# def BFS(source, destination):
#     queue = []
