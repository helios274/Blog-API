from rest_framework import generics, status, mixins
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema

from .models import User
from .serializers import UserSerializer, UserProfileSerializer
from utils.responses import SuccessResponse
from utils.permissions import IsOwner, IsOwnerOrReadOnly
from utils import swagger_schemas


class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_summary="User Registration",
        operation_description="Registers a new user",
        tags=["Authentication"],
        request_body=UserSerializer,
        responses={
            201: UserSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return SuccessResponse(
                "User created successfully",
                serializer.data,
                "user"
            )
        # error_message = ""
        # for _, errors in serializer.errors.items():
        #     for error in errors:
        #         error_message += str(error)
        #         break
        #     break
        # return ValidationErrorResponse(error_message)


class LoginView(APIView):

    @swagger_auto_schema(
        tags=["Authentication"],
        operation_summary="User Login",
        operation_description="Logins a user",
        request_body=swagger_schemas.LOGIN_REQ_BODY,
        responses={
            200: swagger_schemas.LOGIN_RES_BODY,
        }
    )
    def post(self, request: Request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            raise ValidationError("Email and password are required")
        user = authenticate(request, email=email, password=password)
        print(user)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                data={
                    "tokens": {
                        "access": str(refresh.access_token),
                        "refresh": str(refresh)
                    }
                },
                status=status.HTTP_200_OK,
            )
        raise ValidationError("Invalid credentials")


class UserProfileView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView
):

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    @swagger_auto_schema(
        tags=['User'],
        operation_summary="Get user profile",
        operation_description="Retrieves user profile information",
        responses={
            200: UserProfileSerializer
        }
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['User'],
        operation_summary="Update user profile",
        operation_description="Updates user profile information",
        request_body=swagger_schemas.UPDATE_PROFILE_REQ_BODY,
        responses={
            200: UserProfileSerializer
        }
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['User'],
        operation_summary="Update user profile",
        operation_description="Updates user profile information",
        request_body=swagger_schemas.UPDATE_PROFILE_REQ_BODY,
        responses={
            200: UserProfileSerializer
        }
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


@swagger_auto_schema(
    method='delete',
    tags=['User'],
    operation_summary="Delete user account",
    operation_description="Removes user account along with all posts and comments",
)
@api_view(["DELETE"])
@permission_classes([IsOwner])
def delete_account(request: Request) -> SuccessResponse:
    user = request.user
    user.delete()
    return SuccessResponse("User deleted successfully")
