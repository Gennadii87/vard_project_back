import os

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import serializers
from .models import UserProxy, PasswordChangeDate, File, Access, Feedback, Chart, Dashboard, Comment, ReadComment
from django.urls import reverse

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
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True,  required=False)
    password_date = serializers.DateTimeField(source='password_change_date.date_password_changed', read_only=True,
                                              format='%Y-%m-%d %H:%M:%S')
    token = serializers.CharField(source='auth_token.key', read_only=True)

    class Meta:
        model = UserProxy
        exclude = ['is_staff', 'is_superuser', 'groups', 'user_permissions']
        extra_kwargs = {
            'last_login': {'read_only': True},
            'date_joined': {'read_only': True},
        }

    def update(self, instance, validated_data):
        # Проверяем, был ли предоставлен новый пароль
        if 'password' in validated_data:
            new_password = validated_data['password']
            if not instance.check_password(new_password):
                # Если пароли различаются, обновляем пароль
                instance.set_password(new_password)
                validated_data.pop('password')  # Удаляем пароль из словаря validated_data
            else:
                # Если пароли совпадают, удаляем пароль из validated_data
                validated_data.pop('password')
        # Обновляем остальные поля
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()  # Сохраняем
        return instance


class FileSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='file-detail')
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = '__all__'

    def create(self, validated_data):
        instance = super().create(validated_data)  # Создаем экземпляр модели
        return instance

    # def create(self, validated_data):
    #     instance = super().create(validated_data)
    #
    #     file_field = instance.link
    #
    #     if file_field:
    #         file_extension = os.path.splitext(file_field.name)[1]
    #         new_file_name = f"{validated_data['name']}{file_extension}"
    #
    #         old_file_path = file_field.path
    #         new_file_path = os.path.join(os.path.dirname(old_file_path), new_file_name)
    #
    #         # Переименовываем файл
    #         os.rename(old_file_path, new_file_path)
    #
    #         # Создаем новый файл ContentFile
    #         with open(new_file_path, 'rb') as new_file:
    #             content = new_file.read()
    #             new_content_file = ContentFile(content)
    #
    #         # Обновляем поле link в модели с новым именем файла
    #         instance.link.save(new_file_name, new_content_file, save=True)

        return instance
    def get_download_url(self, obj):
        request = self.context.get('request')
        if obj.link:
            file_id = obj.id
            download_url = request.build_absolute_uri(reverse('file-download', args=[file_id]))
            return download_url
        return None

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