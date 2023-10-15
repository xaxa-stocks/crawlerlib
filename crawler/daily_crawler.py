'''Module to get and save assets info'''
from datetime import datetime, timedelta
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from crawler.mongo import MongoConnect
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_and_add_asset(stock_list: list = None ):
    """Main method called from pod"""
    with Crawler() as crawler_session:
        crawler_session.iterate_through_items(stock_list=stock_list)
class Crawler():
    ''' Class to get fiis list, prices and save to a mongodb colletion '''

    def __init__(self):
        self.now = datetime.now()
        self.today = self.now.strftime("%Y-%m-%d")
        self.delta_last_month = self.now - timedelta(days=30)
        self.last_month = str(self.delta_last_month.strftime("%m/%y"))
        self.current_month = str(self.now.strftime("%m/%y"))
        self.session_db = self.db_session(collection="daily_info")

    def requests_session(self, url, content=None):
        """Generic requests session
        Args: url: Url to request
        Returns: bs in html parser
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; \
                 Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'}
        content = requests.get(url, headers=headers)
        return BeautifulSoup(content.text, 'html.parser')

    def close_popup(self):
        # Create a new instance of the web driver (you may need to install a browser driver such as chromedriver)
        driver = webdriver.Chrome()
        # Maximize the browser window to make it full screen
        driver.maximize_window()

        try:
            # Open a web page
            driver.get('https://fiis.com.br/lista-de-fundos-imobiliarios/')
            # Wait for the popup to appear
            # wait = WebDriverWait(driver, 15)  # Adjust the timeout as needed

            popup_element = WebDriverWait(driver, 35).until(EC.element_to_be_clickable((By.CLASS_NAME, 'popup')))
            popup_element.click()

            url = 'https://fiis.com.br/lista-de-fundos-imobiliarios/'
            page_source = driver.page_source
            soup = self.requests_session(content=page_source,url=None)

            # Handle any potential popup
            if len(driver.window_handles) > 1:
                # Switch to the popup window
                driver.switch_to.window(driver.window_handles[-1])

                # Perform actions in the popup (e.g., close it)
                # For example, you can simulate a key press, such as ESC

                # Switch back to the original window
                driver.switch_to.window(driver.window_handles[0])

        finally:
            # Close the browser window when you're done
            driver.quit()


    def get_fii_list(self):
        '''Get a list with all the available assets

        Returns:
        List with all the assets
        '''
        # close popup from site
        # self.close_popup()
        # url to retrieve the data from
        url = 'https://fiis.com.br/lista-de-fundos-imobiliarios/'
        soup = self.requests_session(url=url)
        print(soup.title)
        # Get the occurencies of class ticker to the variable rows
        rows = soup.find_all("div", {"class": "tickerBox"})
        # Defines the list to save all the fiis
        fii_table = []
        # Loop to parse and correct every fii ticker and save it to the list
        for row in rows:
            # Get the text from the Beatifulsoup variable
            fii_ticker = row.get_text()
            fii_ticker = fii_ticker.split(sep='\n')
            # Append the correct value to the list
            fii_table.append(fii_ticker[3])
        return fii_table

    def _normalize_price_string_to_float(self, price: str):
        """Converts string to float
        Args: price: string with the price
        Returns: converted float with the price
        """
        return float(price.replace('.', '').replace(',','.'))


    def _get_fii_price(self, fii_ticker: str):
        """Retrieves the price for a fii
        Args: fii_ticker: String with the fii ticker
        Returns: Float value with the price
        """
        url = f'https://statusinvest.com.br/fundos-imobiliarios/{fii_ticker.lower()}'
        soup = self.requests_session(url=url)
        asset_price = soup.find("div", attrs={"title": 'Valor atual do ativo' }).find_all('strong')
        return self._normalize_price_string_to_float(asset_price[0].text)

    def _return_fii_info(self, fii_ticker: str):
        """Returns a dict with fii info
        Args: fii_ticker: String with the fii ticker
        Returns: dict with that fii info
        """
        fii_price = {}
        fii_price = { "ticker": fii_ticker,
        "eod_price": self._get_fii_price(fii_ticker=fii_ticker),
        "day": self.now.strftime("%d/%m/%Y")}
        return fii_price

    def _get_price(self,fii_ticker: str):
        '''Get price for a given asset
        Args:
        fii_ticker: String with a fii ticker. Ex: bcff11
        Returns:
        The price of the asset
        '''
        try:
            return self._return_fii_info(fii_ticker=fii_ticker)
        except BaseException as error:
            raise error

    def db_session(self, collection: str):
        """Create a db session
        Args: collection: mongodb collection to connect
        Returns: A mongodb session
        """
        conn = MongoConnect()
        return conn.connect(collection)

    def update_fii(self, fii_to_add: dict):
        """Updates fii if exists
        Args: fii_to_add: dict with fii info
        """
        try:
            self.session_db.update_one(
                {'_id': fii_to_add['_id']},
                {'$set': {'current_price': fii_to_add['current_price']}}
            )
            print(f"Price for {fii_to_add['name']} updated!")
        except Exception as error:
            print("Fii not found")
            print(error)

    def add_item_to_db(self, fii_to_add: dict):
        """Adds a fii to DB
        Args: fii_to_add: Dict with info about the fii
        """
        try:
            fii = fii_to_add['name']
            print(f"Will add {fii} - {self.now}")
            self.session_db.replace_one({'_id': fii_to_add['_id']}, fii_to_add, upsert=True)
            print(f"Price data for {fii} added - {self.now}")
        except Exception as error:
            print(error)
            print("Something went wrong")

    def format_fii_price(self, price: float):
        """Round a float to two decimals places"""
        return round(price,2)

    def return_uid_fii(self, item: str):
        """Returns a fii uid"""
        return str(self.now.strftime("%d%m%y")) + '-' + item.lower()

    def format_item(self, item: str):
        """Receives a list with stocks and returns a formated dict with basic info

        Args: stocks_list: string with the item to be formated
        Returns: Dict with basic info
        """

        print(item)
        try:
            price_fii = self._get_price(item)
            return {
            '_id': self.return_uid_fii(item=item),
            'date': self.today,
            'name': item.lower(),
            'current_price': self.format_fii_price(price_fii["eod_price"]),
            }

        except Exception as error:
            print(error)
            return None

    def iterate_through_items(self, stock_list: list = None):
        """Go through all fii items"""

        if not stock_list:
            stock_list = self.get_fii_list()

        for item in stock_list:
            self.add_price_data_to_table(item=item)

    def find_fii(self, fii_id: str):
        """Returns a fii if existes in DB"""
        return self.session_db.find_one({"_id": fii_id})

    def add_price_data_to_table(self,item: str):
        '''Adds the price of an asset to mongo db
        Args:
        stock_list: List with the assets to get and add price
        collection: Collection in mongo db
        '''

        fii_item = self.format_item(item=item)

        try:
            print(f"Trying to add {fii_item['name']}")
            if self.find_fii(fii_id=fii_item['_id']):
                self.update_fii(fii_item)
            else:
                print("The fii doesn't exist  yet. Will add")
                self.add_item_to_db(fii_item)
        except Exception as error:
            print(f"Something went wrong {error}")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        print("Exiting class")
