from django.db import models
from apps.users.models import User
from muscn.utils.forms import unique_slugify


class Person(models.Model):
    user = models.ForeignKey(User)
    slug = models.SlugField(max_length=254, blank=True)
    image = models.ImageField(upload_to='photos/', blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    birth_place = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        unique_slugify(self, self.user.full_name)
        super(Person, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.full_name

    class Meta:
        abstract = True
        ordering = ('order',)


class Player(Person):
    positions = models.CharField(max_length=50, blank=True, null=True)
    squad_no = models.PositiveIntegerField(blank=True, null=True)


class Staff(Person):
    role = models.CharField(max_length=50, blank=True, null=True)
    pass
