from django.test import TestCase
from django.urls import resolve
from django.test.client import RequestFactory

from blog import views

class UrlTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_post_list_url(self):
        url = resolve('/')
        self.assertEqual(url.func, views.post_list)
        # print(url)
        # structure returned by resolve():
        # ResolverMatch(
        #     func=blog.views.post_detail,
        #     args=(), kwargs={'pk': 1},
        #     url_name=post_detail,
        #     app_names=[],
        #     namespaces=[],
        #     route=post/<int:pk>/
        # )
        self.assertEqual(url.url_name, 'post_list')

    def test_post_detail_url(self):
        url = resolve('/post/1/')
        self.assertEqual(url.func, views.post_detail)
        self.assertEqual(url.url_name, 'post_detail')

    def test_post_new_url(self):
        url = resolve('/post/new/')
        self.assertEqual(url.func, views.post_new)
        self.assertEqual(url.url_name, 'post_new')

    def test_post_edit_url(self):
        url = resolve('/post/1/edit/')
        self.assertEqual(url.func, views.post_edit)
        self.assertEqual(url.url_name, 'post_edit')
