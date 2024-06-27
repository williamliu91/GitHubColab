# Import the necessary libraries
import plotly.express as px
import yfinance as yf
import pandas as pd

# Download the Google stock data
data = yf.download('GOOGL', start='2022-01-01', end='2024-06-21')

# Calculate MACD
# First, calculate the 12-day EMA (Exponential Moving Average)
shortEMA = data['Close'].ewm(span=12, adjust=False).mean()

# Next, calculate the 26-day EMA
longEMA = data['Close'].ewm(span=26, adjust=False).mean()

# Calculate MACD line
MACD = shortEMA - longEMA

# Calculate Signal line (9-day EMA of MACD)
signal = MACD.ewm(span=9, adjust=False).mean()

# Calculate MACD Histogram
histogram = MACD - signal

# Multiply MACD and Signal line by 5 for amplification
MACD_amplified = MACD * 5
signal_amplified = signal * 5

# Calculate MA 200
ma200 = data['Close'].rolling(window=200).mean()

# Add MACD, Signal Line, and MA 200 to the dataframe
data['MACD'] = MACD_amplified
data['Signal Line'] = signal_amplified
data['MA 200'] = ma200

# Create a line chart with MACD, Signal Line, and MA 200
fig = px.line(data, x=data.index, y=['Close', 'MACD', 'Signal Line', 'MA 200'],
              title='Google Stock Prices with Amplified MACD and MA 200',
              labels={'value': 'Price', 'variable': 'Metric', 'date': 'Date'})

# Add MACD Histogram as a bar chart with pitch black color
fig.add_bar(x=data.index, y=histogram * 5, name='MACD Histogram', marker_color='rgb(0, 0, 0)')

# Add a dynamic spike line (both vertical and horizontal)
fig.update_layout(
    hovermode='x unified',
    xaxis=dict(
        showspikes=True,
        spikemode='across',
        spikesnap='cursor',
        spikedash='dot',  # Change spike line to dotted
        showline=True,
        spikecolor="green",
        spikethickness=1
    ),
    yaxis=dict(
        showspikes=True,
        spikemode='across',
        spikesnap='cursor',
        spikedash='dot',  # Change spike line to dotted
        showline=True,
        spikecolor="green",
        spikethickness=1
    )
)

# Show the chart
fig.show()
