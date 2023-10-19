# Import the streamlit modules
import streamlit as st
from streamlit_lottie import st_lottie

# Get the necessary modules for retrieving stock info and displaying it within a certain time range
import yfinance as yf
import plotly.express as px
from datetime import datetime

# Import Path for file navigation and json for integrating lottie files
from pathlib import Path
import json


# Obtain the path of the current file
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()

# Find the CSS file
css_file = current_dir / "styles" / "main.css"

# Store the page icon and title in variables
PAGE_TITLE = "Stock Tracker"
PAGE_ICON = "📈"

# Set the page configuration to the title and icon variables defined above
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

# Open CSS file
with open(css_file) as css:
    st.markdown("<style>{}</style>".format(css.read()), unsafe_allow_html=True)

# Define a function to load the Lottie file (basically a gif)
def load_lottie(filepath: str):
    with open(filepath, "r") as f:
        # Use json to load the file
        return json.load(f)

# Call the function to load the lottie file
stocks_lottie = load_lottie("stocks.json")

# Set the page title to "Stock Tracker"
st.title("Stock Tracker")

# Create two columns on the page
col1, col2 = st.columns(2, gap="small")

# Add instructions in the first column
with col1:
    # Welcome the user
    st.write("**Welcome to the Stock Tracker app!**")
    st.write("Enter any stock ticker in the left sidebar to view its price chart over a customizable time range (for example, Microsoft --> MSFT)")

    # Add blank space
    st.write("###")
    
    # Store the link to Yahoo Finance in a variable
    link = "https://ca.finance.yahoo.com/"

    # Link the Yahoo Finance website for users trying to find stock tickers
    st.write(f"Having trouble? You can find stock tickers on this [website]({link}).")

    # Add a divider
    st.write("---")

# Add the lottie file in the second column
with col2:
    st_lottie(
    stocks_lottie,
    speed=1,
    reverse=False,
    loop=True,
    # Set quality to low to prevent lag
    quality="low",
)

# Get the ticker input from the Streamlit sidebar
ticker = st.sidebar.text_input("Ticker")

# Set the default start date to January 1, 2015
default_start_date = datetime(2015, 1, 1)
start_date = st.sidebar.date_input("Start Date", default_start_date)

# Set the end date (default will be today's date)
end_date = st.sidebar.date_input("End Date")


# Check if the user has entered a ticker
if ticker:
    # Use yahoofinance to download stock data with the ticker, start_date, and end_date parameters in place
    data = yf.download(ticker, start=start_date, end=end_date)
    
    # If the data is not empty (meaning that it exists), then proceed
    if not data.empty:

        # Set ticker_yahoo to the stock ticker
        ticker_yahoo = yf.Ticker(ticker)
        # Find the live data of the ticker using .history()
        data_live = ticker_yahoo.history()
        # Find the close price of the stock by using the [-1] index
        last_quote = data["Close"].iloc[-1]
        # Add the ticker as a subheader and capitalize it
        st.subheader(ticker.upper())
        # Display the price using st.write and round it to two decimal places
        st.write(f"**Close Price = ${last_quote:.2f}**")


        # Make sure the data is not empty
        fig = px.line(data, x=data.index, y="Adj Close")
        # Use plotly_chart to graph the chart
        st.plotly_chart(fig)

        # Add tips to help the user
        st.subheader("Tips:")
        st.write("- 🔎 Left click and hold to zoom into a specific area of the graph")
        st.write("- ↔️ Left click and drag the axes to move the chart vertically or horizontally")
        st.write("- ⬇️ Click the camera icon to download the chart as a pdf ")
        st.write("- ✣ Click the four-arrow icon to pan around the chart")
        st.write("- 📉 Press the autoscale icon (left of the home symbol) or double left-click to revert the graph to default settings")

    # If no data is found for the ticker the user entered, then display this message
    else:
        st.write("No data available for the given ticker and date range.")

# If the user has not entered any ticker yet, then display this message
else:
    st.write("Please enter a valid ticker.")

