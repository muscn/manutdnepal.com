import os

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import DetailView

from apps.gallery.http import upload_receive, UploadResponse, JFUResponse
from .models import Album, Image


def album_list(request):
    albums = Album.objects.order_by('-event__end')
    return render(request, 'album.html', {'albums': albums})


class AlbumDetail(DetailView):
    model = Album


@staff_member_required
@require_POST
def multi_upload(request, pk):
    if request.method == 'POST':
        file = upload_receive(request)
        instance = Image(file=file, album_id=pk)
        instance.save()
        basename = os.path.basename(instance.file.path)
        file_dict = {
            'name': basename,
            'size': file.size,

            'url': settings.MEDIA_URL + basename,
            'thumbnailUrl': instance.file.url,

            'deleteUrl': reverse('image-delete', kwargs={'pk': instance.pk}),
            'deleteType': 'POST',
        }
        return UploadResponse(request, file_dict)
    return render(request, 'upload.html')


@require_POST
@staff_member_required
def upload_delete(request, pk):
    success = True
    try:
        instance = Image.objects.get(pk=pk)
        os.unlink(instance.file.path)
        instance.delete()
    except Image.DoesNotExist:
        success = False

    return JFUResponse(request, success)
