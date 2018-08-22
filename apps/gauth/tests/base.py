# Django
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

# Rest Framework
from rest_framework.authtoken.models import Token

# Project
from ..models import User

TEST_USER1 = 'test1@example.com'
TEST_USER2 = 'test2@example.com'
TEST_USER3 = 'test3@example.com'
TEST_USER4 = 'test4@example.com'
CURRENT_PASSWORD = 'current_password_123'
NEW_PASSWORD = 'new_password_123'
WRONG_PASSWORD = 'wrong_password_123'
WRONG_TOKEN = '11111111-2222-3333-4444-555555555555'


def test_get_token(username=TEST_USER1):
    user = User.objects.get(username=username)
    token = Token.objects.get_or_create(user=user)

    return 'Token ' + token[0].key


class AuthTestCase(object):
    def _get_user(self, username):
        return User.objects.get(username=username)

    def _get_token(self, user):
        token = Token.objects.get_or_create(user=user)
        return 'Token ' + token[0].key

    def _get_perm(self, content_type, action):
        codename = '%s_%s' % (action, content_type.model, )
        perm = Permission.objects.get(
            content_type=content_type,
            codename=codename)

        return perm

    def _add_perm(self, model, action):
        content_type = ContentType.objects.get_for_model(model)
        user = self._get_user(TEST_USER2)
        perm = self._get_perm(content_type, action)
        user.user_permissions.add(perm)

    def _auth_admin(self):
        user = self._get_user(TEST_USER1)
        token = self._get_token(user)
        self.client.credentials(HTTP_AUTHORIZATION=token)

    def _auth_non_admin(self):
        user = self._get_user(TEST_USER2)
        token = self._get_token(user)
        self.client.credentials(HTTP_AUTHORIZATION=token)

    def _auth_non_owner(self):
        user = self._get_user(TEST_USER4)
        token = self._get_token(user)
        self.client.credentials(HTTP_AUTHORIZATION=token)
