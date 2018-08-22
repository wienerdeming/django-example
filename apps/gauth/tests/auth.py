# Django
from django.utils.translation import ugettext_lazy as _

# Rest Framework
from rest_framework import status
from rest_framework.test import APITestCase

# Project
from apps.shared.utils import reverse
from .base import TEST_USER1, CURRENT_PASSWORD, WRONG_TOKEN


class AuthTest(APITestCase):
    fixtures = ['user.yaml']

    def _auth(self, data):
        url = reverse('apps.gauth:auth')
        return self.client.post(url, data, format='json')

    def _me(self, token):
        url = reverse('apps.gauth:me')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        return self.client.get(url)

    def test_auth_success(self):
        data = {'username': TEST_USER1, 'password': CURRENT_PASSWORD}
        response = self._auth(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_auth_confirm(self):
        data = {'username': TEST_USER1, 'password': CURRENT_PASSWORD}
        token = self._auth(data).data['token']

        response = self._me(token)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], TEST_USER1)

    def test_auth_fail(self):
        data = {'username': TEST_USER1, 'password': WRONG_TOKEN}
        response = self._auth(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_auth_fail_empty(self):
        response = self._auth({})
        errors = response.data

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(errors['username'][0], _('This field is required.'))
        self.assertEqual(errors['password'][0], _('This field is required.'))

    # def test_permissions(self):
    #     data = {'username': TEST_USER1, 'password': CURRENT_PASSWORD}
    #     token = self._auth(data).data['token']
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    #
    #     url = url_with_params('apps.gauth:permissions-list')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
