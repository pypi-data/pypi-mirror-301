from multi_time_series_connectedness.connectedness import Connectedness
import pandas as pd
import pickle


class RollingConnectedness:

    def __init__(self, data, max_lag, data_periods):
        # to variable to run this module
        self.data = data
        self.max_lag = max_lag
        self.data_periods = data_periods
        self.name = [col for col in data.columns if col != 'time'] + ['all']

        # save the calculated connectedness
        self.data_list = None
        self.rolling_connectedness = None
        self.accuracy_list = None

    def divide_timeseries_volatilities(self):
        dataframe = self.data
        periods = self.data_periods

        data_list = []

        for i in range(len(dataframe)):

            # get divided data
            data = dataframe.iloc[i: periods+i]
            if len(data) < periods:
                break

            # get the start and end date
            data = data.reset_index(drop=True)

            # add to data_list
            data_list.append(data)

        self.data_list = data_list

    def calculate(self, store_result_at, callback_after_one_connectedness=None):
        restructured_connectedness_timeseries = pd.DataFrame()
        for data in self.data_list:
            start_date = data["time"].iloc[0]
            end_date = data["time"].iloc[self.data_periods-1]
            period = start_date + " ~ " + end_date
            print("calculate connectedness for period, %s with data between %s"
                  % (end_date, period))

            conn = Connectedness(data)
            conn.calculate_full_connectedness()
            conn.rename_table(self.name)
            conn.flatten_connectedness()

            restructured_connectedness = conn.restructure_connectedness
            if callback_after_one_connectedness:
                callback_after_one_connectedness(restructured_connectedness)
            restructured_connectedness_timeseries = pd.concat(
                [restructured_connectedness_timeseries, restructured_connectedness], 
                ignore_index=True
            )

        self.rolling_connectedness = restructured_connectedness_timeseries

        with open(store_result_at, 'wb') as f:
            pickle.dump(self.rolling_connectedness, f)

    def plot_rolling():
        pass
