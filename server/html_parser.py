from bs4 import BeautifulSoup
from bs4 import Comment

BLACKLIST = [
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
        if element.parent.name not in BLACKLIST and not isinstance(element, Comment):
            output += '{} '.format(element)

    return {'title': title, 'text': output}