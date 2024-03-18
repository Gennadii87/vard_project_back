from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets, permissions

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .swagger_schema_doc import user_response_schema
from .models import UserProxy
from .serializers import UserSerializer, UsersListSerializer


class UserCreateViewlet(viewsets.ViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={status.HTTP_201_CREATED: openapi.Response('User created', schema=user_response_schema)},
    )
    def create(self, request):
        if not request.data:
            serializer_fields = UserSerializer().get_fields()
            fields = {}
            for field_name, field in serializer_fields.items():
                field_type = field.__class__.__name__
                fields[field_name] = field_type
            return Response(fields, status=status.HTTP_200_OK)

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class UsersListViewSet(viewsets.ModelViewSet):
    queryset = UserProxy.objects.all()
    serializer_class = UsersListSerializer
    # permission_classes = [permissions.IsAuthenticated]
