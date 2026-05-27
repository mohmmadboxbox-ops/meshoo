import streamlit as st

st.set_page_config(page_title="ميشو", layout="centered")

# CSS خفيف جداً يركز بس على شكل الأزرار الدائري
st.markdown("""
<style>
    div[data-testid="stButton"] > button {
        width: 100% !important;
        aspect-ratio: 1 !important;
        border-radius: 50% !important;
        background-color: #111 !important;
        color: #fff !important;
        border: 1px solid #333 !important;
        font-size: 12px !important;
    }
    div[data-testid="stButton"] > button:active { background-color: #444 !important; }
</style>
""", unsafe_allow_html=True)

if "c1" not in st.session_state: st.session_state.c1 = set()

# عرض 90 رقم في شبكة (9 صفوف × 10 أعمدة)
for r in range(9):
    cols = st.columns(10)
    for c in range(10):
        n = r * 10 + c + 1
        with cols[c]:
            if st.button(str(n)):
                if n in st.session_state.c1: st.session_state.c1.discard(n)
                else: st.session_state.c1.add(n)
                st.rerun()