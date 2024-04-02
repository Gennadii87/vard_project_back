from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from django.utils import timezone
from rest_framework import serializers
from .models import UserProxy, PasswordChangeDate, File, Access, Feedback, Chart, Dashboard, Comment, ReadComment


class PasswordChangeDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordChangeDate
        fields = ('date_password_changed',)


class LoginAuthTokenSerializer(serializers.Serializer):
    """
    Сериализатор для аутентификации пользователя и получения токена.
    """
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        fields = ('username', 'password')


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='userproxy-detail')
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProxy
        fields = ('id', 'username', 'email', 'url', 'password', )
        extra_kwargs = {
            'username': {'required': True},  # username обязателен при создании
            'password': {'required': True},  # password обязателен при создании
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = UserProxy.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        PasswordChangeDate.objects.create(user=user, date_password_changed=timezone.now(), change_type="created")
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True,  required=False)
    password_date = serializers.CharField(source='password_change_date', read_only=True,)
    token = serializers.CharField(source='auth_token.key', read_only=True)

    class Meta:
        model = User
        exclude = ['is_staff', 'is_superuser', 'groups', 'user_permissions']
        extra_kwargs = {
            'last_login': {'read_only': True},
            'date_joined': {'read_only': True},
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.password = make_password(password)
            password_change_date = PasswordChangeDate.objects.get(user=instance)
            password_change_date.date_password_changed = timezone.now()
            password_change_date.change_type = "changed"
            password_change_date.save()
            print(password_change_date)
        return super().update(instance, validated_data)


class FileSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='file-detail')
    download_url = serializers.HyperlinkedIdentityField(view_name='file-download')

    class Meta:
        model = File
        fields = '__all__'


class AccessSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='access-detail')

    class Meta:
        model = Access
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='feedback-detail')

    class Meta:
        model = Feedback
        fields = '__all__'


class ChartSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='chart-detail')

    class Meta:
        model = Chart
        fields = '__all__'


class DashboardSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='dashboard-detail')

    class Meta:
        model = Dashboard
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='comment-detail')

    class Meta:
        model = Comment
        fields = '__all__'


class ReadCommentSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='readcomment-detail')

    class Meta:
        model = ReadComment
        fields = '__all__'
