from django.test import TestCase
from blog.forms import PostForm
from django import forms

class PostFormTest(TestCase):
    def test_form_fields(self):
        # Properties of the form fields
        post_form = PostForm({
            'title': 'Title',
            'text': 'Text',
        })

        self.assertEqual(post_form.fields['title'].widget.input_type, 'text')
        self.assertTrue(isinstance(post_form.fields['title'], forms.CharField))
        self.assertTrue(isinstance(post_form.fields['text'], forms.CharField))

        # Test invalid inputs
        post_form = PostForm({
            'title': '',
            'text': 'Valid Text',
        })
        self.assertFalse(post_form.is_valid())
        self.assertNotIn('title', post_form.cleaned_data)

        post_form = PostForm({
            'title': '*' * 201,
            'text': 'Valid Text',
        })
        self.assertFalse(post_form.is_valid())
        self.assertNotIn('title', post_form.cleaned_data)

        post_form = PostForm({
            'title': 'Valid Title',
            'text': '',
        })
        self.assertFalse(post_form.is_valid())
        self.assertNotIn('text', post_form.cleaned_data)

        # Test valid inputs
        post_form = PostForm({
            'title': 'Title',
            'text': 'Text',
        })
        self.assertTrue(post_form.is_valid())
        cleaned_data = post_form.cleaned_data
        self.assertEqual(cleaned_data['title'], 'Title')
        self.assertEqual(cleaned_data['text'], 'Text')
