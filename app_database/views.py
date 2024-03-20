from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.authtoken.models import Token

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .swagger_schema_doc import user_response_schema
from .models import UserProxy
from .serializers import UserSerializer, UsersListSerializer, UserDetailSerializer, CustomAuthTokenSerializer
from .permissions import IsOwnerOrReadOnly

from django.contrib.auth import authenticate, login


class CustomAuthToken(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomAuthTokenSerializer

    @swagger_auto_schema(
        request_body=CustomAuthTokenSerializer,
        responses={status.HTTP_201_CREATED: openapi.Response('token create')},
    )
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': f'Token {token.key}'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Неверные учетные данные'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def list(request):
        serializer_fields = CustomAuthTokenSerializer().get_fields()
        fields = {}
        for field_name, field in serializer_fields.items():
            field_type = field.__class__.__name__
            fields[field_name] = field_type
        return Response(fields, status=status.HTTP_200_OK)


class UserCreateViewlet(viewsets.ViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={status.HTTP_201_CREATED: openapi.Response('User created', schema=user_response_schema)},
    )
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Автоматическая аутентификация пользователя
        user = authenticate(request, username=request.data['username'], password=request.data['password'])
        if user is not None:
            login(request, user)
            # Создание или обновление токена доступа
            token, created = Token.objects.get_or_create(user=user)
            response_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'token': token.key
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Authentication failed'}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def list(request):
        serializer_fields = UserSerializer().get_fields()
        fields = {}
        for field_name, field in serializer_fields.items():
            field_type = field.__class__.__name__
            fields[field_name] = field_type
        return Response(fields, status=status.HTTP_200_OK)


class UsersListViewSet(viewsets.ModelViewSet):
    queryset = UserProxy.objects.all().order_by('id')
    serializer_class = UsersListSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return UsersListSerializer  # Используем сериализатор для списка пользователей
        return UserDetailSerializer

from rest_framework.views import APIView

# class UserCreateViewlet(viewsets.ViewSet):
#     serializer_class = UserSerializer
#     permission_classes = [permissions.AllowAny]
#
#     @swagger_auto_schema(
#         request_body=UserSerializer,
#         responses={status.HTTP_201_CREATED: openapi.Response('User created', schema=user_response_schema)},
#     )
#     def create(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#
#         response_data = {
#             'id': user.id,
#             'username': user.username,
#             'email': user.email,
#         }
#         return Response(response_data, status=status.HTTP_201_CREATED)
#
#     @staticmethod
#     def list(request):
#         serializer_fields = UserSerializer().get_fields()
#         fields = {}
#         for field_name, field in serializer_fields.items():
#             field_type = field.__class__.__name__
#             fields[field_name] = field_type
#         return Response(fields, status=status.HTTP_200_OK)
# class CustomAuthToken(viewsets.ViewSet):
#     """
#     API endpoint для получения токена аутентификации пользователя.
#     """
#
#     @staticmethod
#     def create(request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#
#         user = authenticate(request, username=username, password=password)
#         if user:
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Неверные учетные данные'}, status=status.HTTP_400_BAD_REQUEST)