from django.shortcuts import render
from django.views.generic import DetailView

from .models import Image, Album


def album_list(request):
    albums = Album.objects.all()
    return render(request, 'album.html', {'albums': albums})


class AlbumDetail(DetailView):
    model = Album
