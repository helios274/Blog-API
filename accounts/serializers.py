from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, ValidationError
import re
from pprint import pprint

from .models import User

USERNAME_REGEX = r'^[\w.]+$'
PASSWORD_REGEX = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+{}":?><])[a-zA-Z\d!@#$%^&*()_+{}":?><]{5,35}$'


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        min_length=5,
        max_length=50,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message="user with this username already exists."
        )]
    )
    first_name = serializers.CharField(min_length=2, max_length=55)
    last_name = serializers.CharField(min_length=2, max_length=55)
    password = serializers.CharField(
        min_length=6,
        max_length=35,
        write_only=True
    )
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name',
                  'last_name', 'bio', 'password', 'confirm_password']
        extra_kwargs = {
            'email': {'required': True},
        }

    def validate_username(self, username):
        if not re.match(USERNAME_REGEX, username):
            raise ValidationError(
                "Username should only contain alphabets, numbers, underscores, or periods."
            )
        return username

    def validate(self, attrs):
        if not re.match(PASSWORD_REGEX, attrs['password']):
            raise ValidationError(
                'Password must contain at least one uppercase, one lowercase, one number, and one special character, and be between 5 and 35 characters long.')
        if attrs['password'] != attrs['confirm_password']:
            raise ValidationError("Passwords do not match.")
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    profile_photo = serializers.ImageField(use_url=True)
    email = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'profile_photo', 'email', 'username',
                  'first_name', 'last_name', 'bio', 'date_joined']
