import os
import json

from lxml import html
import requests
import urllib.request


class Scraper(object):
    data = {}
    logs = []
    command = False
    old_logs = []

    def log(self, log):
        self.logs.append(self.__class__.__name__.replace('scraper', '').replace('Scraper', '') + ':: ' + log)
        if self.command:
            print(log)

    def get_url_content(self, url):
        self.log('Retrieving content from: ' + url + ' ...')
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        try:
            response = opener.open(url)
            return response.read()
        except urllib.request.URLError:
            return None

    def get_json_from_url(self, url):
        self.log('Retrieving JSON: ' + url + ' ...')
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        try:
            response = opener.open(url)
            return json.loads(response.read())
        except urllib.request.URLError:
            return None

    def download(self, url=None, path=None):
        url = url or self.url
        path = path or self.local_path
        self.log('Downloading ' + url + ' to ' + path)
        with open(path, 'wb') as handle:
            response = requests.get(url, stream=True)
            # if not response.ok:
            # # Something went wrong
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)

    def download_if_required(self):
        if not os.path.isfile(self.local_path):
            self.download()

    def start(self, *args, **kwargs):
        self.command = kwargs.get('command')
        self.old_logs += self.logs
        self.logs = []
        self.scrape()
        self.log('Scraped!')
        self.save()
        self.log('Saved!')

    def get_root_tree(self, url=None):
        root_url = url or self.url
        self.log('Retrieving root URL: ' + root_url + ' ...')
        cookies = {'tz': '5.75', 'u_country': 'Nepal', 'u_country_code': 'NP', 'u_timezone': 'Asia%2FKatmandu',
                   'u_continent': 'Asia'}
        # try:
        page = requests.get(root_url, cookies=cookies)
        tree = html.fromstring(page.text)
        return tree
        # except requests.ConnectionError:
        #     return None

    def get_wiki_cell_content(self, td):
        if td.getchildren():
            last_child = td.getchildren()[-1]
            if last_child.tag == 'sup':
                try:
                    last_child = td.getchildren()[-2]
                except IndexError:
                    return td.text
            if last_child.getchildren():
                last_child = last_child.getchildren()[-1]
                if last_child.tag == 'sup':
                    last_child = td.getchildren()[-2]
            ret = last_child.text_content()
        else:
            ret = td.text_content()
        if 'n/a' in ret or ret == '':
            return None
        return ret

    def gwcc(self, *args):
        return self.get_wiki_cell_content(*args)

    def get_style(self, el, style_property):
        try:
            all_styles = el.attrib['style']
        except KeyError:
            return None
        styles = all_styles.split(';')
        for style in styles:
            if style:
                css_property, value = style.split(':')
                if css_property == style_property:
                    return value

    def scrape(self):
        raise NotImplementedError('Your scraper class needs to implemented scrape().')

    def save(self):
        raise NotImplementedError('Your scraper class needs to implemented save().')
