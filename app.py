import streamlit as st
import random

st.set_page_config(page_title="ميشو", page_icon="🎯", layout="wide", initial_sidebar_state="collapsed")

# CSS البسيط والمضمون (بدون تعقيدات تكسر المتصفح)
st.markdown("""
<style>
    /* إجبار الأزرار تكون دائرية ومرتبة */
    .stButton > button {
        width: 100% !important;
        aspect-ratio: 1 !important;
        border-radius: 50% !important;
        padding: 0 !important;
        border: 1px solid #333 !important;
        background: #111 !important;
        color: #fff !important;
        font-weight: bold !important;
    }
    /* ألوان التحديد */
    .sel-1 { background: #0066ff !important; }
    .sel-2 { background: #00a844 !important; }
    .sel-both { background: linear-gradient(135deg, #0066ff 50%, #00a844 50%) !important; }
</style>
""", unsafe_allow_html=True)

if "c1" not in st.session_state: st.session_state.c1 = set()
if "c2" not in st.session_state: st.session_state.c2 = set()
if "tab" not in st.session_state: st.session_state.tab = 1

# تقسيم الـ 90 رقم إلى 9 صفوف (كل صف 10 أزرار)
for r in range(9):
    cols = st.columns(10)
    for c in range(10):
        n = r * 10 + c + 1
        with cols[c]:
            # تحديد الحالة
            cls = ""
            if n in st.session_state.c1 and n in st.session_state.c2: cls = "sel-both"
            elif n in st.session_state.c1: cls = "sel-1"
            elif n in st.session_state.c2: cls = "sel-2"
            
            # زر ستريمليت الأصلي (سريع ولا يسوي رفرش)
            if st.button(str(n), key=f"btn_{n}"):
                tab = st.session_state.tab
                sel = st.session_state.c1 if tab == 1 else st.session_state.c2
                if n in sel: sel.discard(n)
                else: sel.add(n)
                st.rerun()