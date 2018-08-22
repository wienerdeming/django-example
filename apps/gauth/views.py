# REST framework
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import (RetrieveAPIView, UpdateAPIView, )

# Project
from .models import User
from .serializers import (
    AuthUserSerializer, MeSerializer, ChangePasswordSerializer,
)


class AuthUserView(ObtainAuthToken):
    serializer_class = AuthUserSerializer
    renderer_classes = (renderers.JSONRenderer, renderers.AdminRenderer)


class MeUserView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = MeSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
