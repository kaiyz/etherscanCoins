import pandas as pd
import requests
from datetime import datetime


class EtherscanScraper:
    def __init__(self, urls):
        self.urls = urls
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        cols = ['#', 'Token', 'Price',
                'Change (%)', 'Volume (24H)', 'Market Cap', 'Holders', 'dt', 'date']

        self.df_arch = pd.DataFrame(columns=cols)

    def getdata(self):
        m = len(self.urls)

        for url in self.urls:
            n = url.split('=')[-1]
            print('processing page'+n)
            r = requests.get(url, headers=self.headers)
            tx = r.text
            df = self.html_to_table(tx)
            self.df_arch = self.df_arch.append(df)

        self.df_arch['Price'] = self.df_arch['Price'].str.split(
            '\xa0Btc', expand=True)[0]

    def html_to_table(self, html):
        df = pd.read_html(html)[0]
        df['Token'] = df['Token'].str.split(
            '(', expand=True)[1].str.split(')', expand=True)[0]
        df['dt'] = datetime.now()
        df['date'] = datetime.now().date()
        return df


if __name__ == '__main__':
    today = str(datetime.now().date())
    html_prefix = 'https://etherscan.io/tokens?ps=100&p='
    urls = [html_prefix+str(i) for i in range(1, 10)]

    scraper = EtherscanScraper(urls)
    scraper.getdata()

    scraper.df_arch.to_csv('coins{}.csv'.format(today), index=False)
