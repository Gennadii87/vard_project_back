from django.http import Http404, FileResponse

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.authtoken.models import Token

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from .swagger_schema_doc import user_response_schema, file_response_schema
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
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
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
            return [permissions.AllowAny(),]
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

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={status.HTTP_201_CREATED: openapi.Response('User created', schema=user_response_schema)},
    )
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


class UserAccountViewSet(viewsets.ViewSet):
    serializer_class = UserDetailSerializer
    queryset = UserProxy.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        user_id = self.kwargs.get('pk')
        if self.request.user.is_authenticated:
            try:
                user = self.queryset.get(id=user_id)
                return user
            except UserProxy.DoesNotExist:
                raise Http404('User does not exist')
        else:
            raise Http404('User does not exist')

    def list(self, request, *args, **kwargs):
        instance = request.user.pk
        user = self.queryset.get(pk=instance)
        serializer = self.serializer_class(user)
        # Проверяем совпадение идентификаторов текущего пользователя и пользователя из запроса
        if instance == user.pk:
            return Response(serializer.data, status=status.HTTP_200_OK)  # Если совпадают, возвращаем данные
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, *args, **kwargs):
        try:
            user = self.get_object()
        except Http404:
            # Если объект не существует, возвращаем ответ с кодом статуса 403 Forbidden
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_403_FORBIDDEN)

        # Проверка, что пользователь имеет доступ только к своему профилю
        if user.pk == self.request.user.pk:
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_403_FORBIDDEN)

    @swagger_auto_schema(
        request_body=UserDetailSerializer,
        responses={status.HTTP_200_OK: openapi.Response('User update')},
    )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=UserDetailSerializer,
        responses={status.HTTP_200_OK: openapi.Response('User update')},
    )
    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: openapi.Response('content removed')},
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Проверяем, что пользователь имеет доступ только к своему профилю
        if instance.pk == self.request.user.pk:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_403_FORBIDDEN)


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all().order_by('id')
    serializer_class = FileSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.serializer_class(queryset, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer_fields = self.serializer_class().get_fields()
            fields = {}
            for field_name, field in serializer_fields.items():
                field_type = field.__class__.__name__
                fields[field_name] = field_type
            return Response(file_response_schema.example, status=status.HTTP_204_NO_CONTENT)

    def handle_exception(self, exc):
        error_message = str(exc)
        return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'])
    def download(self, request, pk=None):
        try:
            file_obj = self.get_object()
        except Http404:
            return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)
        file_path = file_obj.link.path  # Получаем путь к файлу
        return FileResponse(open(file_path, 'rb'), as_attachment=True)


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
