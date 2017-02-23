from unittest import TestCase
from fba import Fees


class Common(TestCase):
    def test_is_media(self):
        fees = Fees()

        test = fees.is_media("Video Games")

        self.assertEqual(test, True)
