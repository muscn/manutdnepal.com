from django.db import models
import datetime

YEAR_CHOICES = []
for r in range(1890, (datetime.datetime.now().year + 1)):
    YEAR_CHOICES.append((r, r))


# Fixtured
class Competition(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)


class CompetitionYear(models.Model):
    competition = models.ForeignKey(Competition, related_name='seasons')
    year = models.IntegerField('Year', max_length=4, choices=YEAR_CHOICES, default=datetime.datetime.now().year)


# Fixtured
class Country(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)


# Fixtured
class City(models.CharField):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)


# Fixtured
class Stadium(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    city = models.ForeignKey(City, related_name='stadiums')
    capacity = models.PositiveIntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()


# Fixtured
class Team(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=10)
    alternative_names = models.CharField(max_length=255)
    nick_name = models.CharField(max_length=50)
    stadium = models.ForeignKey(Stadium, related_name='teams')
    foundation_date = models.DateField(blank=True, null=True)
    crest = models.ImageField(upload_to='/crests/')

    def get_derby_teams(self):
        # stadium -> city -> stadiums -> teams
        pass

    def get_current_players(self):
        pass

    def get_current_staffs(self):
        pass

    def get_players_by_year(self, year):
        pass

    def get_staffs_by_year(self, year):
        pass


class TeamYear(models.Model):
    team = models.ForeignKey(Team, related_name='seasons')
    year = models.IntegerField('Year', max_length=4, choices=YEAR_CHOICES)
    # color codes, hex probably
    home_color = models.CharField(max_length=10, null=True, blank=True)
    away_color = models.CharField(max_length=10, null=True, blank=True)
    third_color = models.CharField(max_length=10, null=True, blank=True)


class Person(models.Model):
    name = models.CharField(max_length=254)
    slug = models.CharField(max_length=254)
    date_of_birth = models.DateField()
    # fmh
    # favored_person = models.ForeignKey('Person')
    # favored_team = models.ForeignKey(Team)

    class Meta:
        abstract = True


class Player(Person):
    nationality = models.ForeignKey(Country, related_name='players')
    favored_position = models.CharField(max_length=4)

    def get_contract_expiry_date(self):
        pass

    def get_current_team(self):
        pass


class Official(Person):
    nationality = models.ForeignKey(Country, related_name='officials', null=True, blank=True)
    pass


# Doesn't handle cases where a player is also a staff. Re: Giggsy 2013/14 :D
class Staff(Person):
    nationality = models.ForeignKey(Country, related_name='staffs')
    roles = [('Manager', 'manager'), 'Goal Keeping Coach', 'goal_keeping_coach']
    role = models.CharField(max_length=254, choices=roles)

    def get_contract_expiry_date(self):
        pass

    def get_current_team(self):
        pass


class PlayerCareerSession(models.Model):
    player = models.ForeignKey(Player, related_name='career_sessions')
    team = models.ForeignKey(Team, related_name='player_sessions')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    wage = models.FloatField(null=True, blank=True)

    @property
    def session_expired(self):
        # return False if not self.end_date or if self.end_date is in future
        pass


class StaffCareerSession(models.Model):
    staff = models.ForeignKey(Staff, related_name='career_sessions')
    team = models.ForeignKey(Team, related_name='staff_sessions')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    wage = models.FloatField(null=True, blank=True)

    @property
    def session_expired(self):
        # return False if not self.end_date or if self.end_date is in future
        pass


class Match(models.Model):
    start_time = models.DateTimeField()
    home_team = models.ForeignKey(Team, related_name='home_matches')
    away_team = models.ForeignKey(Team, related_name='away_matches')
    competition_year = models.ForeignKey(CompetitionYear, related_name='matches')
    referee = models.ForeignKey(Official, related_name='refereed_matches')
    assistant_referee_1 = models.ForeignKey(Official, related_name='assisted_matches')
    assistant_referee_2 = models.ForeignKey(Official, related_name='assisted_matches2')
    match_referee = models.ForeignKey(Official)


# Match Events

class Goal(models.Model):
    scorer = models.ForeignKey(Player)
    assist_by = models.ForeignKey(Player)
    time = models.PositiveIntegerField()
    match = models.ForeignKey(Match)


# class Card(models.Model):
# player = models.ForeignKey(Player)
#     time = models.PositiveIntegerField()
#     match = models.ForeignKey(Match)
#
#     class Meta:
#         abstract = True


class YellowCard(models.Model):
    player = models.ForeignKey(Player, related_name='yellow_cards')
    time = models.PositiveIntegerField()
    match = models.ForeignKey(Match, related_name='yellow_cards')


class RedCard(models.Model):
    player = models.ForeignKey(Player, related_name='red_cards')
    time = models.PositiveIntegerField()
    match = models.ForeignKey(Match, related_name='red_cards')


class StatSet(models.Model):
    '''
    Holds all the basic stats of a game such as possession, shots on goal
    so on and so forth
    '''

    attempts_on_goal = models.IntegerField()
    shots_on_target = models.IntegerField()
    shots_off_target = models.IntegerField()
    blocked_shots = models.IntegerField()
    corner_kicks = models.IntegerField()
    fouls = models.IntegerField()
    crosses = models.IntegerField()
    offsides = models.IntegerField()
    first_yellows = models.IntegerField()
    second_yellows = models.IntegerField()
    red_cards = models.IntegerField()
    duels_won = models.IntegerField()
    duels_won_percentage = models.IntegerField()
    total_passes = models.IntegerField()
    pass_percentage = models.IntegerField()
    possession = models.DecimalField(decimal_places=2, max_digits=4)
    team = models.ForeignKey(Team)
    match = models.ForeignKey(Match, related_name='stats')

    def __unicode__(self):
        return u'Stats for %s' % self.match