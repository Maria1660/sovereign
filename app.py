import streamlit as st
import urllib.parse
import xml.etree.ElementTree as ET
import requests

# Настройка широкого экрана
st.set_page_config(layout="wide")

st.title("SovereignDebt Pulse")
st.caption("A premium geopolitical intelligence framework for tracking systemic market risk.")

# Безотказный выпадающий список стран
active_country = st.selectbox(
    "Select Target Vector Node", 
    ["United States", "United Kingdom", "Japan", "Germany", "France", "Canada", "Australia", "India", "Brazil", "South Africa"]
)

st.write(f"### Selected Target Vector: {active_country}")

# Создаем две колонки 50 на 50 с помощью встроенных средств
left_column, right_column = st.columns(2)

# Встроенный парсер открытых RSS новостей (работает без ключей)
def get_clean_news(search_term):
    news_list = []
    try:
        query = urllib.parse.quote(search_term)
        rss_url = f"https://google.com{query}&hl=en-US&gl=US&ceid=US:en"
        raw_xml = requests.get(rss_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=7).text
        xml_tree = ET.fromstring(raw_xml)
        
        for item in xml_tree.findall('.//item')[:3]:  # Ровно 3 самые свежие новости
            raw_title = item.find('title').text if item.find('title') is not None else "Breaking News"
            url_link = item.find('link').text if item.find('link') is not None else "#"
            date_published = item.find('pubDate').text if item.find('pubDate') is not None else "Live"
            media_source = item.find('source').text if item.find('source') is not None else "Global Media"
            
            # Удаляем хвост с названием источника из заголовка
            if " - " in raw_title:
                raw_title = raw_title.rsplit(" - ", 1)[0]
                
            news_list.append({
                "title": raw_title,
                "url": url_link,
                "date": date_published[:16],
                "source": media_source
            })
    except:
        pass
    return news_list

# Левая колонка: Финансы
with left_column:
    st.subheader("Financial News Feed")
    financial_data = get_clean_news(f"{active_country} finance economy")
    
    if financial_data:
        for article in financial_data:
            with st.container(border=True):  # Используем только встроенные рамки Streamlit
                st.markdown(f"### {article['title']}")
                st.caption(f"INDEX: {article['source']} // DATETIME: {article['date']}")
                st.write("Access real-time global financial report arrays for structural macroeconomic trends within this sector node.")
                st.link_button("RESOLVE REPORT", article['url'], use_container_width=True)
    else:
        st.info("NO RECENT FINANCIAL RECORDS DETECTED FOR THIS VECTOR")

# Правая колонка: Политика
with right_column:
    st.subheader("Political News Feed")
    political_data = get_clean_news(f'{active_country} AND (politics OR government OR tariff OR legislation)')
    
    if political_data:
        for article in political_data:
            with st.container(border=True):  # Используем только встроенные рамки Streamlit
                st.markdown(f"### {article['title']}")
                st.caption(f"INDEX: {article['source']} // DATETIME: {article['date']}")
                st.write("Access tactical geopolitical intelligence briefings regarding legislative changes and executive state actions.")
                st.link_button("RESOLVE DOSSIER", article['url'], use_container_width=True)
    else:
        st.info("NO RECENT POLITICAL RECORDS DETECTED FOR THIS VECTOR")
