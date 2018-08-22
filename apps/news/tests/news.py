# REST framework
from rest_framework.test import APITestCase
from rest_framework import status

# Project
from apps.shared import messages as msg
from apps.shared.utils import timezone_fix
from apps.shared.tests import ViewSetTestCase
from apps.gauth.tests import AuthTestCase
from ..models import News


class NewsCrudTest(APITestCase, ViewSetTestCase, AuthTestCase):
    fixtures = ['user.yaml', 'news.yaml']

    list = 'apps.news:news-list'
    detail = 'apps.news:news-detail'

    def setUp(self):
        self._auth_admin()

    def test_unauth(self):
        self.client.credentials()

        response = self._list()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self._retrieve({'pk': 1})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self._create()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self._update({'pk': 1})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self._destroy({'pk': 1})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_perm_list(self):
        self._auth_non_admin()

        response = self._list()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self._add_perm(News, 'list')

        response = self._list()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list(self):
        response = self._list()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 4)

    def test_pagination(self):
        response = self._list({'page': 2, 'page_size': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'News title 3')

    def test_ordering_id(self):
        # Ordering asc
        response = self._list({'ordering': 'id'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'News title 1')

        # Ordering desc
        response = self._list({'ordering': '-id'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'News title 4')

    def test_ordering_title(self):
        # Ordering asc
        response = self._list({'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'News title 1')

        # Ordering desc
        response = self._list({'ordering': '-title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'News title 4')

    def test_search(self):
        response = self._list({'search': 'News title 4'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'News title 4')

    def test_created_date_filter(self):
        filters = {
            'created_date_after': '2018-01-02',
            'created_date_before': '2018-01-02'
        }
        response = self._list(filters)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'News title 4')

    def test_published_date_filter(self):
        filters = {
            'published_date_after': '2018-01-03',
            'published_date_before': '2018-01-03'
        }
        response = self._list(filters)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'News title 4')

    def test_author_filter(self):
        response = self._list({'author': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 4)

        response = self._list({'author': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_is_active_filter(self):
        response = self._list({'is_active': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

        response = self._list({'is_active': False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_perm_create(self):
        data = {
            'title': 'News title',
            'desc': 'News description',
            'content': 'News content',
            'is_active': True,
            'published_date': '2018-01-01 00:00:00+00:00'
        }
        self._auth_non_admin()

        response = self._create(data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self._add_perm(News, 'create')

        response = self._create(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_success(self):
        data = {
            'title': 'News title',
            'desc': 'News description',
            'content': 'News content',
            'is_active': True,
            'published_date': '2018-01-01 00:00:00+00:00'
        }
        response = self._create(data)
        news = News.objects.get(pk=response.data['id'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(news.title, data['title'])
        self.assertEqual(news.desc, data['desc'])
        self.assertEqual(news.content, data['content'])
        self.assertEqual(news.is_active, data['is_active'])
        self.assertEqual(str(news.published_date), data['published_date'])

    def test_create_without_required_fields(self):
        response = self._create()
        errors = response.data

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(errors['title'][0], msg.INVALID_REQUIRED)
        self.assertEqual(errors['desc'][0], msg.INVALID_REQUIRED)
        self.assertEqual(errors['content'][0], msg.INVALID_REQUIRED)
        self.assertEqual(errors['published_date'][0], msg.INVALID_REQUIRED)

    def test_create_with_empty_data(self):
        data = {
            'title': '',
            'desc': '',
            'content': '',
            'is_active': True,
            'published_date': ''
        }
        response = self._create(data)
        errors = response.data

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(errors['title'][0], msg.INVALID_BLANK)
        self.assertEqual(errors['desc'][0], msg.INVALID_BLANK)
        self.assertEqual(errors['content'][0], msg.INVALID_BLANK)
        self.assertEqual(errors['published_date'][0], msg.INVALID_DATETIME)

    def test_create_with_wrong_data(self):
        data = {
            'title': {},
            'desc': {},
            'content': {},
            'is_active': '',
            'published_date': 0
        }
        response = self._create(data)
        errors = response.data

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(errors['title'][0], msg.INVALID_STRING)
        self.assertEqual(errors['desc'][0], msg.INVALID_STRING)
        self.assertEqual(errors['content'][0], msg.INVALID_STRING)
        self.assertEqual(errors['is_active'][0], msg.INVALID_BOOLEAN %
                         data['is_active'])
        self.assertEqual(errors['published_date'][0], msg.INVALID_DATETIME)

    def test_perm_retrieve(self):
        self._auth_non_admin()

        response = self._retrieve({'pk': 1})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self._add_perm(News, 'retrieve')

        response = self._retrieve({'pk': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        response = self._retrieve({'pk': 1})
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['title'], 'News title 1')
        self.assertEqual(data['desc'], 'News desc 1')
        self.assertEqual(data['content'], 'News content 1')
        self.assertEqual(data['is_active'], True)
        self.assertEqual(str(data['published_date']),
                         timezone_fix('2018-01-01T00:00:00+00:00'))
        self.assertEqual(len(response.data.items()), 9)

    def test_perm_update(self):
        data = {
            'title': 'News title',
            'desc': 'News description',
            'content': 'News content',
            'is_active': True,
            'published_date': '2018-01-01 00:00:00+00:00'
        }
        self._auth_non_admin()

        response = self._update({'pk': 1}, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self._add_perm(News, 'update')

        response = self._update({'pk': 1}, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        data = {
            'title': 'News title',
            'desc': 'News description',
            'content': 'News content',
            'is_active': True,
            'published_date': '2018-01-01 00:00:00+00:00'
        }

        response = self._update({'pk': 1}, data)
        news = News.objects.get(id=1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(news.title, data['title'])
        self.assertEqual(news.desc, data['desc'])
        self.assertEqual(news.content, data['content'])
        self.assertEqual(news.is_active, data['is_active'])
        self.assertEqual(str(news.published_date), data['published_date'])

    def test_perm_destroy(self):
        self._auth_non_admin()

        response = self._destroy({'pk': 1})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self._add_perm(News, 'destroy')

        response = self._destroy({'pk': 1})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_destroy(self):
        # Delete
        response = self._destroy({'pk': 1})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify delete
        response = self._retrieve({'pk': 1})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
