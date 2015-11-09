from django.test import TestCase
import gmi.django.avatar.utils as utils


class UtilsTestCase(TestCase):

    def test_hash_email(self):
        self.assertEqual(
            utils.hash_email('foo@bar.baz'),
            '80c66bdd90ae7fd4378cef780422fe428ee7fb526301f7b236113c4ece3be146')
