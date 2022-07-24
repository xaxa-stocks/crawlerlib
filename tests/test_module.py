"""Test class for most importante methods"""
import os
from unittest import TestCase
import unittest
from crawler.daily_crawler import get_and_add_asset
from crawler.daily_crawler import Crawler

class TestFiis(TestCase):
    """Test class"""

    @classmethod
    def setUpClass(cls):
        cls.TICKER = "bcff11"
        cls.crawler = Crawler()

    def test_list_fiis(self):
        """Method to test the price of an asset"""

        fiis_list = self.crawler.get_fii_list()
        self.assertIn("BCFF11", fiis_list)

    def test_normalize_string_to_float(self):
        price = self.crawler._normalize_price_string_to_float(price="1.000,9")
        assert isinstance(price, float)
        self.assertEqual(price, 1000.9)
    
    def test_format_fii_price(self):
        price = self.crawler.format_fii_price(10.9443335)
        assert isinstance(price, float)
        self.assertEqual(price, 10.94)
    
    def test_return_uid_fii(self):
        uid = self.crawler.return_uid_fii(item=self.TICKER)
        self.assertEqual(uid, f'{self.crawler.now.strftime("%d%m%y")}-bcff11')

    def test_get_price(self):
        """Method to test the get_price method"""
        fii_price = self.crawler._get_price(fii_ticker=self.TICKER)
        assert isinstance(fii_price, dict)
        assert fii_price["ticker"] == self.TICKER
        assert isinstance(fii_price["eod_price"], float)

    def test_run(self):
        """Test the main method"""
        test_list = [self.TICKER]
        get_and_add_asset(stock_list=test_list)

if __name__ == '__main__':
    password = os.environ["DB_PASSWORD"]
    db_name = os.environ["DB_NAME"]
    username = os.environ["DB_USERNAME"]
    unittest.main()
