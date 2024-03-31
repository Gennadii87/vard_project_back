from drf_yasg import openapi

user_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
        'username': openapi.Schema(type=openapi.TYPE_STRING),
        'email': openapi.Schema(type=openapi.TYPE_STRING),
        'token': openapi.Schema(type=openapi.TYPE_STRING),
    },
    example={
        'id': 1,
        'username': 'example_user',
        'email': 'user@example.com',
        'token': 'Token 22d48d47d2a574719d91dc2dc68f708b6192f4d1'
    }
)

file_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'place_id': openapi.Schema(type=openapi.TYPE_STRING),
        'type_id': openapi.Schema(type=openapi.TYPE_STRING),
        'name': openapi.Schema(type=openapi.TYPE_STRING),
        'publish': openapi.Schema(type=openapi.TYPE_INTEGER),
        'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
    },
    example={
        'place_id': "CHOICES = ['CM', 'MF', 'BP']",
        'type_id': "CHOICES = ['CSV', 'JSON', 'Excel', 'PDF']",
        'name': 'file_name',
        'publish': 'CHOICES = [0, 1]',
        'user_id': 1,
    }
)
