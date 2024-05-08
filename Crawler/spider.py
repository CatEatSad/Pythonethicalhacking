import requests
import re
from urllib.parse import urljoin


def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass


target_url = "192.168.189.131/mutillidae/"
target_link = []


def extract_links_from(url):
    try:
        response = request(url)
        return re.findall('(?:href=")(.*)"', response.content.decode())
    except:
        pass


def crawl(target_url):
    href_links = extract_links_from(target_url)
    for link in href_links:
        link = urljoin(target_url, link)

        if "#" in link:
            link = link.split("#")[0]
        if target_url in link and link not in target_link:
            target_link.append(link)
            print(link)


crawl(target_url)
