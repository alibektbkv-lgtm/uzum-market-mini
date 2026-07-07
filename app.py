 import streamlit as st
import pandas as pd
import os

# Sahifa sozlamalari
st.set_page_config(page_title="Uzum Market Pro", page_icon="🛍️", layout="wide")

# API kalitlari yoki qo'shimcha sozlamalar (kerak bo'lsa)
# Loyihangiz kelajakda kengayishi uchun tayyor joy

# CSS dizayn kodlari (Uzum Market binafsha va sariq ranglari)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        background-color: #7000ff;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 8px 16px;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover { background-color: #5b00d6; color: white; }
    .savat-btn>button {
        background-color: #ffc107;
        color: #212529;
    }
    .savat-btn>button:hover { background-color: #e0a800; color: #212529; }
    .tovar-card {
        background-color: white;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        height: 100%;
    }
    .narx { font-size: 18px; font-weight: bold; color: #1f2026; }
    .oylik { font-size: 12px; background-color: #fffae6; color: #f2994a; padding: 2px 6px; border-radius: 4px; display: inline-block; font-weight: bold; }
    .tovar-nomi { font-size: 14px; color: #1f2026; margin-top: 10px; height: 40px; overflow: hidden; }
    </style>
""", unsafe_allow_html=True)

# Savat tizimini ishga tushirish
if 'savat' not in st.session_state:
    st.session_state.savat = {}

# SESSYADAGI FUNKSIYALAR
def savatga_qush(tovar_id, tovar_nomi, tovar_narxi):
    if tovar_id in st.session_state.savat:
        st.session_state.savat[tovar_id]['soni'] += 1
    else:
        st.session_state.savat[tovar_id] = {'nomi': tovar_nomi, 'narxi': tovar_narxi, 'soni': 1}

def savatdan_kamaytirish(tovar_id):
    if tovar_id in st.session_state.savat:
        st.session_state.savat[tovar_id]['soni'] -= 1
        if st.session_state.savat[tovar_id]['soni'] <= 0:
            del st.session_state.savat[tovar_id]

def savatni_tozalash():
    st.session_state.savat = {}

# BAZA BILAN ISHLASH (CSV FAYLDAN MA'LUMOTLARNI O'QISH)
EXCEL_FILE = "mahsulotlar.csv"

if os.path.exists(EXCEL_FILE):
    try:
        df = pd.read_csv(EXCEL_FILE)
    except Exception as e:
        st.error(f"Faylni o'qishda xatolik: {e}")
        df = pd.DataFrame()
else:
    st.error("mahsulotlar.csv fayli topilmadi!")
    df = pd.DataFrame()

# TEPADA ASOSIY PANEL
col_title, col_cart = st.columns([3, 1])

with col_title:
    st.markdown("<div style='background-color: #7000ff; padding: 15px; border-radius: 10px; color: white; font-size: 24px; font-weight: bold;'>🛍️ Uzum Market Pro — 500+ Tovar Tizimi</div>", unsafe_allow_html=True)

# SAVATNING UMUMIY HISOB-KITOBI
jami_tovar_soni = sum(item['soni'] for item in st.session_state.savat.values())
jami_summa = sum(item['narxi'] * item['soni'] for item in st.session_state.savat.values())

with col_cart:
    st.markdown(f"<div style='background-color: #ffc107; padding: 18px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 16px;'>🛒 Savatda: {jami_tovar_soni} ta</div>", unsafe_allow_html=True)

# QIDIRUV TIZIMI
qidiruv = st.text_input("🔍 Mahsulotlarni qidirish...", "")

# KATEGORIYALAR (CHAKANA / OPTOM)
tab1, tab2 = st.tabs(["🔥 Chakana savdo", "📦 OPTOM BO'LIMI"])

# TOVARLARNI EKRAVGA CHIQARISH FUNKSIYASI
def tovarlarni_kursat (data, tur):
    if data.empty:
        st.info("Hozircha mahsulotlar yo'q.")
        return
    
    # Faqat mos keladigan toifani filtrlash
    filtr_df = data[data['toifa'] == tur]
    
    # Qidiruv bo'yicha filtrlash
    if qidiruv:
        filtr_df = filtr_df[filtr_df['nomi'].str.contains(qidiruv, case=False, na=False)]
        
    if filtr_df.empty:
        st.warning("Hech qanday mahsulot topilmadi.")
        return

    # 4 ta ustunli setka yaratish
    rows = len(filtr_df) // 4 + 1
    for r in range(rows):
        cols = st.columns(4)
        for c in range(4):
            idx = r * 4 + c
            if idx < len(filtr_df):
                row = filtr_df.iloc[idx]
                with cols[c]:
                    st.markdown(f"""
                        <div class="tovar-card">
                            <img src="{row['rasm']}" style="width:100%; height:180px; object-fit:contain; border-radius:8px;">
                            <div class="narx">{int(row['narxi']):,} so'm</div>
                            <div class="oylik">{row['oylik']}</div>
                            <div class="tovar-nomi">{row['nomi']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Savatga qo'shish tugmasi
                    if st.button(f"🛒 Savatga", key=f"btn_{row['id']}"):
                        savatga_qush(row['id'], row['nomi'], int(row['narxi']))
                        st.rerun()

# TABLAR ICHIDA KO'RSATISH
with tab1:
    tobarlar_data = df.copy() if not df.empty else pd.DataFrame()
    tovarlarni_kursat(tobarlar_data, "chakana")

with tab2:
    tovarlarni_kursat(tobarlar_data, "optom")

# YON PANEL (SIDEBAR) ICHIDA SAVAT MA'LUMOTLARINI KO'RSATISH
if jami_tovar_soni > 0:
    st.sidebar.markdown("### 🛒 Sizning savatingiz")
    for tid, item in st.session_state.savat.items():
        st.sidebar.markdown(f"**{item['nomi']}**")
        st.sidebar.write(f"{item['soni']} ta x {item['narxi']:,} so'm = {item['soni']*item['narxi']:,} so'm")
        
        col_minus, col_plus = st.sidebar.columns(2)
        with col_minus:
            if st.button("➖ Kamaytirish", key=f"min_{tid}"):
                savatdan_kamaytirish(tid)
                st.rerun()
        with col_plus:
            if st.button("➕ Ko'paytirish", key=f"pls_{tid}"):
                savatga_qush(tid, item['nomi'], item['narxi'])
                st.rerun()
        st.sidebar.markdown("---")
        
    st.sidebar.markdown(f"### 💰 Jami: {jami_summa:,} so'm")
    
    if st.sidebar.button("✅ Buyurtmani rasmiylashtirish", type="primary"):
        st.balloons()
        st.sidebar.success("🎉 Buyurtmangiz muvaffaqiyatli qabul qilindi!")
        savatni_tozalash()
        
    if st.sidebar.button("🗑️ Savatni bo'shatish"):
        savatni_tozalash()
        st.rerun()
else:
    st.sidebar.markdown("### 🛒 Savatingiz hozircha bo'sh")
