import streamlit as st
import requests

# Настройка страницы
st.set_page_config(layout="wide")

st.title("SovereignDebt Pulse")
st.caption("A premium geopolitical intelligence framework for tracking systemic market risk.")

# Надежный выпадающий список для выбора стран
active_country = st.selectbox(
    "Select Target Vector Node", 
    ["United States", "United Kingdom", "Japan", "Germany", "France", "Canada", "Australia", "India", "Brazil", "South Africa"]
)

st.write(f"### Current Node Analysis: {active_country}")

# Создаем две колонки 50/50
left_column, right_column = st.columns(2)

try:
    # Берем ключ из настроек Secrets
    api_key = st.secrets["GNEWS_API_KEY"]
    
    # ЛЕВАЯ КОЛОНКА: Финансовые новости
    with left_column:
        st.subheader("Financial News Feed")
        fin_url = f'https://gnews.io"{active_country}" AND (finance OR economy OR "central bank" OR bonds)&lang=en&max=3&apikey={api_key}'
        fin_data = requests.get(fin_url).json()
        
        if 'articles' in fin_data and fin_data['articles']:
            for post in fin_data['articles']:
                with st.container(border=True): # Красивая встроенная рамка
                    st.markdown(f"**{post['title']}**")
                    st.caption(f"Source: {post['source']['name']} | Date: {post['publishedAt'][:10]}")
                    st.write(post['description'] if post['description'] else "No summary available.")
                    st.link_button("Access Financial Report", post['url'])
        else:
            st.info("No recent financial records detected for this vector node.")

    # ПРАВАЯ КОЛОНКА: Политические новости
    with right_column:
        st.subheader("Political News Feed")
        pol_url = f'https://gnews.io"{active_country}" AND (politics OR government OR tariff OR regulation)&lang=en&max=3&apikey={api_key}'
        pol_data = requests.get(pol_url).json()
        
        if 'articles' in pol_data and pol_data['articles']:
            for post in pol_data['articles']:
                with st.container(border=True): # Красивая встроенная рамка
                    st.markdown(f"**{post['title']}**")
                    st.caption(f"Source: {post['source']['name']} | Date: {post['publishedAt'][:10]}")
                    st.write(post['description'] if post['description'] else "No tactical overview available.")
                    st.link_button("Access Political Dossier", post['url'])
        else:
            st.info("No recent political records detected for this vector node.")

except Exception as e:
    st.error("System configuration requires an active GNEWS_API_KEY parameter in Advanced Settings.")
