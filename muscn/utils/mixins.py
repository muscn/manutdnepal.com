from random import randint

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from django.core.cache import cache
from django.db.models import Q
from django.views.generic.edit import UpdateView as BaseUpdateView, CreateView as BaseCreateView, \
    DeleteView as BaseDeleteView
from django.contrib.admin.filters import SimpleListFilter


class CachedModel(models.Model):
    @classmethod
    def get_all(cls):
        # Override on inherited class if necessary, e.g.
        # return cls.objects.filter(enabled=True)
        return cls.objects.all()

    @classmethod
    def get_cached(cls):
        all_instances = cache.get(cls._meta.verbose_name_plural)
        if not all_instances:
            all_instances = list(cls.get_all())
            cache.set(cls._meta.verbose_name_plural, all_instances, timeout=None)
        return all_instances

    @classmethod
    def random(cls):
        instances = cls.get_cached()
        if not instances:
            return None
        random_index = randint(0, len(instances) - 1)
        return instances[random_index]

    @classmethod
    def invalidate_cache(cls):
        cache.delete(cls._meta.verbose_name_plural)

    def save(self, *args, **kwargs):
        self.invalidate_cache()
        super(CachedModel, self).save()

    class Meta:
        abstract = True


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class UpdateView(BaseUpdateView):
    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['scenario'] = 'Update'
        return context


class CreateView(BaseCreateView):
    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['scenario'] = 'Create'
        return context


class DeleteView(BaseDeleteView):
    def post(self, request, *args, **kwargs):
        response = super(DeleteView, self).post(request, *args, **kwargs)
        messages.success(request, self.object.__class__._meta.verbose_name.title() + ' successfully deleted!')
        return response


class EmptyFilterSpec(SimpleListFilter):
    title = ''

    parameter_name = ''

    def lookups(self, request, model_admin):
        return (
            ('1', 'Has value'),
            ('0', 'None'),
        )

    def queryset(self, request, queryset):
        filters = Q(**{self.parameter_name + '__isnull': True}) | Q(**{self.parameter_name: ''})
        if self.value() == '0':
            return queryset.filter(filters)
        if self.value() == '1':
            return queryset.exclude(filters)
        return queryset
