import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET
import urllib.parse

# Layout configuration
st.set_page_config(layout="wide")

# Premium custom CSS to enforce a high-end fintech dashboard aesthetic
st.markdown("""
    <style>
        .reportview-container { background: #0E1117; }
        h1, h2, h3, p { font-family: 'Inter', sans-serif; }
        
        .module-header-fin {
            color: #00D4B2; 
            font-size: 1.25rem; 
            font-weight: 600; 
            text-transform: uppercase; 
            letter-spacing: 1px;
            border-bottom: 2px solid #00D4B2; 
            padding-bottom: 6px; 
            margin-bottom: 16px;
        }
        .module-header-pol {
            color: #3B82F6; 
            font-size: 1.25rem; 
            font-weight: 600; 
            text-transform: uppercase; 
            letter-spacing: 1px;
            border-bottom: 2px solid #3B82F6; 
            padding-bottom: 6px; 
            margin-bottom: 16px;
        }
        
        .premium-card-fin {
            background-color: #161B22;
            border-left: 3px solid #00D4B2;
            padding: 18px;
            margin-bottom: 14px;
            border-radius: 4px;
            transition: all 0.2s ease-in-out;
        }
        .premium-card-pol {
            background-color: #161B22;
            border-left: 3px solid #3B82F6;
            padding: 18px;
            margin-bottom: 14px;
            border-radius: 4px;
            transition: all 0.2s ease-in-out;
        }
        .premium-card-fin:hover, .premium-card-pol:hover {
            transform: translateY(-2px);
            background-color: #1C212B;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        
        .item-title { color: #FFFFFF; font-size: 1.05rem; font-weight: 600; line-height: 1.4; margin-bottom: 6px; }
        .item-meta { color: #8A99AD; font-size: 0.8rem; font-family: monospace; letter-spacing: 0.5px; margin-bottom: 10px; }
        .item-desc { color: #C1C9D2; font-size: 0.9rem; line-height: 1.5; margin-bottom: 12px; }
        
        .terminal-btn {
            display: inline-block;
            background-color: #21262D;
            color: #C9D1D9;
            padding: 6px 12px;
            font-size: 0.8rem;
            font-family: monospace;
            text-decoration: none;
            border-radius: 4px;
            border: 1px solid #30363D;
            transition: all 0.15s;
        }
        .terminal-btn:hover { background-color: #30363D; color: #FFFFFF; border-color: #8B949E; }
    </style>
""", unsafe_allowed_html=True)

st.title("SovereignDebt Pulse")

# Selection menu component
active_country = st.selectbox(
    "Select Target Vector Node", 
    ["United States", "United Kingdom", "Japan", "Germany", "France", "Canada", "Australia", "India", "Brazil", "South Africa"]
)

st.markdown(f"<h2 style='font-size:1.5rem; margin-top:20px; color:#FFFFFF;'>Selected Target Vector: {active_country}</h2>", unsafe_allowed_html=True)

# 50/50 Horizontal layout architecture
left_column, right_column = st.columns(2)

# Функция для безопасного парсинга RSS-ленты новостей Google News
def fetch_rss_news(query):
    articles = []
    try:
        encoded_query = urllib.parse.quote(query)
        url = f"https://google.com{encoded_query}&hl=en-US&gl=US&ceid=US:en"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            for item in root.findall('.//item')[:3]:  # Берём топ-3 самые свежие новости
                title = item.find('title').text if item.find('title') is not None else "No Title"
                link = item.find('link').text if item.find('link') is not None else "#"
                pub_date = item.find('pubDate').text if item.find('pubDate') is not None else "Recent"
                source = item.find('source').text if item.find('source') is not None else "Google News"
                
                # Чистим заголовок от названия источника в конце, если он там есть
                if " - " in title:
                    title = title.rsplit(" - ", 1)[0]
                    
                articles.append({
                    "title": title,
                    "url": link,
                    "publishedAt": pub_date[:16],
                    "source": source
                })
    except Exception as e:
        pass
    return articles

# Left Split Column: Financial Indicators Data Panel
with left_column:
    st.markdown("<div class='module-header-fin'>Financial News Feed</div>", unsafe_allowed_html=True)
    fin_articles = fetch_rss_news(f'{active_country} (finance OR economy OR "central bank" OR bonds)')
    
    if fin_articles:
        for post in fin_articles:
            st.markdown(f"""
                <div class="premium-card-fin">
                    <div class="item-title">{post['title']}</div>
                    <div class="item-meta">INDEX: {post['source']} // DATETIME: {post['publishedAt']}</div>
                    <div class="item-desc">Access the real-time financial report wire for detailed coverage on economic trends within this node.</div>
                    <a class="terminal-btn" href="{post['url']}" target="_blank">RESOLVE REPORT</a>
                </div>
            """, unsafe_allowed_html=True)
    else:
        st.markdown("<p style='color:#8A99AD; font-family:monospace;'>NO RECENT FINANCIAL RECORDS DETECTED FOR THIS VECTOR</p>", unsafe_allowed_html=True)

# Right Split Column: Geopolitical Tracking Data Panel
with right_column:
    st.markdown("<div class='module-header-pol'>Political News Feed</div>", unsafe_allowed_html=True)
    pol_articles = fetch_rss_news(f'{active_country} (politics OR government OR tariff OR regulation)')
    
    if pol_articles:
        for post in pol_articles:
            st.markdown(f"""
                <div class="premium-card-pol">
                    <div class="item-title">{post['title']}</div>
                    <div class="item-meta">INDEX: {post['source']} // DATETIME: {post['publishedAt']}</div>
                    <div class="item-desc">Access the dynamic legislative dossier for structural updates and tracking on executive policy nodes.</div>
                    <a class="terminal-btn" href="{post['url']}" target="_blank">RESOLVE DOSSIER</a>
                </div>
            """, unsafe_allowed_html=True)
    else:
        st.markdown("<p style='color:#8A99AD; font-family:monospace;'>NO RECENT POLITICAL RECORDS DETECTED FOR THIS VECTOR</p>", unsafe_allowed_html=True)
