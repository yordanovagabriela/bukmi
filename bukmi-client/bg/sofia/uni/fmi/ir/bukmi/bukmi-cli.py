import click
import requests
from termcolor import colored
import json

ADD_API_ENDPOINT = "http://localhost:5000/add"
SEARCH_API_ENDPOINT = "http://localhost:5000/search"
LIST_API_ENDPOINT = "http://localhost:5000/list"

@click.group()
def main():
    pass

@main.command('add')
@click.argument('link')
def add_bookmark(link):
    body = {'url': link}
    response = requests.post(ADD_API_ENDPOINT, json = body)
    click.echo(response.content)

@main.command('search')
@click.option('--tag', '-t', multiple=True)
def search_bookmarks(tag):
    body = {'tags': list(tag)}
    response = requests.get(SEARCH_API_ENDPOINT, json = body)

    bookmarks = json.loads(response.content)
    if len(bookmarks) == 0:
        click.echo("There are no bookmarks matching your request.")
        return
        
    pretty_print(bookmarks)

@main.command('list')
def list_bookmarks():
    response = requests.get(LIST_API_ENDPOINT)

    bookmarks = json.loads(response.content)
    if len(bookmarks) == 0:
        click.echo("There are no bookmarks currently added.")
        return

    pretty_print(bookmarks)

def pretty_print(bookmarks):
    index = 1
    for bookmark in bookmarks:
        message = "{}. {} \n   > {}".format(index, bookmark['title'], bookmark['url'])
        click.echo(message)
        index += 1

if __name__ == '__main__':
    main()