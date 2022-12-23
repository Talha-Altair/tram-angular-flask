import pandas as pd

from kats.consts import TimeSeriesData
from kats.models.prophet import ProphetModel, ProphetParams

def forecast(df, time_col_name, steps):

    forecast_df = df.rename(columns={time_col_name: "time"})

    ts = TimeSeriesData(forecast_df)

    params = ProphetParams(seasonality_mode='multiplicative')

    m = ProphetModel(ts, params)

    m.fit()

    fcst = m.predict(steps=steps, freq="D")

    fcst = fcst.drop(columns=['fcst_lower', 'fcst_upper'])

    return fcst

if __name__ == "__main__":

    df = pd.read_csv("apple_data.csv")

    print(forecast(df, "date", 10))
