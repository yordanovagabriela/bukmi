import time

from bs4 import BeautifulSoup
from bs4 import Comment

BLACKLIST_ITEMS = [
    'nav',              
    'cite',
    'noscript',
    'iframe',
    '[document]',
    'noscript',
    'header',
    'html',
    'meta',
    'head', 
    'input',
    'script',
    'style',
    'footer'
]

def parse(html_page):
    soup = BeautifulSoup(html_page, 'html.parser')

    title = soup.title.string
    text = soup.find_all(text=True)

    output = ''

    for element in text:
        blacklisted = False
        if element.parent.name in BLACKLIST_ITEMS or isinstance(element, Comment):
          continue

        # exclude the last three parents (html, document, ...) otherwise everything will be blacklisted 
        for parent in list(element.parents)[:-3]:
          if parent.name in BLACKLIST_ITEMS:
            blacklisted = True
            break
      
        if not blacklisted:
          output += '{} '.format(element)

    return {'title': title, 'text': output}