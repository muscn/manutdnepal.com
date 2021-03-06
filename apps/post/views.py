from django.views.generic import DetailView
from django.views.generic.list import ListView

from .models import Post


class PostList(ListView):
    queryset = Post.objects.filter(status='Published')


class PostDetail(DetailView):
    queryset = Post.objects.filter(status='Published')
