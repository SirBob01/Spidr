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
        self.explore = [self.get_ip(l) for l in list(start_urls)]
        self.visited = {}

        self.parser = parser

    def get_ip(self, url):
        return url

    def process(self, ip):
        print(ip, len(self.explore))
        response = request.urlopen(ip)
        return response.read().decode()

    def crawl(self):
        while self.explore:
            ip = self.explore.pop()
            self.visited[ip] = True

            try:
                self.parser.feed(self.process(ip))
            except:
                continue

            for child in self.parser.get_children():
                c_ip = self.get_ip(child)
                if c_ip in self.visited:
                    continue
                self.explore.append(c_ip)
