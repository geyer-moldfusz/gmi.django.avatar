from django.contrib.auth.models import User
from django.test import TestCase
from django.template import Context, Template

class AvatarTemplateTagsTestCase(TestCase):

    def setUp(self):
        self.john = User.objects.create_user(
            'john', 'john@example.com', 'apassword')

    def test_avatar_url_valid(self):
        template = Template("{% load avatar_tags %}{{ user|avatar_url }}")
        rendered = template.render(Context(dict(user=self.john)))
        self.assertIn('/static/avatar/160x160/none', rendered)

    def test_avatar_url_resolution(self):
        template = Template("{% load avatar_tags %}{{ user|avatar_url:320 }}")
        rendered = template.render(Context(dict(user=self.john)))
        self.assertIn('/static/avatar/320x320/none', rendered)

    def test_avatar_url_html_injection(self):
        template = Template(
            "{% load avatar_tags %}{{ user|avatar_url:'<html>' }}")
        rendered = template.render(Context(dict(user=self.john)))
        self.assertNotIn('<html>', rendered)
