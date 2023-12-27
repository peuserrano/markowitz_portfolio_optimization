# Markowitz Portfolio Optimization using Python

This project implements Markowitz's (1952) portfolio theory using Python, allowing users to optimize their investment portfolios, given that they have chosen a set of listed companies and a predetermined time interval for backtesting.

## Overview

The aim of this project is to assist users in selecting an optimal combination of stocks from a set of publicly traded stocks within a specific time frame for analysis. The program utilizes historical stock data to generate a visual representation illustrating various portfolios, along with identifying the optimized portfolio exhibiting optimal returns and volatilities.

## How it Works

1. **Selection of Stocks and Timeframe:** Users choose a selection of stocks traded on a stock exchange and specify a time period for analysis.

2. **Portfolio Optimization:** The program employs the Markowitz portfolio theory to compute and visualize various investment portfolios, highlighting the optimized portfolio with the best balance of returns and volatilities.

3. **Results:** Upon execution, the program returns a visual representation showcasing different portfolios, identifies the optimized one, and provides information regarding the corresponding returns and volatilities. Additionally, it generates a dataframe displaying the weight allocation for each stock within the optimized portfolio.

## Usage

1. **Installation:** Ensure the required Python libraries (like `yfinance`, `numpy`, `matplotlib`, `pandas`, `scipy`) are installed.
   
2. **Execution:** Run the Python script, providing the chosen stocks and timeframe for analysis.

3. **Visualization:** View the generated figure depicting various portfolios, the optimized portfolio, and associated returns and volatilities. Access the resulting dataframe to analyze the weight allocation for each stock in the optimized portfolio.
