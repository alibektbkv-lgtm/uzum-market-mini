import streamlit as st
import pandas as pd
import os

# Sahifa sozlamalari
st.set_page_config(page_title="Uzum Market Pro", page_icon="🛍️", layout="wide")

# Savatcha xotirasi
if "savatcha" not in st.session_state:
    st.session_state.savatcha = []

# CSS dizayn
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #f9f9fa;
    }
    .brand-box {
        background-color: #7000ff;
        color: white;
        padding: 15px;
        border-radius: 12px;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .product-card {
        background: white;
        border-radius: 12px;
        padding: 12px;
        border: 1px solid #e2e8f0;
        margin-bottom: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.02);
    }
    .product-image {
        width: 100%;
        border-radius: 8px;
        aspect-ratio: 1 / 1;
        object-fit: cover;
    }
    .price-main {
        font-size: 18px;
        font-weight: 700;
        color: #1f293d;
        margin-top: 8px;
    }
    .price-monthly {
        background-color: #fffae6;
        color: #6b5000;
        font-size: 11px;
        font-weight: 600;
        padding: 2px 6px;
        border-radius: 4px;
        display: inline-block;
    }
    .product-title {
        font-size: 13px;
        color: #2d3a50;
        height: 38px;
        overflow: hidden;
        margin-top: 5px;
    }
    .optom-tag {
        background-color: #27ae60;
        color: white;
        font-size: 11px;
        font-weight: bold;
        padding: 2px 6px;
        border-radius: 4px;
        display: inline-block;
    }
    div.stButton > button {
        background-color: #7000ff !important;
        color: white !important;
        border-radius: 8px !important;
        width: 100% !important;
        border: none !important;
        padding: 6px 0px !important;
    }
</style>
""", unsafe_allow_html=True)

# EXCEL FAYLDAN MA'LUMOTLARNI O'QISH
EXCEL_FILE = "mahsulotlar.csv"

if os.path.exists(EXCEL_FILE):
    try:
        df = pd.read_excel(EXCEL_FILE)
        # Ustunlar borligini tekshirish
        for col in ['id', 'toifa', 'nomi', 'narxi', 'oylik', 'rasm']:
            if col not in df.columns:
                df[col] = ""
        chakana_tovarlar = df[df['toifa'] == 'chakana'].to_dict(orient='records')
        optom_tovarlar = df[df['toifa'] == 'optom'].to_dict(orient='records')
    except Exception as e:
        st.error(f"Excel faylini o'qishda xato: {e}")
        st.stop()
else:
    st.error(f"Xato: Papkada '{EXCEL_FILE}' fayli topilmadi!")
    st.stop()

# TEPADAGI PANEL
col_top1, col_top2 = st.columns([3, 1])
with col_top1:
    st.markdown('<div class="brand-box">🛍️ Uzum Market Pro — 500+ Tovar Tizimi</div>', unsafe_allow_html=True)
with col_top2:
    savat_soni = len(st.session_state.savatcha)
    st.markdown(f"<div style='background-color: #ffb800; color: #1f293d; padding: 15px; border-radius: 12px; text-align: center; font-weight: bold; font-size: 18px;'>🛒 Savatda: {savat_soni} ta</div>", unsafe_allow_html=True)

# QIDIRUV TIZIMI
qidiruv = st.text_input("🔍 Mahsulotlarni qidirish...", "")

# Bo'limlar
tab1, tab2 = st.tabs(["🔥 Chakana savdo", "📦 OPTOM BO'LIMI"])

def mahsulotlarni_chiqarish(tovarlar_royxati, is_optom=False):
    if qidiruv:
        tovarlar_royxati = [t for t in tovarlar_royxati if qidiruv.lower() in str(t['nomi']).lower()]
        
    if not tovarlar_royxati:
        st.warning("Hech qanday mahsulot topilmadi.")
        return

    for i in range(0, len(tovarlar_royxati), 4):
        qator = tovarlar_royxati[i:i+4]
        cols = st.columns(4)
        for idx, item in enumerate(qator):
            with cols[idx]:
                tag_html = f'<div class="optom-tag">📦 OPTOM</div>' if is_optom else f'<div class="price-monthly">{item.get("oylik", "")}</div>'
                try:
                    narx_val = int(item.get('narxi', 0))
                    narx_str = f"{narx_val:,} so'm"
                except:
                    narx_str = f"{item.get('narxi', 0)} so'm"
                
                rasm_url = item.get('rasm', 'https://via.placeholder.com/400')
                if pd.isna(rasm_url) or not str(rasm_url).startswith('http'):
                    rasm_url = 'https://via.placeholder.com/400'

                st.markdown(f"""
                <div class="product-card">
                    <img src="{rasm_url}" class="product-image">
                    <div class="price-main">{narx_str}</div>
                    {tag_html}
                    <div class="product-title">{item.get('nomi', 'Nomsiz tovar')}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("🛒 Savatga", key=str(item.get('id', idx)) + ("_optom" if is_optom else "_chakana")):
                    st.session_state.savatcha.append(item)
                    st.rerun()

with tab1:
    mahsulotlarni_chiqarish(chakana_tovarlar, is_optom=False)

with tab2:
    mahsulotlarni_chiqarish(optom_tovarlar, is_optom=True)

st.markdown("---")

# SAVATCHA HISOB-KITOBI
st.subheader("🧾 Buyurtmalarni hisoblash")
if len(st.session_state.savatcha) == 0:
    st.info("Savatchangiz bo'sh.")
else:
    c_s1, c_s2 = st.columns([2, 1])
    jami = 0
    with c_s1:
        for tovar in st.session_state.savatcha:
            try:
                n_val = int(tovar.get('narxi', 0))
                st.write(f"• **{tovar.get('nomi', 'Tovar')}** — {n_val:,} so'm")
                jami += n_val
            except:
                st.write(f"• **{tovar.get('nomi', 'Tovar')}**")
    with c_s2:
        st.markdown(f"### Jami summa: {jami:,} so'm")
        if st.button("✅ Rasmiylashtirish"):
            st.balloons()
            st.success("🎉 Buyurtma qabul qilindi!")
            st.session_state.savatcha = []
            st.rerun()
