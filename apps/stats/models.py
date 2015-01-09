from django.db import models
import datetime
from muscn.utils.countries import CountryField
from jsonfield import JSONField

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


# # Fixtured
# class Country(models.Model):
# name = models.CharField(max_length=255)
# slug = models.SlugField(max_length=255)


# Fixtured
class City(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    country = CountryField()

    class Meta:
        verbose_name_plural = 'Cities'


# Fixtured
class Stadium(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    city = models.ForeignKey(City, related_name='stadiums')
    capacity = models.PositiveIntegerField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)


# Fixtured
class Team(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=10)
    alternative_names = models.CharField(max_length=255, blank=True, null=True)
    nick_name = models.CharField(max_length=50, blank=True, null=True)
    stadium = models.ForeignKey(Stadium, related_name='teams')
    foundation_date = models.DateField(blank=True, null=True)
    crest = models.ImageField(upload_to='/crests/', blank=True, null=True)

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
    date_of_birth = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='/photos/', blank=True, null=True)
    # fmh
    # favored_person = models.ForeignKey('Person')
    # favored_team = models.ForeignKey(Team)

    class Meta:
        abstract = True


class Player(Person):
    nationality = CountryField()
    favored_position = models.CharField(max_length=4, blank=True, null=True)

    def get_contract_expiry_date(self):
        pass

    def get_current_team(self):
        pass


class Official(Person):
    nationality = CountryField(null=True, blank=True)
    pass


# Doesn't handle cases where a player is also a staff. e.g.: Giggsy 2013/14 :D
class Staff(Person):
    nationality = CountryField()
    roles = [('Manager', 'manager'), ('Goal Keeping Coach', 'goal_keeping_coach')]
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
    referee = models.ForeignKey(Official, related_name='refereed_matches', blank=True, null=True)
    assistant_referee_1 = models.ForeignKey(Official, related_name='assisted_matches', blank=True, null=True)
    assistant_referee_2 = models.ForeignKey(Official, related_name='assisted_matches2', blank=True, null=True)
    match_referee = models.ForeignKey(Official, blank=True, null=True)


# Match Events

class Goal(models.Model):
    scorer = models.ForeignKey(Player, related_name='goals')
    assist_by = models.ForeignKey(Player, related_name='assists', blank=True, null=True)
    penalty = models.BooleanField(default=False)
    own_goal = models.BooleanField(default=False)
    time = models.PositiveIntegerField()
    match = models.ForeignKey(Match, related_name='goals')


# class Card(models.Model):
# player = models.ForeignKey(Player)
# time = models.PositiveIntegerField()
# match = models.ForeignKey(Match)
#
# class Meta:
# abstract = True


class YellowCard(models.Model):
    player = models.ForeignKey(Player, related_name='yellow_cards')
    time = models.PositiveIntegerField()
    match = models.ForeignKey(Match, related_name='yellow_cards')


class RedCard(models.Model):
    player = models.ForeignKey(Player, related_name='red_cards')
    time = models.PositiveIntegerField()
    match = models.ForeignKey(Match, related_name='red_cards')


class Substitution(models.Model):
    subbed_in = models.ForeignKey(Player, related_name='subbed_in')
    subbed_out = models.ForeignKey(Player, related_name='subbed_out')
    types = [('Injury', 'injury'), ('Tactical', 'tactical')]
    type = models.CharField(max_length=10, choices=types, null=True, blank=True)
    time = models.PositiveIntegerField()


# Pure stats

class StatSet(models.Model):
    """
    Holds all the basic stats of a game such as possession, shots on goal
    so on and so forth
    """

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


# class PlayerStatLine(models.Model):
# """ Used for collecting the stat line for a player in a game """
#
# player = models.ForeignKey(Player)
# match = models.ForeignKey(Match)
#     shots = models.IntegerField(default=0)
#     shots_on_goal = models.IntegerField(default=0)
#     minutes = models.IntegerField(default=0)
#     goals = models.IntegerField(default=0)
#     assists = models.IntegerField(default=0)
#     fouls_committed = models.IntegerField(default=0)
#     fouls_suffered = models.IntegerField(default=0)
#     corners = models.IntegerField(default=0)
#     offsides = models.IntegerField(default=0)
#     saves = models.IntegerField(default=0)
#     goals_against = models.IntegerField(default=0)
#
#     def __unicode__(self):
#         return u'Stats for %s' % self.player

# Formation
# Position


class Injury(models.Model):
    player = models.ForeignKey(Player, related_name='injuries')
    injuries = [('Groin', 'Groin'), ('Hamstring', 'Hamstring'), ('MCL', 'MCL'), ('ACL', 'ACL')]
    # Ankle, Illness, Shoulder, Finger,
    type = models.CharField(max_length=100, choices=injuries, null=True, blank=True)
    injury_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    return_date_confirmed = models.BooleanField(default=True)
    remarks = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Injuries'


class Quote(models.Model):
    text = models.TextField()
    by = models.CharField(max_length=255, null=True, blank=True)
    enabled = models.BooleanField(default=True)

    def excerpt(self):
        txt = self.text
        if len(txt) < 101:
            return txt
        return txt[0:98] + ' ...'


class SeasonData(models.Model):
    year = models.IntegerField('Year', max_length=4, choices=YEAR_CHOICES)
    summary = JSONField()
    matches = JSONField()

    def __unicode__(self):
        return unicode(self.year)

    class Meta:
        verbose_name_plural = 'Seasons Data'