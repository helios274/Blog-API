from drf_yasg import openapi


SUCCESS_RES_BODY = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='True'),
        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message'),
        'data': openapi.Schema(type=openapi.TYPE_OBJECT, description='Optional data object')
    },
)

LOGIN_REQ_BODY = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='User email'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description='User password'),
    },
    required=['email', 'password']
)

LOGIN_RES_BODY = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'tokens': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access': openapi.Schema(type=openapi.TYPE_STRING, description='Access token'),
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
            },
        ),
    },
)

UPDATE_PROFILE_REQ_BODY = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'profile_photo': openapi.Schema(type=openapi.TYPE_FILE, description='User profile photo'),
        'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='User first name'),
        'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='User last name'),
        'bio': openapi.Schema(type=openapi.TYPE_STRING, description='User bio'),
    },
)
