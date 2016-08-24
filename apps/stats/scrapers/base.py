import os
import urllib2
import json

from lxml import html
import requests


class Scraper(object):
    data = {}
    logs = []
    command = False
    old_logs = []

    @classmethod
    def log(cls, log):
        cls.logs.append(cls.__name__.replace('scraper', '').replace('Scraper', '') + ':: ' + log)
        if cls.command:
            print(log)

    @classmethod
    def get_url_content(cls, url):
        cls.log('Retrieving content from: ' + url + ' ...')
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        response = opener.open(url)
        return response.read()

    @classmethod
    def get_json_from_url(cls, url):
        cls.log('Retrieving JSON: ' + url + ' ...')
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        response = opener.open(url)
        return json.loads(response.read())

    @classmethod
    def download(cls, url=None, path=None):
        url = url or cls.url
        path = path or cls.local_path
        cls.log('Downloading ' + url + ' to ' + path)
        with open(path, 'wb') as handle:
            response = requests.get(url, stream=True)
            # if not response.ok:
            # # Something went wrong
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)

    @classmethod
    def download_if_required(cls):
        if not os.path.isfile(cls.local_path):
            cls.download()

    @classmethod
    def start(cls, *args, **kwargs):
        cls.command = kwargs.get('command')
        cls.old_logs += cls.logs
        cls.logs = []
        cls.scrape()
        cls.log('Scraped!')
        cls.save()
        cls.log('Saved!')

    @classmethod
    def get_root_tree(cls, url=None):
        root_url = url or cls.url
        cls.log('Retrieving root URL: ' + root_url + ' ...')
        cookies = {'tz': '5.75', 'u_country': 'Nepal', 'u_country_code': 'NP', 'u_timezone': 'Asia%2FKatmandu'}
        page = requests.get(root_url, cookies=cookies)
        tree = html.fromstring(page.text)
        return tree

    @classmethod
    def get_wiki_cell_content(cls, td):
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

    @classmethod
    def gwcc(cls, *args):
        return cls.get_wiki_cell_content(*args)

    @classmethod
    def get_style(cls, el, style_property):
        try:
            all_styles = el.attrib['style']
        except KeyError:
            return None
        styles = all_styles.split(';')
        for style in styles:
            css_property, value = style.split(':')
            if css_property == style_property:
                return value

    @classmethod
    def scrape(cls):
        raise NotImplementedError('Your scraper class needs to implemented scrape().')

    @classmethod
    def save(cls):
        raise NotImplementedError('Your scraper class needs to implemented save().')
