import os
from unittest import TestCase
import unittest

password = os.environ["DB_PASSWORD"] = ""
db_name = os.environ["DB_NAME"] = ""
username = os.environ["DB_USERNAME"] = ""
ticker = "bcff11"

from crawler.daily_crawler import Crawler

class TestFiis(TestCase,Crawler):


    def test_list_fiis(self):

        fiis_list = Crawler.get_fii_list(self)
        self.assertIn("BCFF11", fiis_list)

    def test_get_price(self):
        fii_price = Crawler.__get_price__(self,ticker)
        assert type(fii_price) is dict 
        assert fii_price["ticker"] == ticker
        assert type(fii_price["eod_price"]) is float
        

if __name__ == '__main__':
    unittest.main()