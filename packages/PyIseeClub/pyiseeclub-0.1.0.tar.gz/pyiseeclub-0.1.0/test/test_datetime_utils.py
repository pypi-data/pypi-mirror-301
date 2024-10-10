# -*- coding: utf-8 -*-
from isee_club.datetime_utils import current_date
import unittest


class TestDateFunction(unittest.TestCase):
    def test_datetime(self):
        self.assertEqual(current_date(), "2023-09-30")


if __name__ == '__main__':
    unittest.main()
