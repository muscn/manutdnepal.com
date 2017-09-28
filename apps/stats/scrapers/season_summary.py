from .base import Scraper


class SeasonDataScraper(Scraper):
    url = 'https://en.wikipedia.org/wiki/List_of_Manchester_United_F.C._seasons'

    def get_remark_from_bgcolor(self, bgcolor):
        dct = {
            '#DDD': 'Runners-up',
            '#FCC': 'Relegated',
            '#FE2': 'Champions',
            '#DFD': 'Promoted',
        }
        if bgcolor in dct:
            return dct[bgcolor]
        return bgcolor

    def get_remark_from_cell(self, cell):
        return self.get_remark_from_bgcolor(self.get_style(cell, 'background-color'))

    def scrape(self):
        root = self.get_root_tree()
        if root is not None:
            table = root.xpath('//h2/span[@id="Seasons"]/..//following-sibling::table')[0]
            rows = table.xpath('tr')[2:]
            dct = {}
            for row in rows:
                columns = row.getchildren()
                if columns:
                    year = columns[0].text_content()[0:4]
                    if columns[0].xpath('.//a'):
                        data = {'wiki_url': columns[0].xpath('.//a')[0].attrib['href']}
                        if self.gwcc(columns[1]):
                            data['division'] = self.gwcc(columns[1])
                        if self.gwcc(columns[2]):
                            data['P'] = self.gwcc(columns[2])
                        if self.gwcc(columns[3]):
                            data['W'] = self.gwcc(columns[3])
                        if self.gwcc(columns[4]):
                            data['D'] = self.gwcc(columns[4])
                        if self.gwcc(columns[5]):
                            data['L'] = self.gwcc(columns[5])
                        if self.gwcc(columns[6]):
                            data['F'] = self.gwcc(columns[6])
                        if self.gwcc(columns[7]):
                            data['A'] = self.gwcc(columns[7])
                        if self.gwcc(columns[8]):
                            data['Pts'] = self.gwcc(columns[8])
                        if self.gwcc(columns[9]):
                            data['Pos'] = {'value': self.gwcc(columns[9])}
                            if self.get_style(columns[9], 'background-color'):
                                data['Pos']['remarks'] = self.get_remark_from_cell(columns[9])
                        if self.gwcc(columns[10]):
                            data['FA'] = {'value': self.gwcc(columns[10])}
                            if self.get_style(columns[10], 'background-color'):
                                data['FA']['remarks'] = self.get_remark_from_cell(columns[10])
                        if self.gwcc(columns[11]):
                            data['League'] = {'value': self.gwcc(columns[11])}
                            if self.get_style(columns[11], 'background-color'):
                                data['League']['remarks'] = self.get_remark_from_cell(columns[11])
                        if self.gwcc(columns[12]):
                            data['Community'] = self.gwcc(columns[12])
                            data['Community'] = {'value': self.gwcc(columns[12])}
                            if self.get_style(columns[12], 'background-color'):
                                data['Community']['remarks'] = self.get_remark_from_cell(columns[12])
                        if self.gwcc(columns[13]):
                            # test for multiple achievements
                            if columns[13].xpath('*/ul'):
                                achievements = []
                                achievements_li = columns[13].xpath('*/ul')[0].getchildren()
                                for achievement_li in achievements_li:
                                    result = achievement_li.text_content().strip()
                                    result_splitted = result.split(u'\u2013')
                                    achievement = {'cup': result_splitted[0].strip(), 'value': result_splitted[1].strip()}
                                    if achievement_li.getchildren() and achievement_li.getchildren()[0].tag == 'div':
                                        achievement['remarks'] = self.get_remark_from_cell(achievement_li.getchildren()[0])
                                    achievements.append(achievement)
                                data['International'] = achievements
                            else:
                                result = columns[13].getchildren()[1].text_content().strip()
                                result_splitted = result.split(u'\u2013')
                                data['International'] = [
                                    {'cup': result_splitted[0].strip(), 'value': result_splitted[1].strip()}
                                ]
                                if self.get_style(columns[13], 'background-color'):
                                    data['International'][0]['remarks'] = self.get_remark_from_cell(columns[13])

                        if self.gwcc(columns[14]):
                            players = []
                            player_links = columns[14].xpath('.//a')
                            for player_link in player_links:
                                if player_link.getparent().tag == 'sup':
                                    continue
                                players.append({'name': player_link.text_content(), 'wiki_url': player_link.attrib['href']})
                            data['top_scorers'] = players

                        if self.gwcc(columns[15]):
                            data['top_score'] = self.gwcc(columns[15])

                        if 'division' in data and data['division'] == 'Not held':
                            pass
                        else:
                            dct[year] = data

            self.data = dct

    def save(self):
        from apps.stats.models import SeasonData

        for season, data in self.data.items():
            season_data, created = SeasonData.objects.get_or_create(year=season)
            season_data.summary = data
            season_data.save()