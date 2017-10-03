from .base import Scraper
import re
import datetime
from apps.stats.models import Injury, Player
from django.core.exceptions import MultipleObjectsReturned


class InjuriesScraper(Scraper):
    url = 'http://www.physioroom.com/news/english_premier_league/epl_injury_table.php'

    def scrape(self):
        root = self.get_root_tree()
        if root and len(root):
            united_row = root.xpath('//a[contains(text(), "Manchester United")]')[1].getparent().getparent().getparent()
            urtc = united_row.text_content().strip()
            # no_of_injuries = int(re.match(r'Manchester United\s* \((.*)\)', urtc, re.M | re.I).group(1))
            no_of_injuries = int(re.search(r'Manchester United\s* \((.*)\)', urtc, re.M | re.I).group(1))
            # Added +1 to leave row containing player, condition... header
            injury_rows = united_row.xpath('./following-sibling::tr')[1:no_of_injuries + 1]
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
                    except Player.DoesNotExist:
                        raise ValueError('Player "%s" does\'nt exist.' % player_name_last)
                self.data[player] = {'type': row.getchildren()[1].text_content()}
                if row.getchildren()[2].text:
                    self.data[player]['remarks'] = row.getchildren()[2].text
                return_date_raw = row.getchildren()[3].text
                if return_date_raw.lower() == 'no return date':
                    pass
                elif len(return_date_raw.split()) == 3:
                    day = return_date_raw.split()[1].strip(',').zfill(2)
                    month = return_date_raw.split()[0]
                    year = return_date_raw.split()[2]
                    self.data[player]['return_date'] = datetime.datetime.strptime(day + '-' + month + '-' + year, '%d-%B-%Y')
                elif len(return_date_raw.split()) == 2:
                    day = '15'
                    month = return_date_raw.split()[0]
                    year = return_date_raw.split()[1]
                    self.data[player]['return_date'] = datetime.datetime.strptime(day + '-' + month + '-' + year, '%d-%B-%Y')

    def save(self):
        old_injuries = Injury.get_current_injuries()
        new_injuries = []
        for player, data in self.data.items():
            try:
                injury = old_injuries.get(player=player)
            except Injury.DoesNotExist:
                injury = Injury(player=player, injury_date=datetime.datetime.today())

            injury.type = data.get('type', '').strip() or None
            injury.remarks = data.get('remarks', '').strip() or None
            injury.return_date = data.get('return_date')
            new_injuries.append(injury)
        for old_injury in old_injuries:
            if old_injury not in new_injuries:
                yesterday = datetime.datetime.today() - datetime.timedelta(hours=24)
                old_injury.return_date = yesterday
                old_injury.save()
        for new_injury in new_injuries:
            new_injury.save()
