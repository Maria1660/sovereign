import streamlit as st
import plotly.express as px
import pandas as pd
from newsapi import NewsApiClient

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
st.write("Interact with country regions across the global mapping layer to isolate macro datasets.")

# Load Plotly's built-in global dataset to access all countries automatically
global_df = px.data.gapminder().query("year == 2007")

# Render a full, clickable vector choropleth map instead of scattered points
fig = px.choropleth(
    global_df,
    locations="iso_alpha",
    color_discrete_sequence=["#1C212B"], 
    hover_name="country",
    projection="natural earth"
)

fig.update_layout(
    template='plotly_dark',
    geo=dict(
        showland=True, landcolor='#161B22',
        showocean=True, oceancolor='#0D1117',
        showcountries=True, countrycolor='#30363D',
        showframe=False
    ),
    margin=dict(l=0, r=0, t=10, b=0),
    height=450,
    showlegend=False
)
fig.update_traces(
    marker_line_color='#30363D', 
    marker_line_width=1,
    selected_marker_opacity=1,
    unselected_marker_opacity=0.4
)

# Track interface country selections dynamically via map clicks
map_selection = st.plotly_chart(fig, use_container_width=True, on_select="rerun")

# Establish default context values
active_country = "United States"

# Detect which specific country polygon was clicked
if map_selection and "selection" in map_selection and map_selection["selection"]["points"]:
    node_idx = map_selection["selection"]["points"]["point_number"]
    active_country = global_df.iloc[node_idx]['country']

st.markdown(f"<h2 style='font-size:1.5rem; margin-top:20px; color:#FFFFFF;'>Selected Target Vector: {active_country}</h2>", unsafe_allowed_html=True)

# 50/50 Horizontal layout architecture
left_column, right_column = st.columns(2)

try:
    newsapi = NewsApiClient(api_key=st.secrets["NEWS_API_KEY"])
    
    # Left Split Column: Financial Infrastructure Data
    with left_column:
        st.markdown("<div class='module-header-fin'>Financial News Feed</div>", unsafe_allowed_html=True)
        financial_response = newsapi.get_everything(
            q=f'"{active_country}" AND (finance OR economy OR "central bank" OR bonds)',
            language='en', sort_by='publishedAt', page_size=3
        )
        
        if financial_response['articles']:
            for post in financial_response['articles']:
                snippet = post['description'] if post['description'] else "Abstract brief unavailable for this node entry."
                st.markdown(f"""
                    <div class="premium-card-fin">
                        <div class="item-title">{post['title']}</div>
                        <div class="item-meta">INDEX: {post['source']['name']} // DATETIME: {post['publishedAt'][:10]}</div>
                        <div class="item-desc">{snippet}</div>
                        <a class="terminal-btn" href="{post['url']}" target="_blank">RESOLVE REPORT</a>
                    </div>
                """, unsafe_allowed_html=True)
        else:
            st.markdown("<p style='color:#8A99AD; font-family:monospace;'>NO RECENT FINANCIAL RECORDS DETECTED FOR THIS VECTOR</p>", unsafe_allowed_html=True)

    # Right Split Column: Geopolitical Tracking Data
    with right_column:
        st.markdown("<div class='module-header-pol'>Political News Feed</div>", unsafe_allowed_html=True)
        political_response = newsapi.get_everything(
            q=f'"{active_country}" AND (politics OR government OR election OR tariff OR regulation)',
            language='en', sort_by='publishedAt', page_size=3
        )
        
        if political_response['articles']:
            for post in political_response['articles']:
                snippet = post['description'] if post['description'] else "Abstract brief unavailable for this node entry."
                st.markdown(f"""
                    <div class="premium-card-pol">
                        <div class="item-title">{post['title']}</div>
                        <div class="item-meta">INDEX: {post['source']['name']} // DATETIME: {post['publishedAt'][:10]}</div>
                        <div class="item-desc">{snippet}</div>
                        <a class="terminal-btn" href="{post['url']}" target="_blank">RESOLVE DOSSIER</a>
                    </div>
                """, unsafe_allowed_html=True)
        else:
            st.markdown("<p style='color:#8A99AD; font-family:monospace;'>NO RECENT POLITICAL RECORDS DETECTED FOR THIS VECTOR</p>", unsafe_allowed_html=True)

except Exception as e:
    st.markdown("<div style='font-family:monospace; color:#8A99AD; padding:20px; border:1px dashed #30363D;'>SYSTEM REFRESH REQUIRED // VALIDATE ADVANCED CONFIGURATION SECRETS</div>", unsafe_allowed_html=True)
