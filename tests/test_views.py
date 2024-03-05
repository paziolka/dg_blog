from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from freezegun import freeze_time

from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import connection

from blog.models import Post
from blog.views import post_list, post_detail, post_new, post_edit

class ViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(title='Test Post', text='This is a test post', author=self.user)

    @freeze_time("2024-03-05 08:05:21.118404")
    def test_post_list_view(self):
        with CaptureQueriesContext(connection) as ctx:
            response = self.client.get(reverse('post_list'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'blog/post_list.html')


            # Check the SQL query generated
            expected_query = (
                f"""SELECT "blog_post"."id", "blog_post"."author_id", "blog_post"."title",
                "blog_post"."text", "blog_post"."created_date", "blog_post"."published_date"
                FROM "blog_post"
                WHERE "blog_post"."published_date" <= \'2024-03-05 08:05:21.118404\'
                ORDER BY "blog_post"."published_date" ASC """
            ).replace("\n", "").replace(" ", "")

            actual_query = ctx.captured_queries[0]['sql'].replace("\n", "").replace(" ", "")
            self.assertIn(expected_query, actual_query)

    def test_post_detail_view(self):
        with CaptureQueriesContext(connection) as ctx:
            response = self.client.get(reverse('post_detail', kwargs={'pk': self.post.pk}))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'blog/post_detail.html')

            # Check the SQL query generated
            expected_query = (
                f"""SELECT "blog_post"."id", "blog_post"."author_id", "blog_post"."title",
                "blog_post"."text", "blog_post"."created_date", "blog_post"."published_date"
                FROM "blog_post"
                WHERE "blog_post"."id" = 1
                LIMIT 21 """
            ).replace("\n", "").replace(" ", "")

            actual_query = ctx.captured_queries[0]['sql'].replace("\n", "").replace(" ", "")
            self.assertIn(expected_query, actual_query)

    def test_post_new_view_get(self):
        response = self.client.get(reverse('post_new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_edit.html')

    @freeze_time("2024-03-05 08:05:21.118404")
    def test_post_new_view_post(self):
        self.client.force_login(self.user)
        with CaptureQueriesContext(connection) as ctx:
            response = self.client.post(reverse('post_new'), {
                'title': 'Test Post',
                'text': 'This is a test post',
            })
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, reverse('post_detail', kwargs={'pk': 2}))

            expected_query = (
                f"""INSERT INTO "blog_post"
                ("author_id", "title", "text", "created_date", "published_date")
                VALUES
                (1, 'Test Post', 'This is a test post', '2024-03-05 08:05:21.118404', '2024-03-05 08:05:21.118404') """
            ).replace("\n", "").replace(" ", "")

            actual_query = ctx.captured_queries[-1]['sql'].replace("\n", "").replace(" ", "")
            self.assertIn(expected_query, actual_query)

        post = Post.objects.get(pk=2)
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.text, 'This is a test post')
        self.assertEqual(post.author, self.user)
        self.assertIsNotNone(post.published_date)

    def test_post_edit_view(self):
        with CaptureQueriesContext(connection) as ctx:
            response = self.client.get(reverse('post_edit', kwargs={'pk': self.post.pk}))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'blog/post_edit.html')

            # Check the SQL query generated
            expected_query = (
                f"""SELECT "blog_post"."id", "blog_post"."author_id", "blog_post"."title",
                "blog_post"."text", "blog_post"."created_date", "blog_post"."published_date"
                FROM "blog_post"
                WHERE "blog_post"."id" = 1
                LIMIT 21 """
            ).replace("\n", "").replace(" ", "")

            actual_query = ctx.captured_queries[0]['sql'].replace("\n", "").replace(" ", "")
            self.assertIn(expected_query, actual_query)

