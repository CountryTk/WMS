
from sys import exit
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request


def main():
    target_url = "https://www.nike.com/t/air-vapormax-2019-premium-shoe-wr4C0z/AT6810-100"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Charset": "image/webp,image/apng,image/*,*/*;q=0.8",
        "Cookie": "YOUR_COOKIE_HERE",
        "Accept-Encoding": "none",
        "Accept-Language": "en-US,en;q=0.8",
        "Connection": "keep-alive"}

    request = Request(target_url, headers=headers)
    response = urlopen(request).read()

    soup = BeautifulSoup(response, "html.parser")
    print(str(soup.findAll("div", {"class": "description-preview"})))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)