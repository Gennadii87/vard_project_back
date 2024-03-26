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