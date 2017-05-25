from django.shortcuts import render
from django.views.generic import DetailView

from .models import Album


def album_list(request):
    albums = Album.objects.order_by('-event__end')
    return render(request, 'album.html', {'albums': albums})


class AlbumDetail(DetailView):
    model = Album
