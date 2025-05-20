import sys
import requests
from bs4 import BeautifulSoup

start_url, target_url = sys.argv[1], sys.argv[2]

def get_all_links(url):

    request = requests.get(url)
    soup = BeautifulSoup(request.content, 'html.parser')

    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    return links

print(get_all_links(start_url))
