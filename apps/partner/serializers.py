from rest_framework import serializers

from .models import Partner


class PartnerSer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        exclude = []