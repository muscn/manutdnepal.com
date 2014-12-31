from users.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'full_name', 'email',
                  'is_active', 'is_staff', 'is_superuser')


class UserSerializer1(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    full_name = serializers.CharField(max_length=245)
    email = serializers.EmailField(max_length=254)
    is_active = serializers.BooleanField(default=True)
    is_staff = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        import pdb
        pdb.set_trace()
        instance.username = validated_data.get('username', instance.username)
        instance.full_name = validated_data.get(
            'full_name', instance.full_name)
        instance.email = validated_data.get('email', instance.email)
        instance.is_active = validated_data.get(
            'is_active', instance.is_active)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.is_superuser = validated_data.get(
            'is_superuser', instance.is_superuser)
        instance.save()
        return instance
