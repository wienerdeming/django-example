# REST framework
from rest_framework.test import APITestCase
from rest_framework import status

# Project
from apps.shared.utils import timezone_fix
from apps.shared.tests import ViewSetTestCase
from apps.gauth.tests import TEST_USER1


class NewsPublicTest(APITestCase, ViewSetTestCase):
    fixtures = ['user.yaml', 'news.yaml']

    list = 'apps.news:news-public-list'
    detail = 'apps.news:news-public-detail'

    def test_list(self):
        response = self._list()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

    def test_pagination(self):
        response = self._list({'page': 2, 'page_size': 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'News title 2')

    def test_search(self):
        response = self._list({'search': 'News title 4'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'News title 4')

    def test_author_filter(self):
        response = self._list({'author': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

        response = self._list({'author': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_published_date_filter(self):
        filters = {
            'published_date_after': '2018-01-03',
            'published_date_before': '2018-01-03'
        }
        response = self._list(filters)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'News title 4')

    def test_detail(self):
        response = self._retrieve({'pk': 1})
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['title'], 'News title 1')
        self.assertEqual(data['desc'], 'News desc 1')
        self.assertEqual(data['content'], 'News content 1')
        self.assertEqual(data['author']['id'], 1)
        self.assertEqual(data['author']['name'], TEST_USER1)
        self.assertEqual(str(data['published_date']),
                         timezone_fix('2018-01-01T00:00:00+00:00'))
        self.assertEqual(len(response.data.items()), 6)
