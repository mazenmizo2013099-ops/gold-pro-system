import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

# تحديث تلقائي كل 30 ثانية
st_autorefresh(interval=30 * 1000, key="egy_gold_sync")

def fetch_local_egypt_price():
    """Fetches gold prices directly from Egyptian market sources"""
    try:
        # مصدر مصري محلي (بيحدث السعر بالجنيه)
        api_url = "https://data-asg.goldpriceegypt.com/db.json"
        response = requests.get(api_url, timeout=5)
        data = response.json()
        
        return {
            "24": float(data['price']['24']),
            "21": float(data['price']['21']),
            "18": float(data['price']['18']),
            "coin": float(data['price']['21']) * 8
        }
    except:
        # الأسعار الاحتياطية (لو السيرفر وقع) - عدل الأرقام دي "مرة واحدة" لأسعار النهاردة
        return {
            "24": 4114.0, 
            "21": 3600.0, 
            "18": 3086.0, 
            "coin": 28800.0
        }

# إعداد الصفحة
st.set_page_config(page_title="Mazen Gold Local", layout="wide")
prices = fetch_local_egypt_price()

# بيانات الدخول
USERS = {"mazen_boss": "0000", "alamana_shop": "1234"}

st.sidebar.title("دخول النظام")
user = st.sidebar.text_input("المستخدم")
pw = st.sidebar.text_input("الباسورد", type="password")

if user in USERS and USERS[user] == pw:
    st.markdown(f"<h1 style='text-align: center; color: #D4AF37;'>🇪🇬 بورصة {user} المحلية 🇪🇬</h1>", unsafe_allow_html=True)
    
    # عرض الأسعار في مربعات كبيرة
    c1, c2, c3 = st.columns(3)
    c1.metric("عيار 21 (صاغة)", f"{prices['21']:,} ج")
    c2.metric("عيار 18 (صاغة)", f"{prices['18']:,} ج")
    c3.metric("الجنيه الذهب", f"{prices['coin']:,} ج")
    
    st.divider()
    
    # حاسبة البيع والشراء
    st.subheader("🧮 حاسبة السعر النهائي")
    w = st.number_input("الوزن بالجرام", value=1.0, step=0.1)
    k = st.selectbox("العيار", ["24", "21", "18"])
    m = st.number_input("المصنعية للجرام (متوسط 150-200)", value=150)
    
    total = (prices[k] + m) * w
    st.markdown(f"""
        <div style='background:#D4AF37; padding:20px; border-radius:15px; text-align:center;'>
            <h2 style='color:black; margin:0;'>إجمالي المبلغ</h2>
            <h1 style='color:black; margin:10px 0;'>{total:,.2f} جنيه</h1>
        </div>
    """, unsafe_allow_html=True)
else:
    st.info("يرجى تسجيل الدخول لمتابعة أسعار الصاغة المصرية.")
