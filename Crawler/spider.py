import requests
import re
from urllib.parse import urljoin

target_url = "http://192.168.189.131/mutillidae/"
target_link = []


def extract_links_from(url):
    response = requests.get(url)
    return re.findall('(?:href=")(.*?)"', response.content.decode(errors="ignore"))


def crawl(url):
    href_links = extract_links_from(url)

    for link in href_links:
        link = urljoin(url, link)

        if "#" in link:
            link = link.split("#")[0]
        if target_url in link and link not in target_link:
            target_link.append(link)
            print(link)
            crawl(link)

crawl(target_url)
