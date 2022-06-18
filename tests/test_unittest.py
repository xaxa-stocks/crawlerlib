import os
from unittest import TestCase
import unittest
from crawler.daily_crawler import get_and_add_asset

password = os.environ["DB_PASSWORD"]
db_name = os.environ["DB_NAME"]
username = os.environ["DB_USERNAME"]
ticker = "bcff11"

from crawler.daily_crawler import Crawler

class TestFiis(TestCase,Crawler):


    def test_list_fiis(self):

        fiis_list = Crawler.get_fii_list(self)
        self.assertIn("BCFF11", fiis_list)

    def test_get_price(self):
        fii_price = Crawler()._get_price(fii_ticker=ticker)
        assert type(fii_price) is dict 
        assert fii_price["ticker"] == ticker
        assert type(fii_price["eod_price"]) is float

    def test_run(self):
        test_list = [ticker]
        get_and_add_asset(collection="daily_info", stock_list=test_list)
        

if __name__ == '__main__':
    unittest.main()