from django.shortcuts import render

from .models import Image, Album


def album_list(request):
    albums = Album.objects.all()
    return render(request, 'album.html', {'albums': albums})


def album_images(request, slug):
    images = Image.objects.filter(album__slug=slug)
    try:
        album_name = images[0].album.name
    except IndexError:
        return render(request, 'album_images.html', {'object': images})
    return render(request, 'album_images.html', {'images': images, 'album_name': album_name})

# Create your views here.
