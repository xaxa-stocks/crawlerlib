"""Sanitizer class to add daily price to history table"""
from datetime import timedelta
from crawler.daily_crawler import Crawler
from crawler.mongo import MongoConnect


class Sanitizer():
    """"
    Class to get last stock close and save it to time-series collection. Extends Crawler class
    """

    def __init__(self, collection_daily: str = "daily_info", collection_history: str = "time-series") :
        crawler = Crawler()
        self.day_before = crawler.now - timedelta(days=1)
        self.conn_daily = MongoConnect().connect(collection_daily)
        self.conn_history = MongoConnect().connect(collection_history)
        self.uid_base = str(self.day_before.strftime("%d%m%y")) + '-'



    def retrieve_fii(self,stock_list: list):
        """"
        Method to retrieve stock close from the day before and save it to time-series collection.
        Args:
        stock_list: A variable (type:list) with the tickers for each fii to apply the method
        """
        for item in stock_list:
            uid_fii = self.uid_base + item.lower()
            try:
                if self.conn_daily.find_one({"_id": uid_fii}):
                    fii_info = self.conn_daily.find_one({"_id": uid_fii})
                    print(f"Data found for {item}")
                    if self.conn_history.find_one({"name": item}):
                        print("Adding stock data in historical collection")
                        self.conn_history.update_one(
                            {"name": item},
                            {"$addToSet":
                            { "historical":
                            {"Date": self.yesterday, "Close": fii_info["current_price"]} }})
                else:
                    print("No data found for yesterday. Exiting...")
            except Exception as error:
                print(error)
                print("Something went wrong")
