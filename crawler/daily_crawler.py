'''Module to get and save assets info'''
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from crawler.mongo import MongoConnect


def get_and_add_asset(collection: str, stock_list: list = None ):
    """Main method called from pod"""
    with Crawler() as crawler_session:
        crawler_session.add_price_data_to_table(collection=collection, stock_list=stock_list)

class Crawler():

    ''' Class to get fiis list, prices and save to a mongodb colletion '''

    # Function to retrieve a list of fiis and save it to dynamoDB


    def __init__(self):
        self.now = datetime.now()
        self.today = self.now.strftime("%Y-%m-%d")
        self.delta_last_month = self.now - timedelta(days=30)
        self.last_month = str(self.delta_last_month.strftime("%m/%y"))
        self.current_month = str(self.now.strftime("%m/%y"))

    def get_fii_list(self):
        '''Get a list with all the available assets

        Returns:
        List with all the assets
        '''
        # url to retrieve the data from
        url = 'https://fiis.com.br/lista-de-fundos-imobiliarios/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; \
                 Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'}
        content = requests.get(url, headers=headers)
        soup = BeautifulSoup(content.text, 'html.parser')
        # Get the occurencies of class ticker to the variable rows
        rows = soup.find_all("span", {"class": "ticker"})
        # Defines the list to save all the fiis
        fii_table = []
        # Loop to parse and correct every fii ticker and save it to the list
        for row in rows:
            # Get the text from the Beatifulsoup variable
            fii_ticker = row.get_text()
            fii_ticker = fii_ticker.split(sep='"div", {"class": "stylelistrow"}')
            # Append the correct value to the list
            fii_table.append(fii_ticker[0])
        return fii_table


    def _get_price(self,fii_ticker: str):
        '''Get price for a given asset
        Args:
        fii_ticker: String with a fii ticker. Ex: bcff11

        Returns:
        The price of the asset

        '''
        fii_price = {}
        base_url = 'https://statusinvest.com.br/fundos-imobiliarios/'
        url = base_url + fii_ticker.lower()
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; \
                 Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'}
        content = requests.get(url, headers=headers)
        soup = BeautifulSoup(content.text, 'html.parser')
        try:
            for quote in soup.find('div', attrs={'title': 'Valor atual do ativo'}).find_all('strong'):
                quote = quote.text
                quote = quote.replace('.', '').replace(',','.')
            fii_price["ticker"] = fii_ticker
            fii_price["eod_price"] = float(quote)
            fii_price["day"] = self.now.strftime("%d/%m/%Y")
            return fii_price
        except BaseException:
            return "No return for this fii"

    def add_price_data_to_table(self,collection: str,stock_list: list = None):
        '''Adds the price of an asset to mongo db
        
        Args:
        stock_list: List with the assets to get and add price
        collection: Collection in mongo db
        '''
        if not stock_list:
            stock_list = self.get_fii_list()

        for item in stock_list:
            print(item)
            try:
                price_fii = self._get_price(item)

                uid_base = str(self.now.strftime("%d%m%y")) + '-'
                uid_fii = uid_base + item.lower()

                date = self.today
                name = price_fii["ticker"].lower()
                price = round(price_fii["eod_price"],2)

                conn = MongoConnect()
                conn = conn.connect(collection)
                 
                if conn.find_one({"_id": uid_fii}):
                    conn.update_one({'_id': uid_fii}, {'$set': {'current_price': price}})
                    print(f"Price for {item} updated!")
                else:
                    print(f"Will add {item} - {self.now}")
                    item = {
                        '_id': uid_fii,
                        'date': date,
                        'name': name,
                        'current_price': price,
                    }
                    
                    conn.replace_one({'_id': uid_fii}, item, upsert=True)

                    print(f"Price data for {name} added - {self.now}")
            except Exception as error:
                print(error)
                print(f"There is no info for this fii - {self.now}")
    def __enter__(self):
        return self
        
    # FIXME - IMPLEMENT
    # def __exit__(self, *args):
    #     if 
    #     pass
    #     # if self.client:
    #     #     self.client.close()
