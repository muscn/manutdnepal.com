from django import forms
import re
from django.template.defaultfilters import slugify


def _slug_strip(value, separator='-'):
    """
    Cleans up a slug by removing slug separator characters that occur at the
    beginning or end of a slug.

    If an alternate separator is used, it will also replace any instances of
    the default '-' separator with the new separator.
    """
    separator = separator or ''
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
        # Remove multiple instances and if an alternate separator is provided,
    # replace the default '-' separator.
    if separator != re_sep:
        value = re.sub('%s+' % re_sep, separator, value)
        # Remove separator from the beginning and end of the slug.
    if separator:
        if separator != '-':
            re_sep = re.escape(separator)
        value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)
    return value


def unique_slugify(instance, value, slug_field_name='slug', queryset=None, slug_separator='-'):
    """
    Calculates and stores a unique slug of ``value`` for an instance.

    ``slug_field_name`` should be a string matching the name of the field to
    store the slug in (and the field to check against for uniqueness).

    ``queryset`` usually doesn't need to be explicitly provided - it'll default
    to using the ``.all()`` queryset from the model's default manager.
    """
    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug, limiting its length if necessary.
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    # Create the queryset if one wasn't explicitly provided and exclude the
    # current instance from the queryset.
    if queryset is None:
        queryset = instance.__class__._default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = '%s%s' % (slug_separator, next)
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[:slug_len - len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = '%s%s' % (slug, end)
        next += 1

    setattr(instance, slug_field.attname, slug)


class HTML5ModelForm(forms.ModelForm):
    class EmailTypeInput(forms.widgets.TextInput):
        input_type = 'email'

    class NumberTypeInput(forms.widgets.TextInput):
        input_type = 'number'

    class TelephoneTypeInput(forms.widgets.TextInput):
        input_type = 'tel'

    class DateTypeInput(forms.widgets.DateInput):
        input_type = 'date'

    class DateTimeTypeInput(forms.widgets.DateTimeInput):
        input_type = 'datetime'

    class TimeTypeInput(forms.widgets.TimeInput):
        input_type = 'time'

    def __init__(self, *args, **kwargs):
        super(HTML5ModelForm, self).__init__(*args, **kwargs)
        for (name, field) in self.fields.items():
            file_fields = [forms.fields.ImageField, forms.fields.FileField]
            # add HTML5 required attribute for required fields, except for file fields which already have a value
            if field.required and not (field.__class__ in file_fields and getattr(self.instance, name)):
                field.widget.attrs['required'] = 'required'

    def hide_field(self, request):
        for query in request.GET:
            if query[-3:] == '_id':
                query = query[:-3]
            self.fields[query].widget = self.fields[query].hidden_widget()
            self.fields[query].label = ''
        return self


class BootstrapForm(forms.Form):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        self.exclude = kwargs.pop('exclude', None)
        super().__init__(*args, **kwargs)
        if self.exclude:
            del self.fields[self.exclude]
        self.refine()

    def refine(self):
        for (i, (name, field)) in enumerate(self.fields.items()):
            widget = field.widget
            exclude_form_control = ['CheckboxInput', 'RadioSelect']
            if widget.__class__.__name__ in exclude_form_control:
                continue
            if 'class' in widget.attrs:
                widget.attrs['class'] += ' form-control'
            else:
                widget.attrs['class'] = 'form-control'
            # Auto-focus for first field of forms
            if i == 0:
                widget.attrs['autofocus'] = True


class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BootstrapModelForm, self).__init__(*args, **kwargs)
        for (name, field) in self.fields.items():
            widget = field.widget
            exclude_form_control = ['CheckboxInput', 'RadioSelect']
            if widget.__class__.__name__ in exclude_form_control:
                continue
            if 'class' in widget.attrs:
                widget.attrs['class'] += ' form-control'
            else:
                widget.attrs['class'] = 'form-control'


class HTML5BootstrapModelForm(HTML5ModelForm, BootstrapModelForm):
    pass
