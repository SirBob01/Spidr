from urllib import request
from html.parser import HTMLParser


class Parser(HTMLParser):
    children = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for a in attrs:
                if a[0] == "href":
                    self.children.append(a[1])
    
    def handle_data(self, data):
        pass

    def get_children(self):
        children = self.children
        self.children = []
        return children


class Spider(object):
    def __init__(self, parser, *start_urls):
        self.explore = list(start_urls)
        self.visited = {}

        self.parser = parser

    def request(self, url):
        response = request.urlopen(url)
        return response.read().decode()

    def crawl(self):
        while self.explore:
            url = self.explore.pop(0)
            self.visited[url] = True

            try:
                req = self.request(url)
                self.parser.feed(req)
            except:
                continue

            for child in self.parser.get_children():
                if child in self.visited:
                    continue
                self.explore.append(child)
