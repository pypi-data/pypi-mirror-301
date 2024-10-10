import pickle
import pandas as pd
import numpy as np
from .data_processor import load_files


class Volatility:
    def __init__(self, n=2):
        self.n = n

    def yang_zhang_volatility(self, data, name):
        """
        :param data: a list with Open, High, Low, Close price
        :param name: the name of the volatility column
        :return: A DataFrame with time and volatility data
        """
        # define required variables
        o_c = (data['Open'] / data['Close'].shift(1)).apply(np.log)
        c_o = (data['Close'] / data['Open']).apply(np.log)
        h_o = (data['High'] / data['Open']).apply(np.log)
        l_o = (data['Low'] / data['Open']).apply(np.log)

        # overnight volatility
        vo = o_c.rolling(window=self.n).apply(np.var, raw=True)

        # today(open to close) volatility
        vt = c_o.rolling(window=self.n).apply(np.var, raw=True)

        # rogers-satchell volatility
        rs_fomula = h_o * (h_o - c_o) + l_o * (l_o - c_o)
        rs = rs_fomula.rolling(window=self.n, center=False).sum() * (1.0 / self.n)

        # super parameter
        k = 0.34 / (1 + (self.n + 1) / (self.n - 1))

        # yang-zhang
        result = (vo + k * vt + (1 - k) * rs).apply(np.sqrt)

        result_df = result.to_frame(name=name)

        return pd.concat([data['time'], result_df], axis=1)

    def price_data_to_volatility(self, datasets):
        volatilities = None
        for key, value in datasets.items():
            volatility = self.yang_zhang_volatility(value, key)
            if volatilities is None:
                volatilities = volatility
            else:
                volatilities = volatilities.merge(volatility, on='time', how='outer')

        return volatilities

    def calculate(self, start_at, end_at, directory, save_path=None):
        datasets = load_files(directory, start_at, end_at)
        volatilities = self.price_data_to_volatility(datasets)

        with open(save_path, 'wb') as f:
            pickle.dump(volatilities, f)
