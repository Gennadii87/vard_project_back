from rest_framework import serializers
from .models import UserProxy


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProxy
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = UserProxy.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UsersListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProxy
        fields = ['id', 'username', 'email', 'first_name', 'date_joined', ]

