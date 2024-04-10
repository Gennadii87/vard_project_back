import mimetypes
import os
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from django.utils import timezone
from django.core.files.base import ContentFile
from django.core.files import File as DjangoFile

from app_url_save_file.serializers import UrlFileLoadSerializer
from app_database.models import File, UserProxy
import json


class UrlFileLoadViewSet(viewsets.ViewSet):
    """Загрузка файла по URL"""
    serializer_class = UrlFileLoadSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response('message', schema=UrlFileLoadSerializer)},
    )
    def list(self, request):
        fields = list(self.serializer_class().fields.keys())
        return Response({'fields': fields})

    @swagger_auto_schema(
        request_body=UrlFileLoadSerializer,
        responses={status.HTTP_201_CREATED: openapi.Response('message', schema=UrlFileLoadSerializer)},
    )
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            url = serializer.validated_data['url_load']
            response = requests.get(url)
            if response.status_code == 200:
                filename_url = os.path.basename(url)
                mime_type, _ = mimetypes.guess_type(filename_url)
                if mime_type:
                    ext_type = mime_type.split('/')[-1]
                else:
                    ext_type = 'json'

                filename = f"File_{timezone.now().strftime('%Y_%m_%d_%H_%M_%S')}.{ext_type}"
                name, extension = filename.rsplit('.', 1)
                mime_type, encoding = mimetypes.guess_type(filename)
                if mime_type:
                    extension_type = mime_type.split('/')[-1].upper()
                else:
                    extension_type = 'OTHER'

                content = response.content
                if ext_type == 'json':
                    try:
                        content = json.dumps(json.loads(content), indent=4)
                    except json.JSONDecodeError:
                        pass

                file_model = File(
                    user_id=UserProxy.objects.get(id=1),
                    name=name,
                    link=DjangoFile(ContentFile(content), name=filename),
                    type_id=extension_type,
                )
                file_model.save()
                return Response({'File': f'{file_model.name}.{ext_type}', 'message': 'File successfully saved', },
                                status=status.HTTP_201_CREATED, )
            else:
                return Response({'error': 'Failed to fetch file from the provided URL'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
