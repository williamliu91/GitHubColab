import yfinance as yf
import pandas as pd

def get_company_data(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    financials = ticker.financials
    balance_sheet = ticker.balance_sheet

    eps_data = financials.loc['Basic EPS']
    revenue_data = financials.loc['Total Revenue']

    history = ticker.history(period="5y")
    market_cap_data = history['Close'] * ticker.info['sharesOutstanding']

    current_dividend_yield = ticker.info.get('dividendYield', 0)

    net_income = financials.loc['Net Income']
    total_assets = balance_sheet.loc['Total Assets']

    equity_labels = ['Total Stockholder Equity', 'Stockholders Equity', 'Total Equity']
    for label in equity_labels:
        if label in balance_sheet.index:
            total_equity = balance_sheet.loc[label]
            break
    else:
        print(f"Couldn't find total equity in balance sheet for {ticker_symbol}. Please check the data structure.")
        total_equity = pd.Series([0, 0, 0])  # Placeholder

    total_liabilities = balance_sheet.loc['Total Liabilities Net Minority Interest']

    roe = net_income / total_equity
    roa = net_income / total_assets
    debt_to_equity = total_liabilities / total_equity

    company_data = []

    for year, eps, revenue, roe_val, roa_val, de_val in zip(
        eps_data.index[:3][::-1], eps_data.values[:3][::-1], revenue_data.values[:3][::-1],
        roe.values[:3][::-1], roa.values[:3][::-1], debt_to_equity.values[:3][::-1]
    ):
        year_end = f"{year.year}-12-31"
        market_cap = market_cap_data.loc[year_end] if year_end in market_cap_data.index else None

        company_data.append({
            'Company': ticker_symbol,
            'Year': year.year,
            'EPS': round(eps, 2),
            'Revenue (Billions)': round(revenue / 1e9, 2),
            'Market Cap (Billions)': round(market_cap / 1e9, 2) if market_cap else 'N/A',
            'Dividend Yield (%)': round(current_dividend_yield * 100, 2) if current_dividend_yield else 0,
            'ROE (%)': round(roe_val * 100, 2),
            'ROA (%)': round(roa_val * 100, 2),
            'Debt to Equity': round(de_val, 2)
        })

    return company_data

# List of companies
companies = ['GOOGL', 'MSFT', 'AAPL', 'NVDA']

# Fetch data for all companies
all_data = []
for company in companies:
    all_data.extend(get_company_data(company))

# Create a DataFrame and display it
df = pd.DataFrame(all_data)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
print(df.to_string(index=False))