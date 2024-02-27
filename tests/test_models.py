from django.test import TestCase

from django.contrib.auth.models import User
from blog.models import Post
from django.db import models

class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='testuser', password='12345')
        Post.objects.create(title='Title', text='Kiciuś Cat ipsum', author=test_user)

    def test_post_instance(self):
        post = Post.objects.get(id=1)
        self.assertEqual(post.title, "Title")
        self.assertEqual(post.text, "Kiciuś Cat ipsum")
        self.assertEqual(post.author, User.objects.get(id=1))

    def test_title_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_text_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('text').verbose_name
        self.assertEqual(field_label, 'text')

    def test_title_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_object_fields(self):
        self.assertIsInstance(Post._meta.get_field("author"), models.ForeignKey)
        self.assertIsInstance(Post._meta.get_field("title"), models.CharField)
        self.assertIsInstance(Post._meta.get_field("text"), models.TextField)
        self.assertIsInstance(Post._meta.get_field("created_date"), models.DateTimeField)
        self.assertIsInstance(Post._meta.get_field("published_date"), models.DateTimeField)

    def test_object_name_is_title(self):
        post = Post.objects.get(id=1)
        expected_object_name = post.title
        self.assertEqual(str(post), expected_object_name)

    def test_publish(self):
        post = Post.objects.get(id=1)
        self.assertFalse(post.published_date)
        post.publish()
        self.assertTrue(post.published_date)
