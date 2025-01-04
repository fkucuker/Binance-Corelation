import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import time
import requests
import os

# Binance API key and secret
API_KEY = YOUR_API_KEY
API_SECRET = YOUR_API_SEC

class BinanceAPI:
    def __init__(self, api_key: str, api_secret: str):
        self.base_url = "https://api.binance.com"
        self.headers = {
            "X-MBX-APIKEY": api_key
        }
        self.request_weight = 0  # Track the request weight

    def _check_request_limit(self):
        """Check request weight limit and wait if necessary."""
        max_weight = 6000  # Maximum weight allowed per minute
        if self.request_weight >= max_weight:
            print("Request limit reached, waiting for 60 seconds...")
            time.sleep(60)
            self.request_weight = 0

    def get_ticker_data(self):
        """Get market ticker data for all symbols."""
        self._check_request_limit()
        endpoint = "/api/v3/ticker/24hr"
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.headers)
        self.request_weight += 1
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_historical_klines(self, symbol: str, interval: str, start_time: int, end_time: int):
        """Fetch historical candlestick data for a given symbol and time range."""
        self._check_request_limit()
        endpoint = "/api/v3/klines"
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": start_time,
            "endTime": end_time,
            "limit": 1000
        }
        url = self.base_url + endpoint
        response = requests.get(url, params=params, headers=self.headers)
        self.request_weight += 1
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def fetch_all_historical_data(self, symbol: str, interval: str, days: int):
        """Fetch all historical data within a given number of days."""
        end_time = int(datetime.now().timestamp() * 1000)
        start_time = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)
        all_data = []

        while start_time < end_time:
            self._check_request_limit()
            klines = self.get_historical_klines(symbol, interval, start_time, end_time)
            if not klines:
                break
            all_data.extend(klines)
            start_time = klines[-1][6]
            time.sleep(0.1)

        return all_data

class CoinAnalyzer:
    def __init__(self, binance_api: BinanceAPI):
        self.api = binance_api

    def get_top_50_coins_by_market_cap(self):
        """Fetch and list top 50 coins with USDT pairs by market cap."""
        data = self.api.get_ticker_data()
        usdt_pairs = [
            {
                "symbol": item["symbol"],
                "price": float(item["lastPrice"]),
                "volume": float(item["quoteVolume"])
            }
            for item in data if item["symbol"].endswith("USDT")
        ]
        sorted_coins = sorted(usdt_pairs, key=lambda x: x["volume"], reverse=True)
        return [coin["symbol"] for coin in sorted_coins[:50]]

    def get_historical_closing_prices(self, symbols: list, interval: str = "15m"):
        """Fetch historical closing prices for given symbols."""
        closing_prices = {}

        for symbol in symbols:
            klines = self.api.fetch_all_historical_data(symbol, interval, days=730)
            closing_prices[symbol] = {
                datetime.fromtimestamp(kline[6] / 1000).strftime("%Y-%m-%d %H:%M:%S"): float(kline[4])
                for kline in klines
            }

        df = pd.DataFrame(closing_prices)
        df.index = pd.to_datetime(df.index)
        return df


def calculate_monthly_percentage_change(dataframe, symbols, days=30):
    """Calculate percentage change for the last days for given symbols."""
    end_date = dataframe.index.max()
    start_date = end_date - timedelta(days=days)

    monthly_changes = {}
    for symbol in symbols:
        symbol_data = dataframe[symbol].dropna()
        if len(symbol_data) > 0 and start_date in symbol_data.index:
            start_price = symbol_data.loc[start_date]
            end_price = symbol_data.loc[end_date]
            if start_price > 0:
                percentage_change = ((end_price - start_price) / start_price) * 100
                monthly_changes[symbol] = percentage_change
            else:
                monthly_changes[symbol] = np.nan
        else:
            monthly_changes[symbol] = np.nan

    return monthly_changes


def save_to_excel_with_recent_correlation(
    correlation_matrix, monthly_changes, output_file, entry_time,
    current_prices, historical_data, closing_prices_df
):
    """Save filtered correlation data, positions, and profit/loss to Excel."""
    data = []

    if entry_time in closing_prices_df.index:
        entry_prices = closing_prices_df.loc[entry_time].to_dict()
    else:
        closest_idx = closing_prices_df.index.get_indexer([entry_time], method="nearest")[0]
        entry_prices = closing_prices_df.iloc[closest_idx].to_dict()

    recent_30_days = closing_prices_df.tail(30)
    recent_correlation_matrix = recent_30_days.corr()

    for sym1 in correlation_matrix.columns:
        for sym2 in correlation_matrix.columns:
            if sym1 != sym2:
                correlation_value = correlation_matrix.loc[sym1, sym2]
                recent_correlation_value = recent_correlation_matrix.loc[sym1, sym2]
                monthly_diff = monthly_changes.get(sym1, 0) - monthly_changes.get(sym2, 0)

                if correlation_value > 0.85 and monthly_diff > 30:
                    position = "SELL"
                elif correlation_value > 0.85 and monthly_diff < -30:
                    position = "BUY"
                else:
                    position = "HOLD"

                entry_price = entry_prices.get(sym1, None)
                current_price = current_prices.get(sym1, None)

                if position in ["BUY", "SELL"] and entry_price and current_price:
                    profit_loss = ((current_price - entry_price) / entry_price) * 100 \
                        if position == "BUY" else ((entry_price - current_price) / entry_price) * 100
                else:
                    profit_loss = "-"

                data.append([
                    sym1, sym2, correlation_value, monthly_diff, position,
                    entry_price, current_price, profit_loss, recent_correlation_value
                ])

    # Create a DataFrame for the results
    result_df = pd.DataFrame(data, columns=[
        "Sembol1", "Sembol2", "Korelasyon Oranı (2 Yıllık)", "Son Bir Aylık Oran Artış Farkı",
        "Position", "Entry_Position", "Current_Position", "Profit/Loss", "Son 30 Günlük Korelasyon"
    ])

    # Filter the DataFrame based on conditions
    filtered_df = result_df[
        (result_df["Korelasyon Oranı (2 Yıllık)"] > 0.875) &
        (result_df["Son 30 Günlük Korelasyon"] < 0) &
        ((result_df["Son Bir Aylık Oran Artış Farkı"] >= 30) |
         (result_df["Son Bir Aylık Oran Artış Farkı"] <= -30)) &
        (result_df["Position"].isin(["BUY", "SELL"]))
    ]

    # Rearrange columns to move "Son 30 Günlük Korelasyon" to the last position
    column_order = [
        "Sembol1", "Sembol2", "Korelasyon Oranı (2 Yıllık)", "Son Bir Aylık Oran Artış Farkı",
        "Position", "Entry_Position", "Current_Position", "Profit/Loss", "Son 30 Günlük Korelasyon"
    ]
    filtered_df = filtered_df[column_order]

    # Save the filtered data to Excel
    filtered_df.to_excel(output_file, index=False)
    print(f"Sonuçlar {output_file} dosyasına kaydedildi.")



def plot_correlation_heatmap(correlation_matrix):
    """Plot a heatmap of the correlation matrix."""
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=False, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Correlation Heatmap of Coin Closing Prices")
    plt.show()


def main():
    # Binance API ile bağlantı
    binance_api = BinanceAPI(api_key=API_KEY, api_secret=API_SECRET)
    analyzer = CoinAnalyzer(binance_api)

    # İlk 50 coin'i getir
    top_50_symbols = analyzer.get_top_50_coins_by_market_cap()

    # Tarihsel kapanış fiyatlarını al
    closing_prices_df = analyzer.get_historical_closing_prices(top_50_symbols)

    # Eksik verileri kontrol et ve temizle
    print("Eksik Veri Sayısı:\n", closing_prices_df.isna().sum())
    max_missing_ratio = 0.1
    row_count = closing_prices_df.shape[0]
    closing_prices_df = closing_prices_df.loc[:, closing_prices_df.isna().sum() / row_count < max_missing_ratio]
    closing_prices_df.dropna(inplace=True)

    if closing_prices_df.empty:
        print("Korelasyon oluşturmak için yeterli veri yok.")
        return

    # Korelasyon matrisi oluştur
    correlation_matrix = closing_prices_df.corr()

    # Son 30 günlük yüzde değişimi hesapla
    monthly_changes = calculate_monthly_percentage_change(closing_prices_df, closing_prices_df.columns, days=30)

    # Giriş zamanı belirle
    entry_time = "2024-11-06 21:01:00"
    entry_time = pd.Timestamp(entry_time)

    # Güncel fiyatları al
    ticker_data = binance_api.get_ticker_data()
    ticker_dict = {item["symbol"]: float(item["lastPrice"]) for item in ticker_data}
    current_prices = {symbol: ticker_dict.get(symbol, None) for symbol in closing_prices_df.columns}

    # Tarihsel verileri sözlük olarak tut
    historical_data = {symbol: closing_prices_df[symbol].to_dict() for symbol in closing_prices_df.columns}

    # Excel çıktı klasörünü ayarla
    output_dir = os.path.join(os.getcwd(), "../outputs")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "deneme_10.xlsx")

    # Çıktı dosyasını kaydet
    save_to_excel_with_recent_correlation(
        correlation_matrix, monthly_changes, output_file, entry_time,
        current_prices, historical_data, closing_prices_df
    )

    # Korelasyon ısı haritasını çiz
    plot_correlation_heatmap(correlation_matrix)

if __name__ == "__main__":
    main()
