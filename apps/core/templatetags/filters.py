from django.template import Library
import re

register = Library()


@register.filter
def get_class_name(value):
    return value.__class__.__name__


@register.filter
def get_class(value):
    return value.__class__


@register.filter
def key(value):
    dct = {
        'SF': 'Semi-finals',
        'Prem': 'Premier League',
        'Div 1': 'Division 1',
        'Div 2': 'Division 2',
        'Alliance': 'Football Alliance',
        'Combination': 'The Combination',
        'F': 'Final',
        'Group': 'Group',
        'QF': 'Quarter-finals',
        'QR1': 'First Qualifying Round',
        'QR2': 'Second Qualifying Round',
        'QR3': 'Third Qualifying Round',
        'QR4': 'Fourth Qualifying Round',
        'RInt': 'Intermediate Round',
        'R1': 'Round 1',
        'R2': 'Round 2',
        'R3': 'Round 3',
        'R4': 'Round 4',
        'R5': 'Round 5',
        'R6': 'Round 6',
        'H': 'Home',
        'A': 'Away',
        's': 'Semi-finals',
        'f': 'Final',
    }
    if value in dct:
        return dct[value]
    return value


@register.filter
def get_cardinal(value):
    if value == '':
        return value
    pattern = '(\d*).*'
    matches = re.match(pattern, value).groups()
    if matches:
        return int(matches[0])
    return value


@register.filter
def has_key(lst, key):
    for item in lst:
        if key in item:
            return True
    return False


@register.filter
def winner(match):
    if match['hg'] == match['ag']:
        return 'draw'
    if int(match['hg']) > int(match['ag']):
        return 'H'
    return 'A'


@register.filter
def result(match):
    res = winner(match)
    if res == 'draw':
        return 'draw'
    if res == match['ha']:
        return 'won'
    return 'lost'



