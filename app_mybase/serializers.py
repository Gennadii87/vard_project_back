from rest_framework import serializers
from rest_framework.authtoken.admin import User
from rest_framework.generics import get_object_or_404

from app_mybase.models import UserDataBaseProfile


class UserPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """Идентификация пользователя """
    def get_queryset(self):
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            user = request.user
            return User.objects.filter(pk=user.pk)
        return User.objects.none()

    def to_internal_value(self, data):
        instance = get_object_or_404(User, pk=data)
        request = self.context.get('request')
        if request.user != instance:
            raise serializers.ValidationError("You can only set the current authenticated user.")
        return instance


class DatabaseConnectionSerializer(serializers.ModelSerializer):
    """Идентификация пользователя отключена"""
    # user = UserPrimaryKeyRelatedField(queryset=User.objects.all())
    url = serializers.HyperlinkedIdentityField(view_name='userdatabaseprofile-detail', lookup_field='pk')

    class Meta:
        model = UserDataBaseProfile
        fields = '__all__'


class BaseProfileField(serializers.PrimaryKeyRelatedField):
    """Выбор профиля подключения"""
    def get_queryset(self):
        request = self.context.get('request', None)
        if request and not request.user.is_anonymous:
            user = request.user
            return UserDataBaseProfile.objects.filter(user=user)
        return UserDataBaseProfile.objects.none()


class SqlQuerySerializer(serializers.Serializer):
    sql_query = serializers.CharField(max_length=1000)
    base_profile_id = BaseProfileField()
