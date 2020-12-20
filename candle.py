import talib
import sys
import itertools
import yfinance as yf
import numpy as np
from collections import namedtuple


class CandlePatterns:
    def __init__(self, open_, high, low, close):
        self.version = "0.0.1"
        self.data = open_, high, low, close

    def prediction(self):
        return self.detail().type

    def detail(self):
        talib_patterns = {
            "CDL2CROWS": "Two Crows",
            "CDL3BLACKCROWS": "Three Black Crows",
            "CDL3INSIDE": "Three Inside Up/Down",
            "CDL3LINESTRIKE": "Three-Line Strike",
            "CDL3OUTSIDE": "Three Outside Up/Down",
            "CDL3STARSINSOUTH": "Three Stars In The South",
            "CDL3WHITESOLDIERS": "Three Advancing White Soldiers",
            "CDLABANDONEDBABY": "Abandoned Baby",
            "CDLADVANCEBLOCK": "Advance Block",
            "CDLBELTHOLD": "Belt-hold",
            "CDLBREAKAWAY": "Breakaway",
            "CDLCLOSINGMARUBOZU": "Closing Marubozu",
            "CDLCONCEALBABYSWALL": "Concealing Baby Swallow",
            "CDLCOUNTERATTACK": "Counterattack",
            "CDLDARKCLOUDCOVER": "Dark Cloud Cover",
            "CDLDOJI": "Doji",
            "CDLDOJISTAR": "Doji Star",
            "CDLDRAGONFLYDOJI": "Dragonfly Doji",
            "CDLENGULFING": "Engulfing Pattern",
            "CDLEVENINGDOJISTAR": "Evening Doji Star",
            "CDLEVENINGSTAR": "Evening Star",
            "CDLGAPSIDESIDEWHITE": "Up/Down-gap side-by-side white lines",
            "CDLGRAVESTONEDOJI": "Gravestone Doji",
            "CDLHAMMER": "Hammer",
            "CDLHANGINGMAN": "Hanging Man",
            "CDLHARAMI": "Harami Pattern",
            "CDLHARAMICROSS": "Harami Cross Pattern",
            "CDLHIGHWAVE": "High-Wave Candle",
            "CDLHIKKAKE": "Hikkake Pattern",
            "CDLHIKKAKEMOD": "Modified Hikkake Pattern",
            "CDLHOMINGPIGEON": "Homing Pigeon",
            "CDLIDENTICAL3CROWS": "Identical Three Crows",
            "CDLINNECK": "In-Neck Pattern",
            "CDLINVERTEDHAMMER": "Inverted Hammer",
            "CDLKICKING": "Kicking",
            "CDLKICKINGBYLENGTH":
            "Kicking - bull/bear determined by the longer marubozu",
            "CDLLADDERBOTTOM": "Ladder Bottom",
            "CDLLONGLEGGEDDOJI": "Long Legged Doji",
            "CDLLONGLINE": "Long Line Candle",
            "CDLMARUBOZU": "Marubozu",
            "CDLMATCHINGLOW": "Matching Low",
            "CDLMATHOLD": "Mat Hold",
            "CDLMORNINGDOJISTAR": "Morning Doji Star",
            "CDLMORNINGSTAR": "Morning Star",
            "CDLONNECK": "On-Neck Pattern",
            "CDLPIERCING": "Piercing Pattern",
            "CDLRICKSHAWMAN": "Rickshaw Man",
            "CDLRISEFALL3METHODS": "Rising/Falling Three Methods",
            "CDLSEPARATINGLINES": "Separating Lines",
            "CDLSHOOTINGSTAR": "Shooting Star",
            "CDLSHORTLINE": "Short Line Candle",
            "CDLSPINNINGTOP": "Spinning Top",
            "CDLSTALLEDPATTERN": "Stalled Pattern",
            "CDLSTICKSANDWICH": "Stick Sandwich",
            "CDLTAKURI": "Takuri (Dragonfly Doji with very long lower shadow)",
            "CDLTASUKIGAP": "Tasuki Gap",
            "CDLTHRUSTING": "Thrusting Pattern",
            "CDLTRISTAR": "Tristar Pattern",
            "CDLUNIQUE3RIVER": "Unique 3 River",
            "CDLUPSIDEGAP2CROWS": "Upside Gap Two Crows",
            "CDLXSIDEGAP3METHODS": "Upside/Downside Gap Three Methods"
        }
        Pattern = namedtuple("Pattern", ["name", "type", "index"])
        most_recent_pattern = Pattern(name=None, type=0, index=-1)
        for func_name, pat_name in talib_patterns.items():
            output = eval(f"talib.{func_name}(*self.data)")
            index = np.max(np.append(np.flatnonzero(output),
                                     -1))  # Append -1 to avoid empty array
            if index > most_recent_pattern.index:
                most_recent_pattern = Pattern(name=pat_name,
                                              type=output[index] // 100,
                                              index=index)
        return most_recent_pattern

if __name__ == "__main__":

    nifty50 = [
        'DRREDDY.NS', 'BAJAJ-AUTO.NS', 'INFY.NS', 'WIPRO.NS', 'CIPLA.NS',
        'HINDALCO.NS', 'SBIN.NS', 'TITAN.NS', 'HCLTECH.NS', 'UPL.NS',
        'ICICIBANK.NS', 'GAIL.NS', 'HEROMOTOCO.NS', 'ASIANPAINT.NS', 'ITC.NS',
        'SBILIFE.NS', 'HINDUNILVR.NS', 'RELIANCE.NS', 'EICHERMOT.NS',
        'SHREECEM.NS', 'AXISBANK.NS', 'TCS.NS', 'M&M.NS', 'SUNPHARMA.NS',
        'TECHM.NS', 'POWERGRID.NS', 'HDFCLIFE.NS', 'DIVISLAB.NS', 'NESTLEIND.NS',
        'LT.NS', 'GRASIM.NS', 'BPCL.NS', 'ULTRACEMCO.NS', 'TATAMOTORS.NS',
        'NTPC.NS', 'JSWSTEEL.NS', 'BAJAJFINSV.NS', 'TATASTEEL.NS', 'HDFC.NS',
        'BHARTIARTL.NS', 'BRITANNIA.NS', 'BAJFINANCE.NS', 'COALINDIA.NS',
        'ADANIPORTS.NS', 'KOTAKBANK.NS', 'IOC.NS', 'MARUTI.NS', 'ONGC.NS',
        'HDFCBANK.NS', 'INDUSINDBK.NS'
    ]
    data = yf.download(tickers=" ".join(nifty50),progress=sys.stdout.isatty(),period="5d")
    data = data.swaplevel(0, 1, axis=1)
    detected = []
    for equity in nifty50:
        price_history = data[equity]
        ohlc = price_history.Open.values, price_history.High.values, price_history.Close.values, price_history[
            "Adj Close"].values
        candlePattern = CandlePatterns(*ohlc)
        pattern = candlePattern.detail()
        if pattern.name:
            date = price_history.iloc[pattern.index].name.strftime("%d %b %Y")
            detected.append({
                "equity_name": equity,
                "pattern_name": pattern.name,
                "pattern_type": 'Bullish' if pattern.type == 1 else 'Bearish',
                "detected_date": date
            })
    print("Version:",candlePattern.version)
    detected.sort(key=lambda x: x["pattern_type"])
    for pattern_type, pattern in itertools.groupby(
            detected, key=lambda x: x["pattern_type"]):
        print("\n"+pattern_type+"\n"+"="*len(pattern_type))
        for p in pattern:
            fmt = f'{p["pattern_name"]} in {p["equity_name"][:-3]} on {p["detected_date"]}'
            print(fmt)