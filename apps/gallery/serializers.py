# from rest_framework import serializers
# from .models import Album, Image
#
#
# class ImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Image
#         exclude = ()
#
#
# class AlbumSerializer(serializers.ModelSerializer):
#     images = ImageSerializer(many=True)
#
#     class Meta:
#         model = Album
#         exclude = ()
