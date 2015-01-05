from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView as BaseUpdateView, CreateView as BaseCreateView, \
    DeleteView as BaseDeleteView


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
        messages.success(request, self.object.__class__.__name__ + ' successfully deleted!')
        return response