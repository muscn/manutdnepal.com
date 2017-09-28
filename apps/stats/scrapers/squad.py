import datetime
from django.core.mail import mail_admins

from .base import Scraper
from apps.stats.models import Player
from muscn.utils.countries import get_a2_from_a3


class SquadScraper(Scraper):
    url = 'http://www.footballsquads.co.uk/eng/2017-2018/faprem/manutd.htm'
    data = []
    active = True

    def parse_players(self, rows):
        for row in rows:
            dct = {}
            columns = row.getchildren()
            if columns:
                try:
                    if columns[8].text_content().strip() == 'New Club':
                        # players from following rows are no longer in the club
                        self.active = False
                    dct['name'] = columns[1].text_content().strip()
                    if dct['name'] == 'Name' or not dct['name']:
                        continue
                    dct['no'] = columns[0].text_content().strip()
                    if dct['no'] == '':
                        dct['no'] = None
                    dct['country'] = columns[2].text_content().strip()
                    dct['position'] = columns[3].text_content().strip()
                    dct['height'] = columns[4].text_content().strip()
                    dct['weight'] = columns[5].text_content().strip()
                    dct['date_of_birth'] = columns[6].text_content().strip()
                    dct['birth_place'] = columns[7].text_content().strip()
                    if self.active:
                        dct['previous_club'] = columns[8].text_content().strip()
                        if dct['previous_club'] == 'None':
                            dct['previous_club'] = None
                    else:
                        dct['previous_club'] = None
                        new_club = columns[8].text_content().strip()
                        if new_club.endswith('(On Loan)'):
                            dct['on_loan'] = True
                    dct['active'] = self.active
                    self.data.append(dct)
                except IndexError:
                    pass

    def scrape(self):
        root = self.get_root_tree()
        if root is not None:
            active_players_table = root.xpath('//table')[0]
            active_player_rows = active_players_table.xpath('tr')[1:]
            # inactive_players_table = root.xpath('//table')[1]
            # inactive_player_rows = inactive_players_table.xpath('tr')[2:]
            self.parse_players(active_player_rows)
            # self.parse_players(inactive_player_rows, active=False)

    def save(self):
        Player.objects.all().update(active=False)
        for datum in self.data:
            try:
                player = Player.get(datum['name'])
            except Player.DoesNotExist:
                player = Player.objects.create(name=datum['name'])
            player.squad_no = datum['no']
            player.height = datum['height'] or None
            player.weight = datum['weight'] or None
            player.birth_place = datum['birth_place']
            player.previous_club = datum['previous_club']
            player.favored_position = datum['position']
            player.date_of_birth = datetime.datetime.strptime(datum['date_of_birth'], '%d-%m-%y')
            player.nationality = get_a2_from_a3(datum['country'])
            if datum.get('on_loan'):
                player.on_loan = True
            player.active = datum['active']
            try:
                player.save()
            except ValueError:
                mail_admins('[MUSCN] Saving player from squad failed', str(datum))
