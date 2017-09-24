from rest_framework import serializers
from apps.users.models import User, Membership


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        exclude = ('status', 'homepage', 'user', 'registration_date', 'approved_date', 'approved_by', 'payment', 'expiry_date')
        # fields = ('date_of_birth', 'gender', 'permanent_address', 'mobile', 'identification_file',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'full_name', 'mobile', 'status')
