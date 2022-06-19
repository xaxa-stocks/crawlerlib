"""Test class for most importante methods"""
import os
from unittest import TestCase
import unittest
from crawler.daily_crawler import get_and_add_asset
from crawler.daily_crawler import Crawler

password = os.environ["DB_PASSWORD"]
db_name = os.environ["DB_NAME"]
username = os.environ["DB_USERNAME"]
TICKER = "bcff11"

class TestFiis(TestCase,Crawler):
    """Test class"""

    def test_list_fiis(self):
        """Method to test the price of an asset"""

        fiis_list = Crawler.get_fii_list(self)
        self.assertIn("BCFF11", fiis_list)

    def test_get_price(self):
        """Method to test the get_price method"""
        fii_price = Crawler()._get_price(fii_ticker=TICKER)
        assert isinstance(fii_price, dict)
        assert fii_price["ticker"] == TICKER
        assert isinstance(fii_price["eod_price"], float)

    def test_run(self):
        """Test the main method"""
        test_list = [TICKER]
        get_and_add_asset(collection="daily_info", stock_list=test_list)

if __name__ == '__main__':
    unittest.main()
