import streamlit as st
import yfinance as yf
from newsapi import NewsApiClient
import pandas as pd

# 1. Setup App Title and Layout
st.set_page_config(layout="wide")
st.title("🏛️ SovereignDebt Pulse")
st.subheader("Tracking how political shocks manipulate global bond markets.")

# 2. Sidebar Configuration (User Inputs)
st.sidebar.header("Control Panel")
country = st.sidebar.selectbox("Select Country to Analyze", ["United States", "United Kingdom", "Japan"])
ticker_dict = {"United States": "^TNX", "United Kingdom": "^IEX", "Japan": "^JG10"} 

# 3. Fetch Financial Data (Bond Yields)
st.write(f"### 📈 10-Year Government Bond Yield: {country}")
bond_ticker = ticker_dict[country]
bond_data = yf.download(bond_ticker, period="1mo", interval="1d")

if not bond_data.empty:
    chart_data = bond_data['Close']
    st.line_chart(chart_data)
else:
    st.error("Failed to fetch bond data. Market might be closed.")

# 4. Fetch Political News Data (Securely via Secrets)
st.write(f"### 📰 Recent Political Context for {country}")
try:
    # This reads the password key from Streamlit Cloud securely
    newsapi = NewsApiClient(api_key=st.secrets["NEWS_API_KEY"]) 
    
    headlines = newsapi.get_everything(q=f"{country} AND (politics OR election OR tariff OR government)",
                                      language='en',
                                      sort_by='publishedAt',
                                      page_size=5)
    
    for article in headlines['articles']:
        st.markdown(f"**[{article['title']}]({article['url']})**")
        st.caption(f"Source: {article['source']['name']} | Published: {article['publishedAt'][:10]}")
        st.write(article['description'])
        st.markdown("---")
except Exception as e:
    st.info("💡 Make sure to add your NEWS_API_KEY inside your Streamlit Cloud Advanced Settings to see news headlines here!")
