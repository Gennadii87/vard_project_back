import MySQLdb

from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, permissions

from app_database.permissions import IsOwnerOrReadOnly
from .models import UserDataBaseProfile
from .serializers import DatabaseConnectionSerializer, SqlQuerySerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class DatabaseConnectionViewSet(viewsets.ModelViewSet):
    """Ограничения временно отключены"""
    serializer_class = DatabaseConnectionSerializer
    queryset = UserDataBaseProfile.objects.all().order_by('id')

    # permission_classes = [permissions.IsAuthenticated]

    # def get_permissions(self):
    #     if self.action == 'create':
    #         return [permissions.IsAuthenticated()]
    #     elif self.action == 'list':
    #         return [permissions.AllowAny(),]
    #     return super().get_permissions()

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            queryset = self.queryset.filter(user=request.user)
        else:
            queryset = self.queryset.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        request_body=DatabaseConnectionSerializer,
        responses={status.HTTP_201_CREATED: openapi.Response('message')},
    )
    def create(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            validated_data = serializer.validated_data
            # user = request.user
            user = validated_data.pop('user')  # Удаляем 'user' из validated_data
            instance = self.queryset.create(user=user, **validated_data)
            db_type = validated_data.get('db_type')
            try:

                if db_type == 'mysql':
                    import MySQLdb as db
                elif db_type == 'postgresql':
                    import psycopg2 as db
                else:
                    return Response({'error': 'Unsupported database type'}, status=status.HTTP_400_BAD_REQUEST)

                conn = db.connect(
                    host=validated_data.get('db_host'),
                    user=validated_data.get('db_username'),
                    password=validated_data.get('db_password'),
                    port=validated_data.get('db_port')
                )
                serv_info = None
                if db_type == 'mysql':
                    serv_info = conn.get_server_info()
                elif db_type == 'postgresql':
                    cursor = conn.cursor()
                    cursor.execute("SELECT VERSION();")
                    serv_info = cursor.fetchall()
                    cursor.close()

                conn.close()
                return Response({
                    'ver.server sql': serv_info,
                    'message': 'Соединение успешно установлено'
                }, status=status.HTTP_200_OK)
            except MySQLdb.Error as exception:
                instance.delete()
                return Response({'error': f'Ошибка при подключении к базе данных: {str(exception)}'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SqlQueryViewSet(viewsets.ViewSet):
    """Ограничения временно отключены"""
    serializer_class = SqlQuerySerializer

    # permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def list(self, request):
        fields = list(self.serializer_class().fields.keys())
        return Response({'fields': fields})

    @swagger_auto_schema(
        request_body=SqlQuerySerializer,
        responses={status.HTTP_201_CREATED: openapi.Response('sql_query', schema=SqlQuerySerializer)},
    )
    def create(self, request):
        # Получаем SQL-запрос и идентификатор базы данных из запроса
        sql_query = request.data.get('sql_query', '')
        pofile_id = request.data.get('base_profile_id', None)

        if pofile_id:
            try:
                database = UserDataBaseProfile.objects.get(id=pofile_id)
                host = database.db_host
                port = database.db_port
                username = database.db_username
                password = database.db_password
                db_type = database.db_type

                if db_type == 'mysql':
                    import MySQLdb as db
                elif db_type == 'postgresql':
                    import psycopg2 as db
                else:
                    return Response({'error': 'Unsupported database type'}, status=status.HTTP_400_BAD_REQUEST)

                conn = db.connect(
                    host=host,
                    user=username,
                    password=password,
                    port=port
                )
                cursor = conn.cursor()
                # Выполняем SQL-запрос
                cursor.execute(sql_query)
                results = cursor.fetchall()
                cursor.close()
                conn.close()
                return Response(results, status=status.HTTP_200_OK)
            except UserDataBaseProfile.DoesNotExist:
                return Response({'error': 'Указанная база данных не найдена'}, status=status.HTTP_400_BAD_REQUEST)
            except MySQLdb.Error as exception:
                return Response({'error': f'Ошибка при выполнении запроса: {str(exception)}'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'Идентификатор базы данных не предоставлен'}, status=status.HTTP_400_BAD_REQUEST)
