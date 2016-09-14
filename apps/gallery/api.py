# from rest_framework import generics
#
# from .models import Image, Album
# from nepathya.utils import CustomPagination
# from .serializers import ImageSerializer, AlbumSerializer
#
#
# class ImageListAPI(generics.ListAPIView):
#     serializer_class = ImageSerializer
#     queryset = Image.objects.all()
#     pagination_class = CustomPagination
#
#
# class AlbumListAPI(generics.ListAPIView):
#     serializer_class = AlbumSerializer
#     queryset = Album.objects.all()
#     pagination_class = CustomPagination
#
# class AlbumDetailAPI(generics.RetrieveAPIView):
#     serializer_class = AlbumSerializer
#     queryset = Album.objects.all()
