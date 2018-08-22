# Rest Framework
from rest_framework import status
from rest_framework.test import APITestCase

# Project
from apps.shared.utils import reverse
from apps.shared import messages as msg
from .base import AuthTestCase, TEST_USER1, CURRENT_PASSWORD

NEW_PASSWORD = 'abc0987654321'
INVALID_PASSWORD = '123'


class ChangePasswordTest(APITestCase, AuthTestCase):
    fixtures = ['user.yaml']

    url = 'apps.gauth:change-password'

    def _auth(self, data):
        url = reverse('apps.gauth:auth')
        return self.client.post(url, data)

    def _change_password(self, password):
        self._auth_admin()
        url = reverse(self.url)
        return self.client.put(url, {'password': password})

    def test_change_password_invalid(self):
        response = self._change_password(INVALID_PASSWORD)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['password'][0],
                         msg.INVALID_PASSWORD_LENGTH)
        self.assertEqual(response.data['password'][1],
                         msg.INVALID_PASSWORD_ENTIRELY_NUMERIC)

    def test_change_password(self):
        # Auth with current password
        data = {'username': TEST_USER1, 'password': CURRENT_PASSWORD}
        auth_response = self._auth(data)
        self.assertEqual(auth_response.status_code, status.HTTP_200_OK)

        # Change password
        change_response = self._change_password(NEW_PASSWORD)
        self.assertNotEqual(CURRENT_PASSWORD, NEW_PASSWORD)
        self.assertEqual(change_response.status_code, status.HTTP_200_OK)

        # Auth with new password
        data = {'username': TEST_USER1, 'password': NEW_PASSWORD}
        auth_response = self._auth(data)
        self.assertEqual(auth_response.status_code, status.HTTP_200_OK)
