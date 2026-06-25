import yfinance as yf
import mplfinance as mpf
import pandas as pd
import os
import gc

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from tqdm import tqdm


# Tickers is a List of Stcoks (tickers) listed in the stock market (you can get these name from goole or AI to get the list of stock you want to get . )

# ticker (str | tuple[str, str]) – Yahoo Finance symbol (e.g. “AAPL”) or a tuple of (symbol,MIC) e.g. (‘OR’,’XPAR’) (MIC = market identifier code)

TICKERS = [
    'ADANIENT.NS','BSE.NS', 'ADANIPORTS.NS', 'APOLLOHOSP.NS', 'ASIANPAINT.NS', 'AXISBANK.NS',
    'BAJAJ-AUTO.NS', 'BAJAJFINSV.NS', 'BAJFINANCE.NS', 'BEL.NS', 'BHARTIARTL.NS',
    'BPCL.NS', 'BRITANNIA.NS', 'CIPLA.NS', 'COALINDIA.NS', 'DRREDDY.NS',
    'EICHERMOT.NS', 'GRASIM.NS', 'HCLTECH.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS',
    'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS', 'INDUSINDBK.NS',
    'INFY.NS', 'ITC.NS', 'JIOFIN.NS', 'JSWSTEEL.NS', 'KOTAKBANK.NS',
    'LT.NS', 'M&M.NS', 'MARUTI.NS', 'NESTLEIND.NS',
    'NTPC.NS', 'ONGC.NS', 'POWERGRID.NS', 'RELIANCE.NS', 'SBILIFE.NS',
    'SBIN.NS', 'SHRIRAMFIN.NS', 'SUNPHARMA.NS', 'TATACONSUM.NS', 'HAL.NS',
    'TATASTEEL.NS', 'TCS.NS', 'TECHM.NS', 'TITAN.NS', 'ULTRACEMCO.NS',
    'WIPRO.NS'
]

# Hyperparameters
START_DATE = '2016-01-01' # Date - YYYY-MM-DD
END_DATE = '2026-01-01'

WINDOW_SIZE = 30
TARGET_AHEAD = 5
THRESHOLD_PCT = 0.5 
TEST_SPLIT = 0.20
Name = 'Nifty_dataset'



directories = [
    f'{Name}/train/bullish',
    f'{Name}/train/bearish',
    f'{Name}/train/neutral',
    f'{Name}/test/bullish',
    f'{Name}/test/bearish',
    f'{Name}/test/neutral'
]

# Creating directories
for dir_path in directories:
    os.makedirs(dir_path, exist_ok=True)



# Looping through Each Stcok and getting its data for all stocks mentioned in the list 
for ticker in TICKERS:

    print(f"\nProcessing Ticker Asset Matrix: {ticker}")

    df = yf.download(
        ticker,
        start=START_DATE,
        end=END_DATE,
        progress=False
    )

    if df.empty:
        print(f"Warning: No historical profile returned for {ticker}. Skipping.")
        continue

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)

    df['Future_Close'] = df['Close'].shift(-TARGET_AHEAD)

    df['Price_Change'] = df['Future_Close'] - df['Close']

    df['Pct_Return'] = (
        df['Price_Change'] / df['Close']
    ) * 100

    df = df.dropna()

    if len(df) <= WINDOW_SIZE:
        print(f" Warning: Dataset arrays for {ticker} are insufficient size. Skipping.")
        continue

    split_idx = int(len(df) * (1 - TEST_SPLIT))

    for i in tqdm(
        range(len(df) - WINDOW_SIZE),
        desc=f"Generating {ticker} Multi-Class Matrices"
    ):

        window_df = df.iloc[i:i + WINDOW_SIZE]

        current_window_return = df.iloc[
            i + WINDOW_SIZE - 1
        ]['Pct_Return']

        if current_window_return > THRESHOLD_PCT:
            label_dir = 'bullish'
        elif current_window_return < -THRESHOLD_PCT:
            label_dir = 'bearish'
        else:
            label_dir = 'neutral'

        phase_dir = (
            'train'
            if i < split_idx
            else 'test'
        )

        file_path = (
            f'{Name}/'
            f'{phase_dir}/'
            f'{label_dir}/'
            f'{ticker}_{i}.png'
        )

        fig, axlist = mpf.plot(
            window_df,
            type='candle',
            style='charles',
            volume=True,
            mav=(20,),
            axisoff=True,
            savefig=dict(
                fname=file_path,
                dpi=72,
                bbox_inches='tight',
                pad_inches=0
            ),
            returnfig=True
        )

        plt.close(fig)

        del fig
        del axlist
        del window_df

        if i % 100 == 0:
            gc.collect()

    del df
    gc.collect()

print(f'\nDataset Created Successfully')