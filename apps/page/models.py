from django.core.urlresolvers import reverse
from django.db import models
from apps.users.models import User
from mptt.models import MPTTModel, TreeForeignKey
from app.utils.forms import unique_slugify
import datetime
from froala_editor.fields import FroalaField


class Category(MPTTModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, blank=True)
    description = models.TextField(null=True, blank=True)
    parent = TreeForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='children')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = u'Categories'

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        super(Category, self).save(*args, **kwargs)

    def get_all_categories(self):
        return list(self.get_ancestors(include_self=True))


class Page(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Leave empty/unchanged for default slug.')
    content = FroalaField(null=True, blank=True)
    author = models.ForeignKey(User)
    template = models.CharField(max_length=255, blank=True, null=True)
    statuses = (
        ('Published', 'Published'), ('Draft', 'Draft'), ('Trashed', 'Trashed'))
    status = models.CharField(
        max_length=10,
        choices=statuses,
        default='Published')
    comments_enabled = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, blank=True)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        unique_slugify(self, self.title)
        if not self.id:
            self.created_at = datetime.datetime.today()
        self.updated_at = datetime.datetime.today()
        super(Page, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('view_news', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
