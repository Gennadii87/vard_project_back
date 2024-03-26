from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.authtoken.models import Token

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .swagger_schema_doc import user_response_schema
from .models import UserProxy, File, Access, Feedback, Chart, Dashboard, Comment, ReadComment
from .serializers import FileSerializer, UserSerializer, AccessSerializer, FeedbackSerializer, ChartSerializer, \
    DashboardSerializer, CommentSerializer, ReadCommentSerializer, UserDetailSerializer, LoginAuthTokenSerializer
from .permissions import IsOwnerOrReadOnly, IsNotAuthenticated

from django.contrib.auth import authenticate, login


class LoginAuthTokenSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginAuthTokenSerializer

    @swagger_auto_schema(
        request_body=LoginAuthTokenSerializer,
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
                login(request, user)
                return Response({'token': f'Token {token.key}', 'id': user.id}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Неверные учетные данные'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def list(request):
        serializer_fields = LoginAuthTokenSerializer().get_fields()
        fields = {}
        for field_name, field in serializer_fields.items():
            field_type = field.__class__.__name__
            fields[field_name] = field_type
        return Response(fields, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProxy.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_permissions(self):
        if self.action == 'create':
            return [IsNotAuthenticated()]  # Разрешаем доступ без аутентификации только при создании пользователя
        elif self.action == 'list':
            return [permissions.AllowAny(),]  # Разрешаем доступ без аутентификации к списку пользователей
        return super().get_permissions()

    def list(self, request, **kwargs):
        if self.request.user.is_authenticated:
            return super().list(request)
        else:
            # Если пользователь не аутентифицирован, возвращаем форму для создания пользователя
            data = {
                'username': '',
                'password': ''
            }
            return Response(data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action != 'list' and self.action != 'create':
            if 'pk' in self.kwargs and str(self.request.user.pk) == self.kwargs['pk']:
                return UserDetailSerializer
        return self.serializer_class

    # @swagger_auto_schema(
    #     request_body=UserSerializer,
    #     responses={status.HTTP_201_CREATED: openapi.Response('User created', schema=user_response_schema)},
    # )
    def create(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, key = Token.objects.get_or_create(user=user)

        response_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'token': token.key
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


# class UserProfileView(viewsets.ModelViewSet):
#     queryset = UserProxy.objects.all()
#     serializer_class = UserSerializeProfile
#     permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
#
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         # Проверяем, что запрос делает текущий пользователь
#         if instance == request.user:
#             serializer = self.get_serializer(instance)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "Недостаточно прав для доступа к этому ресурсу"}, status=status.HTTP_403_FORBIDDEN)

# class UserProfileViewSet(viewsets.ModelViewSet):
#     queryset = UserProxy.objects.none()
#     serializer_class = UserSerializeProfile
#     permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

# def retrieve(self, request, *args, **kwargs):
#     # Получение текущего пользователя из запроса
#     user = request.user
#
#     # Проверка, что пользователь аутентифицирован
#     if user.is_authenticated:
#         # Проверка, что пользователь имеет доступ только к своему профилю
#         if user.pk == kwargs['pk']:
#             instance = self.get_object()
#             serializer = self.get_serializer(instance)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "Недостаточно прав для доступа к этому ресурсу"}, status=status.HTTP_403_FORBIDDEN)
#     else:
#         return Response({"error": "Пользователь не аутентифицирован"}, status=status.HTTP_401_UNAUTHORIZED)

# def get_queryset(self):
#     user = self.request.user
#     queryset = UserProxy.objects.filter(id=user.id)
#     return queryset.order_by('id')

# def retrieve(self, request, *args, **kwargs):
#     instance = self.get_object()
#     serializer = self.get_serializer(instance)
#     return Response(serializer.data, status=status.HTTP_200_OK)

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all().order_by('id')
    serializer_class = FileSerializer


class AccessViewSet(viewsets.ModelViewSet):
    queryset = Access.objects.all().order_by('id')
    serializer_class = AccessSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all().order_by('id')
    serializer_class = FeedbackSerializer


class ChartViewSet(viewsets.ModelViewSet):
    queryset = Chart.objects.all().order_by('id')
    serializer_class = ChartSerializer


class DashboardViewSet(viewsets.ModelViewSet):
    queryset = Dashboard.objects.all().order_by('id')
    serializer_class = DashboardSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('id')
    serializer_class = CommentSerializer


class ReadCommentViewSet(viewsets.ModelViewSet):
    queryset = ReadComment.objects.all().order_by('id')
    serializer_class = ReadCommentSerializer
