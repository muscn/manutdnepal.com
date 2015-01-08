from lxml import html
import requests


class Scraper(object):
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


class SeasonDataScraper(Scraper):
    url = 'http://en.wikipedia.org/wiki/List_of_Manchester_United_F.C._seasons'

    @classmethod
    def scrape(cls):
        root = cls.get_root_tree()
        table = root.xpath('//h2/span[@id="Seasons"]/..//following-sibling::table')[0]
        rows = table.xpath('tr')[2:]
        dct = {}
        for row in rows:
            columns = row.getchildren()
            if columns:
                year = columns[0].text_content()[0:4]
                if columns[0].xpath('a'):

                    data = {'wiki_url': columns[0].xpath('a')[0].attrib['href']}

                    if cls.gwcc(columns[1]):
                        data['division'] = cls.gwcc(columns[1])
                    if cls.gwcc(columns[2]):
                        data['P'] = cls.gwcc(columns[2])
                    if cls.gwcc(columns[3]):
                        data['W'] = cls.gwcc(columns[3])
                    if cls.gwcc(columns[4]):
                        data['D'] = cls.gwcc(columns[4])
                    if cls.gwcc(columns[5]):
                        data['L'] = cls.gwcc(columns[5])
                    if cls.gwcc(columns[6]):
                        data['F'] = cls.gwcc(columns[6])
                    if cls.gwcc(columns[7]):
                        data['A'] = cls.gwcc(columns[7])
                    if cls.gwcc(columns[8]):
                        data['Pts'] = cls.gwcc(columns[8])
                    if cls.gwcc(columns[9]):
                        data['Pos'] = cls.gwcc(columns[9])
                    if cls.gwcc(columns[10]):
                        data['FA'] = cls.gwcc(columns[10])
                    if cls.gwcc(columns[11]):
                        data['League'] = cls.gwcc(columns[11])
                    if cls.gwcc(columns[12]):
                        data['Community'] = cls.gwcc(columns[12])
                    if cls.gwcc(columns[13]):

                        # test for multiple achievements
                        if columns[13].xpath('*/ul'):
                            achievements = []
                            achievements_li = columns[13].xpath('*/ul')[0].getchildren()
                            for achievement_li in achievements_li:
                                achievements.append(achievement_li.text_content().replace(u'\u2013', '-'))
                        else:
                            data['UEFA'] = [columns[13].getchildren()[1].text_content().replace(u'\u2013', '-')]

                    dct[year] = data

        import ipdb

        ipdb.set_trace()