import datetime
from django.core.urlresolvers import reverse
from django.db import models
from froala_editor.fields import FroalaField
from muscn.utils.forms import unique_slugify


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Leave empty/unchanged for default slug.')
    content = FroalaField(null=True, blank=True)
    statuses = (
        ('Published', 'Published'), ('Draft', 'Draft'), ('Trashed', 'Trashed'))
    status = models.CharField(
        max_length=10,
        choices=statuses,
        default='Published')
    created_at = models.DateTimeField(blank=True)

    @classmethod
    def recent(cls, count=10):
        return cls.objects.filter(status='Published')[0:count]

    def excerpt(self):
        txt = self.content
        if len(txt) < 101:
            return txt
        return txt[0:98] + ' ...'

    def save(self, *args, **kwargs):
        unique_slugify(self, self.title)
        if not self.id:
            self.created_at = datetime.datetime.today()
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('view_post', kwargs={'slug': self.slug})

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('-created_at',)
