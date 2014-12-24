from django.contrib import admin
from .models import Injury, Competition, CompetitionYear, City

admin.site.register(Injury)
admin.site.register(Competition)
admin.site.register(CompetitionYear)
admin.site.register(City)
