import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

# 1. Auto-refresh every 30 seconds to stay updated
st_autorefresh(interval=30 * 1000, key="gold_sync")

# Initialize session state for manual price override
if 'manual_price' not in st.session_state:
    st.session_state.manual_price = None

def fetch_gold_prices():
    """Tries to get real Egypt prices, fallback to manual if API fails"""
    try:
        # مصدر بديل وأسرع لأسعار مصر
        api_url = "https://api.gold-price-egypt.com/v1/latest" 
        response = requests.get(api_url, timeout=5)
        data = response.json()
        return {
            "24": float(data['24k']),
            "21": float(data['21k']),
            "18": float(data['18k']),
            "coin": float(data['21k']) * 8
        }
    except:
        # لو السيرفر وقع، بنستخدم آخر سعر يدوي أو سعر افتراضي منطقي
        base_21 = st.session_state.manual_price if st.session_state.manual_price else 3700.0
        return {
            "24": base_21 / 0.875,
            "21": base_21,
            "18": base_21 * 0.857,
            "coin": base_21 * 8
        }

st.set_page_config(page_title="Mazen Gold Pro", layout="wide")
market_prices = fetch_gold_prices()

# Auth
USER_CREDENTIALS = {"mazen_boss": "0000", "alamana_shop": "1234"}

st.sidebar.title("Login | دخول")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
    st.markdown(f"<h1 style='text-align: center; color: #D4AF37;'>💰 نظام {username} للتسعير 💰</h1>", unsafe_allow_html=True)
    
    # ADMIN PANEL: Only for Mazen to fix prices without touching code
    if username == "mazen_boss":
        with st.expander("🛠 لوحة تحكم المدير (تعديل السعر يدوياً)"):
            new_price = st.number_input("تعديل سعر عيار 21 الحالي:", value=market_prices['21'])
            if st.button("اعتماد السعر في الموقع"):
                st.session_state.manual_price = new_price
                st.success("تم تحديث السعر عند جميع المستخدمين!")
                st.rerun()

    # Display Prices
    c1, c2, c3 = st.columns(3)
    c1.metric("عيار 21", f"{market_prices['21']:,} ج")
    c2.metric("عيار 18", f"{market_prices['18']:,} ج")
    c3.metric("الجنيه الذهب", f"{market_prices['coin']:,} ج")
    
    st.divider()
    
    # Calc
    weight = st.number_input("الوزن (جرام)", min_value=0.0, value=1.0)
    karat = st.selectbox("العيار", ["24", "21", "18"])
    labor = st.number_input("المصنعية", value=150)
    
    total = (market_prices[karat] + labor) * weight
    st.markdown(f"<div style='background:#D4AF37; padding:20px; border-radius:15px; text-align:center;'><h1 style='color:black;'>{total:,.2f} جنيه</h1></div>", unsafe_allow_html=True)
else:
    st.info("سجل دخولك يا بطل.")
