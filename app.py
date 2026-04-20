import streamlit as st

# --- 1. بيانات الدخول ---
SHOPS_DATA = {
    "mazen_boss": {"pass": "0000", "role": "admin", "name": "المدير مازن"},
    "alamana_shop": {"pass": "1234", "role": "user", "name": "مجوهرات الأمانة"},
    "alhuda_shop": {"pass": "5678", "role": "user", "name": "صاغة الهدى"}
}

st.set_page_config(page_title="نظام مازن للذهب", layout="wide")

# --- 2. تسجيل الدخول ---
st.sidebar.title("🔐 دخول النظام")
user = st.sidebar.text_input("اسم المستخدم")
password = st.sidebar.text_input("كلمة السر", type="password")

if user in SHOPS_DATA and SHOPS_DATA[user]["pass"] == password:
    user_info = SHOPS_DATA[user]
    view_as = st.sidebar.selectbox("عرض كـ محل:", ["مجوهرات الأمانة", "صاغة الهدى"]) if user_info["role"] == "admin" else user_info["name"]

    st.markdown(f"<h1 style='text-align: center; color: #D4AF37;'>✨ {view_as} ✨</h1>", unsafe_allow_html=True)
    
    # السعر الأساسي
    gold_24 = 3500 
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("عيار 21", f"{gold_24 * 0.875:.0f} ج")
    with col2: st.metric("جنيه ذهب", f"{gold_24 * 8:.0f} ج")
    with col3: st.metric("سبيكة 10ج", f"{gold_24 * 10:.0f} ج")

    st.write("---")
    st.subheader("🧮 حاسبة المصنعية")
    c1, c2 = st.columns(2)
    with c1:
        weight = st.number_input("الوزن (جرام)", min_value=0.1, value=1.0)
        karat = st.selectbox("العيار", ["عيار 24", "عيار 21", "عيار 18"])
    with c2:
        labor = st.number_input("المصنعية", value=150)
        tax = st.number_input("الدمغة", value=50)

    # الحساب النهائي
    ratios = {"عيار 24": 1.0, "عيار 21": 0.875, "عيار 18": 0.75}
    unit_price = (gold_24 * ratios[karat]) + labor + tax
    total = unit_price * weight

    st.markdown(f"""
        <div style="background-color: #D4AF37; padding: 20px; border-radius: 10px; text-align: center;">
            <h1 style="color: black;">{total:,.2f} جنيه</h1>
        </div>
    """, unsafe_allow_html=True)
else:
    st.warning("دخل اليوزر والباسورد")
    st.stop()