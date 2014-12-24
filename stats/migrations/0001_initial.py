# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompetitionYear',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField(default=2014, max_length=4, verbose_name=b'Year', choices=[(1890, 1890), (1891, 1891), (1892, 1892), (1893, 1893), (1894, 1894), (1895, 1895), (1896, 1896), (1897, 1897), (1898, 1898), (1899, 1899), (1900, 1900), (1901, 1901), (1902, 1902), (1903, 1903), (1904, 1904), (1905, 1905), (1906, 1906), (1907, 1907), (1908, 1908), (1909, 1909), (1910, 1910), (1911, 1911), (1912, 1912), (1913, 1913), (1914, 1914), (1915, 1915), (1916, 1916), (1917, 1917), (1918, 1918), (1919, 1919), (1920, 1920), (1921, 1921), (1922, 1922), (1923, 1923), (1924, 1924), (1925, 1925), (1926, 1926), (1927, 1927), (1928, 1928), (1929, 1929), (1930, 1930), (1931, 1931), (1932, 1932), (1933, 1933), (1934, 1934), (1935, 1935), (1936, 1936), (1937, 1937), (1938, 1938), (1939, 1939), (1940, 1940), (1941, 1941), (1942, 1942), (1943, 1943), (1944, 1944), (1945, 1945), (1946, 1946), (1947, 1947), (1948, 1948), (1949, 1949), (1950, 1950), (1951, 1951), (1952, 1952), (1953, 1953), (1954, 1954), (1955, 1955), (1956, 1956), (1957, 1957), (1958, 1958), (1959, 1959), (1960, 1960), (1961, 1961), (1962, 1962), (1963, 1963), (1964, 1964), (1965, 1965), (1966, 1966), (1967, 1967), (1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014)])),
                ('competition', models.ForeignKey(related_name='seasons', to='stats.Competition')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.PositiveIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Official',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('slug', models.CharField(max_length=254)),
                ('date_of_birth', models.DateField()),
                ('nationality', models.ForeignKey(related_name='officials', blank=True, to='stats.Country', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('slug', models.CharField(max_length=254)),
                ('date_of_birth', models.DateField()),
                ('favored_position', models.CharField(max_length=4)),
                ('nationality', models.ForeignKey(related_name='players', to='stats.Country')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlayerCareerSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True, blank=True)),
                ('wage', models.FloatField(null=True, blank=True)),
                ('player', models.ForeignKey(related_name='career_sessions', to='stats.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RedCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.PositiveIntegerField()),
                ('match', models.ForeignKey(related_name='red_cards', to='stats.Match')),
                ('player', models.ForeignKey(related_name='red_cards', to='stats.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stadium',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('capacity', models.PositiveIntegerField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('city', models.ForeignKey(related_name='stadiums', to='stats.City')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('slug', models.CharField(max_length=254)),
                ('date_of_birth', models.DateField()),
                ('role', models.CharField(max_length=254, choices=[(b'Manager', b'manager'), (b'Goal Keeping Coach', b'goal_keeping_coach')])),
                ('nationality', models.ForeignKey(related_name='staffs', to='stats.Country')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StaffCareerSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True, blank=True)),
                ('wage', models.FloatField(null=True, blank=True)),
                ('staff', models.ForeignKey(related_name='career_sessions', to='stats.Staff')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StatSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attempts_on_goal', models.IntegerField()),
                ('shots_on_target', models.IntegerField()),
                ('shots_off_target', models.IntegerField()),
                ('blocked_shots', models.IntegerField()),
                ('corner_kicks', models.IntegerField()),
                ('fouls', models.IntegerField()),
                ('crosses', models.IntegerField()),
                ('offsides', models.IntegerField()),
                ('first_yellows', models.IntegerField()),
                ('second_yellows', models.IntegerField()),
                ('red_cards', models.IntegerField()),
                ('duels_won', models.IntegerField()),
                ('duels_won_percentage', models.IntegerField()),
                ('total_passes', models.IntegerField()),
                ('pass_percentage', models.IntegerField()),
                ('possession', models.DecimalField(max_digits=4, decimal_places=2)),
                ('match', models.ForeignKey(related_name='stats', to='stats.Match')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('short_name', models.CharField(max_length=10)),
                ('alternative_names', models.CharField(max_length=255)),
                ('nick_name', models.CharField(max_length=50)),
                ('foundation_date', models.DateField(null=True, blank=True)),
                ('crest', models.ImageField(upload_to=b'/crests/')),
                ('stadium', models.ForeignKey(related_name='teams', to='stats.Stadium')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TeamYear',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField(max_length=4, verbose_name=b'Year', choices=[(1890, 1890), (1891, 1891), (1892, 1892), (1893, 1893), (1894, 1894), (1895, 1895), (1896, 1896), (1897, 1897), (1898, 1898), (1899, 1899), (1900, 1900), (1901, 1901), (1902, 1902), (1903, 1903), (1904, 1904), (1905, 1905), (1906, 1906), (1907, 1907), (1908, 1908), (1909, 1909), (1910, 1910), (1911, 1911), (1912, 1912), (1913, 1913), (1914, 1914), (1915, 1915), (1916, 1916), (1917, 1917), (1918, 1918), (1919, 1919), (1920, 1920), (1921, 1921), (1922, 1922), (1923, 1923), (1924, 1924), (1925, 1925), (1926, 1926), (1927, 1927), (1928, 1928), (1929, 1929), (1930, 1930), (1931, 1931), (1932, 1932), (1933, 1933), (1934, 1934), (1935, 1935), (1936, 1936), (1937, 1937), (1938, 1938), (1939, 1939), (1940, 1940), (1941, 1941), (1942, 1942), (1943, 1943), (1944, 1944), (1945, 1945), (1946, 1946), (1947, 1947), (1948, 1948), (1949, 1949), (1950, 1950), (1951, 1951), (1952, 1952), (1953, 1953), (1954, 1954), (1955, 1955), (1956, 1956), (1957, 1957), (1958, 1958), (1959, 1959), (1960, 1960), (1961, 1961), (1962, 1962), (1963, 1963), (1964, 1964), (1965, 1965), (1966, 1966), (1967, 1967), (1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014)])),
                ('home_color', models.CharField(max_length=10, null=True, blank=True)),
                ('away_color', models.CharField(max_length=10, null=True, blank=True)),
                ('third_color', models.CharField(max_length=10, null=True, blank=True)),
                ('team', models.ForeignKey(related_name='seasons', to='stats.Team')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='YellowCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.PositiveIntegerField()),
                ('match', models.ForeignKey(related_name='yellow_cards', to='stats.Match')),
                ('player', models.ForeignKey(related_name='yellow_cards', to='stats.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='statset',
            name='team',
            field=models.ForeignKey(to='stats.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='staffcareersession',
            name='team',
            field=models.ForeignKey(related_name='staff_sessions', to='stats.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='playercareersession',
            name='team',
            field=models.ForeignKey(related_name='player_sessions', to='stats.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='assistant_referee_1',
            field=models.ForeignKey(related_name='assisted_matches', to='stats.Official'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='assistant_referee_2',
            field=models.ForeignKey(related_name='assisted_matches2', to='stats.Official'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='away_team',
            field=models.ForeignKey(related_name='away_matches', to='stats.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='competition_year',
            field=models.ForeignKey(related_name='matches', to='stats.CompetitionYear'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='home_team',
            field=models.ForeignKey(related_name='home_matches', to='stats.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='match_referee',
            field=models.ForeignKey(to='stats.Official'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='referee',
            field=models.ForeignKey(related_name='refereed_matches', to='stats.Official'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='goal',
            name='assist_by',
            field=models.ForeignKey(related_name='assists', to='stats.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='goal',
            name='match',
            field=models.ForeignKey(related_name='goals', to='stats.Match'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='goal',
            name='scorer',
            field=models.ForeignKey(related_name='goals', to='stats.Player'),
            preserve_default=True,
        ),
    ]
