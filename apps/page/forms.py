from django.forms import ModelForm, ChoiceField
from .models import Page
from os.path import isfile, join, splitext
from os import listdir


class PageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        from django.template.utils import get_app_template_dirs

        app_template_dirs = get_app_template_dirs('templates')
        templates = []
        for dir_path in app_template_dirs:
            if dir_path.find('/page/template') == -1:
                continue
            template_dir = join(dir_path, 'page_templates')
            files = [
                (join(
                    template_dir,
                    f),
                 splitext(f)[0].title()) for f in listdir(template_dir) if isfile(
                    join(
                        template_dir,
                        f))]
            templates += files
        self.base_fields['template'] = ChoiceField(choices=templates)
        super(PageForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Page
        exclude = ()
