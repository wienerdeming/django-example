# Django
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password

# REST framework
from rest_framework import serializers
# Project
from apps.gauth.models import User


class AuthUserSerializer(serializers.Serializer):
    username = serializers.CharField(label=_('Username'))
    password = serializers.CharField(
        label=_('Password'), style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers. \
                        ValidationError(msg, code='authorization')
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=255, validators=[validate_password], write_only=True)

    class Meta:
        model = User
        fields = ('id', 'password', )

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'first_name', )
        read_only_fields = ('modified_date', 'created_date', )
