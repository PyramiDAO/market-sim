
import pandas as pd
import ssl


class DataFeed:

    def __init__(self, source, crypto, interval):
        self.source = source
        self.crypto = crypto
        self.interval = interval
        self.raw_data = pd.DataFrame()
        self.access_url = f'https://www.cryptodatadownload.com/cdd/' \
                          f'{self.source}_{self.crypto}_{self.interval}.csv'
        print(f'[+] Data can be found at {self.access_url}')

    def load_to_df(self):
        ssl._create_default_https_context = ssl._create_unverified_context
        print(f"[+] Loading url ... {self.access_url}")
        df = pd.read_csv(self.access_url, skiprows=1)
        df = df.drop(columns=["date"])
        df["unix"] = pd.to_numeric(df["unix"])
        df["unix"] = df["unix"].apply(lambda x: x / 1000 if x > 1000000000000 else x)
        df = df[["unix", "symbol", "open", "high", "low", "close"]]
        df = df.set_index("unix")
        df = df[~df.index.duplicated(keep='first')]  # remove duplicated values in index (problem in original data)
        df = df.reset_index()
        self.raw_data = df
        return self.raw_data

    def get_market_levels(self, _unix, _type):
        data = self.raw_data[self.raw_data.index == _unix]
        return data[_type].values
