from rest_framework import serializers

from apps.page.models import Page


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
