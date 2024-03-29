"""Sanitizer class to add daily price to history table"""
from datetime import timedelta
from crawler.daily_crawler import Crawler
from crawler.mongo import MongoConnect


class Sanitizer(Crawler):
    """"
    Class to get last stock close and save it to time-series collection. Extends Crawler class
    """

    def retrieve_fii(self,stock_list: list):
        """"
        Method to retrieve stock close from the day before and save it to time-series collection.
        Args:
        stock_list: A variable (type:list) with the tickers for each fii to apply the method
        """
        yesterday = self.now - timedelta(days=1)
        conn_daily = MongoConnect().connect("daily_info")
        conn_history = MongoConnect().connect("time-series")
        uid_base = str(yesterday.strftime("%d%m%y")) + '-'
        for item in stock_list:
            uid_fii = uid_base + item.lower()
            try:
                if conn_daily.find_one({"_id": uid_fii}):
                    fii_info = conn_daily.find_one({"_id": uid_fii})
                    print(f"Data found for {item}")
                    if conn_history.find_one({"name": item}):
                        print("Adding stock data in historical collection")
                        conn_history.update_one(
                            {"name": item},
                            {"$addToSet":
                            { "historical":
                            {"Date": yesterday, "Close": fii_info["current_price"]} }})
                else:
                    print("No data found for yesterday. Exiting...")
            except Exception as error:
                print(error)
                print("Something went wrong")
