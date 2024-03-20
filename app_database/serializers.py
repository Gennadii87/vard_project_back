from rest_framework import serializers
from .models import UserProxy, PasswordChangeDate


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


class PasswordChangeDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordChangeDate
        fields = ('date_password_changed',)


class UsersListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProxy
        fields = ('id', 'username', 'email', 'first_name', 'url')
        extra_kwargs = {'url': {'view_name': 'user-detail'}}


class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    password_date = PasswordChangeDateSerializer(source='password_change_date', required=False)

    class Meta:
        model = UserProxy
        fields = ('id', 'username', 'email', 'first_name', 'date_joined', 'password_date')


class CustomAuthTokenSerializer(serializers.Serializer):
    """
    Сериализатор для аутентификации пользователя и получения токена.
    """
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        fields = ('username', 'password')
