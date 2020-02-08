import click
import requests

@click.group()
def main():
    pass

@main.command('add')
@click.argument('link')
def add_bookmark(link):
    click.echo('Adding bookmark ' + link)

@main.command('search')
@click.option('--tags', '-t', multiple=True)
def list_bookmarks(tags):
    click.echo('Searching bookmarks with tags')
    print(tags)

@main.command('list')
def list_bookmarks():
    click.echo('Listing bookmarks')

if __name__ == '__main__':
    main()