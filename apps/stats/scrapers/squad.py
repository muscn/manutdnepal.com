import datetime
from django.core.mail import mail_admins

from .base import Scraper
from apps.stats.models import Player
from muscn.utils.countries import get_a2_from_a3


class SquadScraper(Scraper):
    url = 'http://www.footballsquads.co.uk/eng/2016-2017/faprem/manutd.htm'
    data = []

    @classmethod
    def scrape(cls):
        root = cls.get_root_tree()
        if root is not None:
            table = root.xpath('//table')[0]
            rows = table.xpath('tr')[1:]
            for row in rows:
                dct = {}
                columns = row.getchildren()
                if columns:
                    try:
                        dct['no'] = columns[0].text_content().strip()
                        if dct['no'] == '':
                            dct['no'] = None
                        dct['name'] = columns[1].text_content().strip()
                        dct['country'] = columns[2].text_content().strip()
                        dct['position'] = columns[3].text_content().strip()
                        dct['height'] = columns[4].text_content().strip()
                        dct['weight'] = columns[5].text_content().strip()
                        dct['date_of_birth'] = columns[6].text_content().strip()
                        dct['birth_place'] = columns[7].text_content().strip()
                        dct['previous_club'] = columns[8].text_content().strip()
                        if dct['previous_club'] == 'None':
                            dct['previous_club'] = None
                        if columns[1].getchildren() and columns[1].getchildren()[0].tag == 'i':
                            dct['on_loan'] = True
                        if dct['name'] == 'Name':
                            break
                        if not dct['name'] == '':
                            cls.data.append(dct)
                    except IndexError:
                        pass

    @classmethod
    def save(cls):
        Player.objects.all().update(active=False)
        for datum in cls.data:
            try:
                player = Player.get(datum['name'])
            except Player.DoesNotExist:
                player = Player.objects.create(name=datum['name'])
            player.squad_no = datum['no']
            player.height = datum['height']
            player.weight = datum['weight']
            player.birth_place = datum['birth_place']
            player.previous_club = datum['previous_club']
            player.favored_position = datum['position']
            player.date_of_birth = datetime.datetime.strptime(datum['date_of_birth'], '%d-%m-%y')
            player.nationality = get_a2_from_a3(datum['country'])
            if datum.get('on_loan'):
                player.on_loan = True
            player.active = True
            try:
                player.save()
            except ValueError:
                mail_admins('[MUSCN] Saving player from squad failed', str(datum))