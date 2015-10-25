from .base import Scraper
import re
import datetime
from apps.stats.models import Injury, Player
from django.core.exceptions import MultipleObjectsReturned


class InjuriesScraper(Scraper):
    url = 'http://www.physioroom.com/news/english_premier_league/epl_injury_table.php'

    @classmethod
    def scrape(cls):
        root = cls.get_root_tree()
        united_row = root.xpath('//*[@id="c14"]')[0]
        urtc = united_row.text_content().strip()
        no_of_injuries = int(re.match(r'Manchester United \((.*)\)', urtc, re.M | re.I).group(1))
        injury_rows = united_row.xpath('./following-sibling::tr')[:no_of_injuries]
        for row in injury_rows:
            player_link = row.getchildren()[0].getchildren()[1].attrib['href']
            player_name = player_link.split('/')[-1:][0].split('.')[0].replace('_injury', '').replace('_', ' ').title()
            try:
                player = Player.objects.get(name=player_name)
            except Player.DoesNotExist:
                player_name_short = row.getchildren()[0].text_content()
                player_name_last = player_name_short.split()[-1:][0]
                try:
                    player = Player.objects.get(name__icontains=player_name_last)
                except MultipleObjectsReturned:
                    player_name_first = player_name_short.split()[0]
                    player = Player.objects.get(name__icontains=player_name_last, name__startswith=player_name_first)
            cls.data[player] = {'type': row.getchildren()[1].text_content()}
            if row.getchildren()[2].text:
                cls.data[player]['remarks'] = row.getchildren()[2].text
            return_date_raw = row.getchildren()[3].text
            if return_date_raw == 'no return date':
                pass
            elif len(return_date_raw.split()) == 3:
                day = return_date_raw.split()[0]
                day = re.match(r'^(\d+).*', day, re.M | re.I).group(1).zfill(2)
                month = return_date_raw.split()[1]
                year = return_date_raw.split()[2]
                cls.data[player]['return_date'] = datetime.datetime.strptime(day + '-' + month + '-' + year, '%d-%b-%y')
            elif len(return_date_raw.split()) == 2:
                day = '15'
                month = return_date_raw.split()[0]
                year = return_date_raw.split()[1]
                cls.data[player]['return_date'] = datetime.datetime.strptime(day + '-' + month + '-' + year, '%d-%b-%y')

    @classmethod
    def save(cls):
        old_injuries = Injury.get_current_injuries()
        new_injuries = []
        for player, data in cls.data.iteritems():
            try:
                injury = old_injuries.get(player=player)
            except Injury.DoesNotExist:
                injury = Injury(player=player, injury_date=datetime.datetime.today())

            injury.type = data.get('type')
            injury.remarks = data.get('remarks')
            injury.return_date = data.get('return_date')
            new_injuries.append(injury)
        for old_injury in old_injuries:
            if old_injury not in new_injuries:
                yesterday = datetime.datetime.today() - datetime.timedelta(hours=24)
                old_injury.return_date = yesterday
                old_injury.save()
        for new_injury in new_injuries:
            new_injury.save()
