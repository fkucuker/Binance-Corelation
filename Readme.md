Project Overview

This project leverages the Binance API to analyze historical closing data (15-minute intervals over 2 years) for cryptocurrency pairs. The goal is to identify coin pairs with a correlation coefficient above 0.85 and highlight pairs whose correlation has dropped below 0 over the last 30 days. Among these, pairs with a return difference of 30% or more are analyzed further.

This enables users to potentially take advantage of arbitrage opportunities by opening long and short positions on correlated pairs.

![Project Overview - visual selection](https://github.com/user-attachments/assets/861856c0-be9f-49c2-8f40-7538b301ed03)

Features

Historical closing price analysis using Binance API.

Identification of coin pairs with high correlation and significant return differences.

Automated filtering of pairs for potential arbitrage opportunities.

Export results to Excel for further analysis.

Visual representation of correlations using heatmaps.

![Project Overview - visual selection (1)](https://github.com/user-attachments/assets/7742429d-5d2f-4827-8da4-bd4ebf214c81)


Installation

Clone this repository:

git clone <repository_url>

Navigate to the project directory:

cd <repository_directory>

Install dependencies:

pip install -r requirements.txt

Requirements

The following Python libraries are required:

 pandas==2.0.3
 numpy==1.25.2
 matplotlib==3.5.1
 seaborn==0.11.2
 requests==2.26.0

Binance API Configuration

Obtain your Binance API key and secret from your Binance account.

Add them to the script by modifying the following variables in the main.py file:

API_KEY = "your_api_key"
API_SECRET = "your_api_secret"

Alternatively, store them in a .env file for security.

Usage

Run the main script to start the analysis:

python main.py

Important Notes

Adhere to Binance API request weight limits to avoid throttling.

Ensure your API key and secret remain confidential.

The accuracy of data fetched from Binance and its interpretation are the user's responsibility.

Any financial gains or losses incurred as a result of using this software are solely the user's responsibility.

Contributing

Contributions are welcome! To contribute:

Fork the repository.

Create a new branch for your feature or fix:

git checkout -b feature-name

Commit your changes:

git commit -m "Add feature/fix description"

Push to your fork and submit a pull request.

