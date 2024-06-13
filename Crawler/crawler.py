import requests
import re


def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass


target_url = "zsecurity.org"


def check_subdomain(target_url):
    with open("subdomains-wodlist.txt", "r") as f:
        for line in f:
            word = line.strip()
            test_url = word + "." + target_url
            response = request(test_url)
            if response:
                print("[+] Discovery subdomain --> " + test_url)


def check_hiddenpath(target_url):
    with open("files-and-dirs-wordlist.txt", "r") as wordlist:
        for line in wordlist:
            word = line.strip()
            test_url = target_url + "/" + word
            response = request(test_url)
            if response:
                print("[+] Discovery URL --> " + test_url)


print(request(target_url).content)  # get
