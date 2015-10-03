import os
import urllib
import json

from lxml import html
import requests


class Scraper(object):
    data = {}

    @classmethod
    def get_url_content(cls, url):
        return urllib.urlopen(url).read()

    @classmethod
    def get_json_from_url(cls, url):
        return json.loads(urllib.urlopen(url).read())

    @classmethod
    def download(cls, url=None, path=None):
        url = url or cls.url
        path = path or cls.local_path
        print 'Downloading ' + url + ' to ' + path
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
    def start(cls):
        cls.scrape()
        print 'Scraped!'
        cls.save()
        print 'Saved!'

    @classmethod
    def get_root_tree(cls):
        print 'Retrieving root URL: ' + cls.url + ' ...'
        page = requests.get(cls.url)
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
