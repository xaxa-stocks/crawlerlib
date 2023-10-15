"""Test class for most importante methods"""
import os
from unittest import TestCase
import unittest
from crawler.daily_crawler import get_and_add_asset
from crawler.daily_crawler import Crawler
from crawler.sanitizer import Sanitizer

class TestFiis(TestCase):
    """Test class"""

    @classmethod
    def setUpClass(cls):
        cls.TICKER = "bcff11"
        cls.crawler = Crawler()
        cls.one_item = [cls.TICKER]
        cls.several_items = ["hglg11", "recr11"]
        cls.sanitizer = Sanitizer()
        # os.environ["DB_USERNAME"] = "test"
        # os.environ["DB_PASSWORD"] = "test"
        # os.environ["DB_NAME"] = "test"

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

    def test_add_one_item(self):
        """Test the main method"""
        get_and_add_asset(stock_list=self.one_item)

    def test_add_several_items(self):
        """Test the main method"""
        get_and_add_asset(stock_list=self.several_items)

    def test_sanitizer_retrieve(self):
        self.sanitizer.retrieve_fii(stock_list=["bcff11"])

if __name__ == '__main__':
    password = os.environ["DB_PASSWORD"]
    db_name = os.environ["DB_NAME"]
    username = os.environ["DB_USERNAME"]
    unittest.main()
