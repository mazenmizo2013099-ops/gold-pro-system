import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

# 1. Automatic refresh every 60 seconds
st_autorefresh(interval=60 * 1000, key="gold_price_refresh")

def fetch_gold_prices():
    try:
        api_url = "https://data-asg.goldpriceegypt.com/db.json"
        response = requests.get(api_url)
        data = response.json()
        return {
            "24": float(data['price']['24']),
            "21": float(data['price']['21']),
            "18": float(data['price']['18']),
            "coin": float(data['price']['21']) * 8
        }
    except:
        return {"24": 3500.0, "21": 3100.0, "18": 2650.0, "coin": 24800.0}

st.set_page_config(page_title="Mazen Gold System", layout="wide")
market_prices = fetch_gold_prices()

USER_CREDENTIALS = {"mazen_boss": "0000", "alamana_shop": "1234"}

st.sidebar.title("تسجيل الدخول")
username = st.sidebar.text_input("اسم المستخدم")
password = st.sidebar.text_input("كلمة السر", type="password")

if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
    st.markdown("<h1 style='text-align: center; color: #D4AF37;'>💰 نظام مازن للتسعير اللحظي 💰</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("عيار 21", f"{market_prices['21']:,} ج")
    col2.metric("عيار 18", f"{market_prices['18']:,} ج")
    col3.metric("الجنيه الذهب", f"{market_prices['coin']:,} ج")
    st.divider()
    input_weight = st.number_input("الوزن (جرام)", min_value=0.0, value=1.0)
    selected_karat = st.selectbox("العيار", ["24", "21", "18"])
    labor_fee = st.number_input("المصنعية للجرام الواحد (ج)", value=150)
    final_total = (market_prices[selected_karat] + labor_fee) * input_weight
    st.markdown(f"<div style='background-color:#D4AF37; padding:20px; border-radius:15px; text-align:center;'><h1 style='color:black;'>{final_total:,.2f} جنيه</h1></div>", unsafe_allow_html=True)
else:
    st.info("يرجى تسجيل الدخول.")
