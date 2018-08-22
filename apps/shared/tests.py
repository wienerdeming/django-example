# Python
import os
import json
import pycodestyle

# Django
from django.test import TestCase
from django.conf import settings

# REST framework
from rest_framework import status
from rest_framework.test import APITestCase

# Project
from .utils import get_files_for_checking, reverse


class ViewSetTestCase(object):
    def _list(self, filters=None, kwargs=None):
        filters = filters or {}
        url = reverse(self.list, filters, kwargs=kwargs)
        response = self.client.get(url)
        return response

    def _retrieve(self, kwargs):
        url = reverse(self.detail, kwargs=kwargs)
        response = self.client.get(url)
        return response

    def _create(self, data=None, kwargs=None):
        data = data or {}
        url = reverse(self.list, kwargs=kwargs)
        response = self.client.post(url, data)
        return response

    def _update(self, kwargs, data=None):
        data = data or {}
        url = reverse(self.detail, kwargs=kwargs)
        response = self.client.put(url, data)
        return response

    def _destroy(self, kwargs):
        url = reverse(self.detail, kwargs=kwargs)
        response = self.client.delete(url)
        return response


class PyCodeStyleTest(TestCase):
    def test_check_files(self):
        """Test that we conform to PEP-8."""
        app_dir = os.path.join(settings.BASE_DIR, 'apps')
        source = get_files_for_checking(app_dir)

        total_errors = 0
        messages = ''
        for item in source:
            style = pycodestyle.StyleGuide(quite=True)
            result = style.check_files([item])
            if result.total_errors:
                total_errors += result.total_errors
                message = '%s:%s:%s %s' % (
                    item,
                    result.counters['physical lines'],
                    result.counters['logical lines'],
                    json.dumps(result.messages, sort_keys=True, indent=4)
                )
                messages += '\n' + message

        self.assertEqual(0, total_errors, messages)


class DocumentTest(APITestCase):
    def test_documentation(self):
        response = self.client.get('/', format='html')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
