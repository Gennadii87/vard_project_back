from drf_yasg import openapi

user_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
        'username': openapi.Schema(type=openapi.TYPE_STRING),
        'email': openapi.Schema(type=openapi.TYPE_STRING),
    },
    example={
        'id': 1,
        'username': 'example_user',
        'email': 'user@example.com',
    }
)