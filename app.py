import streamlit as st
import plotly.express as px
import pandas as pd
from newsapi import NewsApiClient

# Layout configuration
st.set_page_config(layout="wide")
st.title("SovereignDebt Pulse")
st.write("Select a coordinate point on the world map to view country-specific financial datasets and regional political news side-by-side.")

# Map data initialization 
map_data = pd.DataFrame({
    'Country': ['United States', 'United Kingdom', 'Japan', 'Germany'],
    'Latitude': [37.0902, 55.3781, 36.2048, 51.1657],
    'Longitude': [-95.7129, -3.4360, 138.2529, 10.4515]
})

# Render a minimal global dark map layout
fig = px.scatter_geo(
    map_data,
    lat='Latitude',
    lon='Longitude',
    hover_name='Country',
    projection='natural earth',
    title='Global Intelligence Coordinates'
)

fig.update_layout(
    template='plotly_dark',
    geo=dict(
        showland=True, landcolor='#1E1E1E',
        showocean=True, oceancolor='#0E1117',
        showcountries=True, countrycolor='#333333'
    ),
    margin=dict(l=0, r=0, t=40, b=0)
)
fig.update_traces(marker=dict(size=12, color='#00D4B2', symbol='circle'))

# Display map on frontend and listen for user click coordinates
selected_points = st.plotly_chart(fig, use_container_width=True, on_select="rerun")

# Default country choice when nothing is clicked
target_country = "United States"

# Detect interactive clicks on map nodes
if selected_points and "selection" in selected_points and selected_points["selection"]["points"]:
    point_index = selected_points["selection"]["points"][0]["point_number"]
    target_country = map_data.iloc[point_index]['Country']

st.write(f"### Current Node Analysis: {target_country}")

# Split screen columns
left_col, right_col = st.columns(2)

try:
    newsapi = NewsApiClient(api_key=st.secrets["NEWS_API_KEY"])
    
    # Column 1: Financial News Panel
    with left_col:
        st.subheader("Financial Dataset")
        fin_data = newsapi.get_everything(
            q=f"{target_country} AND (finance OR economy OR central bank OR bonds)",
            language='en', sort_by='publishedAt', page_size=3
        )
        for article in fin_data['articles']:
            with st.container(border=True):
                st.markdown(f"**{article['title']}**")
                st.caption(f"Source: {article['source']['name']} | Date: {article['publishedAt'][:10]}")
                st.write(article['description'] if article['description'] else "Metadata unavailable.")
                st.link_button("Open Source Link", article['url'])

    # Column 2: Political Briefing Panel
    with right_col:
        st.subheader("Political Briefing")
        pol_data = newsapi.get_everything(
            q=f"{target_country} AND (politics OR government OR election OR policy)",
            language='en', sort_by='publishedAt', page_size=3
        )
        for article in pol_data['articles']:
            with st.container(border=True):
                st.markdown(f"**{article['title']}**")
                st.caption(f"Source: {article['source']['name']} | Date: {article['publishedAt'][:10]}")
                st.write(article['description'] if article['description'] else "Metadata unavailable.")
                st.link_button("Open Source Link", article['url'])

except Exception as e:
    st.info("System configuration requires an active NEWS_API_KEY inside the Advanced Settings panel to populate data pipelines.")
