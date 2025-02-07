import os, fnmatch
import requests
import markdownify
import re
from bs4 import BeautifulSoup

def retrieve_markdown(url):
    print("- Downloading content from " + url)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # might need to adapt this when working with other web pages (not Microsoft Learn)
        div = soup.find(id="unit-inner-section")

        for ul in div.find_all("ul", class_="metadata"):
            ul.decompose()
        for d in div.find_all("div", class_="xp-tag"):
            d.decompose()
        for next in div.find_all("div", class_="next-section"):
            next.decompose()
        for header in div.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
            header.string = "\n# " + header.get_text() + "\n"
        for code in div.find_all("code"):
            code.decompose()

        markdown = markdownify.markdownify(str(div), heading_style="ATX", bullets="-")
        markdown = re.sub('\n{3,}', '\n\n', markdown)
        markdown = markdown.replace("[Continue](/en-us/)", "")
        return markdown
