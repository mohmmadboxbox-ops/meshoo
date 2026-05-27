import streamlit as st
import random

st.set_page_config(page_title="ميشو", page_icon="🎯", layout="wide", initial_sidebar_state="collapsed")

# ── CSS (الخدعة الذكية لتطويع Streamlit) ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] { background: #0a0a0f !important; font-family: 'Tajawal', sans-serif !important; direction: rtl; }
.block-container { padding: 16px 8px 40px !important; max-width: 520px !important; margin: 0 auto !important; }
header, footer, #MainMenu { display: none !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }
.element-container { margin: 0 !important; padding: 0 !important; min-height: 0 !important; }

/* العناوين والعداد */
.misho-title { font-size: 2.2rem; font-weight: 900; letter-spacing: 4px; text-align: center; background: linear-gradient(135deg, #00d4ff, #7b2fff, #ff6b35); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 4px; }
.misho-subtitle { font-size: 0.8rem; color: #555; letter-spacing: 2px; text-transform: uppercase; text-align: center; margin-bottom: 16px;}
.counter-wrap { display: flex; align-items: center; justify-content: space-between; margin: 14px 0; padding: 10px 16px; background: #13131a; border-radius: 14px; border: 1px solid #1e1e2e; }
.counter-label { font-size: 0.8rem; color: #666; }
.counter-num { font-size: 1.5rem; font-weight: 900; color: #fff; }
.counter-num span { font-size: 0.9rem; color: #444; }
.counter-bar-bg { flex: 1; margin: 0 12px; height: 6px; background: #1e1e2e; border-radius: 99px; overflow: hidden; }
.counter-bar-fill { height: 100%; border-radius: 99px; transition: width 0.3s; }
.bar-1 { background: linear-gradient(90deg, #0066ff, #00d4ff); }
.bar-2 { background: linear-gradient(90deg, #00a844, #00ff88); }

/* ── إجبار الأعمدة على البقاء كشبكة أفقية بالموبايل ── */
[data-testid="stHorizontalBlock"]:has(.btn-marker),
[data-testid="stHorizontalBlock"]:has(.tab-marker),
[data-testid="stHorizontalBlock"]:has(.act-marker) {
    flex-direction: row-reverse !important; /* من اليمين لليسار */
    flex-wrap: nowrap !important;
}
[data-testid="stHorizontalBlock"]:has(.btn-marker) > [data-testid="column"],
[data-testid="stHorizontalBlock"]:has(.tab-marker) > [data-testid="column"],
[data-testid="stHorizontalBlock"]:has(.act-marker) > [data-testid="column"] {
    width: auto !important; flex: 1 1 0px !important; min-width: 0 !important; padding: 0 !important;
}

/* 1. تصميم التابات */
[data-testid="stHorizontalBlock"]:has(.tab-marker) { gap: 8px !important; margin-bottom: 14px !important; }
div.element-container:has(> .tab-marker) + div.element-container div.stButton > button { width: 100% !important; border-radius: 10px !important; padding: 10px !important; background: #13131a !important; color: #555 !important; border: 1px solid #1e1e2e !important; font-family: 'Tajawal' !important; font-weight: 700 !important; }
div.element-container:has(> .tab-marker.active-1) + div.element-container div.stButton > button { background: linear-gradient(135deg, #0066ff, #00d4ff) !important; color: #fff !important; border: none !important; box-shadow: 0 0 14px #0066ff55 !important; }
div.element-container:has(> .tab-marker.active-2) + div.element-container div.stButton > button { background: linear-gradient(135deg, #00a844, #00ff88) !important; color: #fff !important; border: none !important; box-shadow: 0 0 14px #00a84455 !important; }

/* 2. تصميم أزرار الأرقام (الدوائر) */
[data-testid="stHorizontalBlock"]:has(.btn-marker) { gap: 4px !important; margin-bottom: 4px !important; }
div.element-container:has(> .btn-marker) + div.element-container div.stButton > button {
    width: 100% !important; aspect-ratio: 1 !important; border-radius: 50% !important; padding: 0 !important;
    font-size: clamp(0.55rem, 2.4vw, 0.85rem) !important; font-weight: 700 !important;
    border: 1.5px solid #1e1e2e !important; background: #13131a !important; color: #444 !important;
    box-shadow: none !important; min-height: unset !important; transition: 0.15s !important;
}
div.element-container:has(> .btn-marker) + div.element-container div.stButton > button:active { transform: scale(0.8) !important; }
div.element-container:has(> .btn-marker.sel-1) + div.element-container div.stButton > button { background: #0066ff !important; border-color: #00d4ff !important; color: #fff !important; box-shadow: 0 0 8px #0066ff88 !important; }
div.element-container:has(> .btn-marker.sel-2) + div.element-container div.stButton > button { background: #00a844 !important; border-color: #00ff88 !important; color: #fff !important; box-shadow: 0 0 8px #00a84488 !important; }
div.element-container:has(> .btn-marker.sel-both) + div.element-container div.stButton > button { background: linear-gradient(135deg, #0066ff 50%, #00a844 50%) !important; border-color: #888 !important; color: #fff !important; box-shadow: 0 0 10px #ffffff33 !important; }
div.element-container:has(> .btn-marker.locked) + div.element-container div.stButton > button { opacity: 0.25 !important; pointer-events: none !important; }

/* 3. تصميم أزرار الإجراءات */
[data-testid="stHorizontalBlock"]:has(.act-marker) { gap: 8px !important; margin-top: 12px !important; }
div.element-container:has(> .act-marker) + div.element-container div.stButton > button { width: 100% !important; border-radius: 12px !important; padding: 12px 4px !important; font-size: 0.85rem !important; font-family: 'Tajawal' !important; font-weight: 700 !important; color: #fff !important; }
div.element-container:has(> .act-marker.btn-reset) + div.element-container div.stButton > button { background: #1e1e2e !important; color: #888 !important; border: 1px solid #2a2a3e !important; }
div.element-container:has(> .act-marker.btn-gen) + div.element-container div.stButton > button { background: linear-gradient(135deg, #7b2fff, #ff6b35) !important; border: none !important; box-shadow: 0 0 16px #7b2fff55 !important; }
div.element-container:has(> .act-marker.btn-gen-off) + div.element-container div.stButton > button { background: #111 !important; color: #444 !important; border: 1px solid #222 !important; pointer-events: none !important; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──
if "c1" not in st.session_state: st.session_state.c1 = set()
if "c2" not in st.session_state: st.session_state.c2 = set()
if "tab" not in st.session_state: st.session_state.tab = 1
if "cards" not in st.session_state: st.session_state.cards = []
if "show" not in st.session_state: st.session_state.show = False

MAX = 50
c1, c2 = st.session_state.c1, st.session_state.c2
tab = st.session_state.tab
sel = c1 if tab == 1 else c2
count = len(sel)
is_full = count >= MAX
can_gen = len(c1) == MAX and len(c2) == MAX

# ── العناوين ──
st.markdown('<div class="misho-title">ميشو</div><div class="misho-subtitle">لوحة الأرقام</div>', unsafe_allow_html=True)

# ── التابات ──
t1, t2 = st.columns(2)
with t1:
    st.markdown(f'<span class="tab-marker {"active-1" if tab==1 else ""}" style="display:none;"></span>', unsafe_allow_html=True)
    if st.button(f"البطاقة الأولى ({len(c1)})", key="tab1"):
        st.session_state.tab = 1; st.rerun()
with t2:
    st.markdown(f'<span class="tab-marker {"active-2" if tab==2 else ""}" style="display:none;"></span>', unsafe_allow_html=True)
    if st.button(f"البطاقة الثانية ({len(c2)})", key="tab2"):
        st.session_state.tab = 2; st.rerun()

# ── العداد ──
st.markdown(f"""
<div class="counter-wrap">
    <span class="counter-label">{'البطاقة الأولى' if tab==1 else 'البطاقة الثانية'}</span>
    <span class="counter-num">{count}<span>/{MAX}</span></span>
    <div class="counter-bar-bg"><div class="counter-bar-fill {'bar-1' if tab==1 else 'bar-2'}" style="width:{int(count/MAX*100) if MAX > 0 else 0}%"></div></div>
</div>
""", unsafe_allow_html=True)

# ── شبكة الأرقام السريعة ──
for r in range(9):
    cols = st.columns(10)
    for c in range(10):
        n = r * 10 + c + 1
        i1, i2 = n in c1, n in c2
        locked = is_full and (n not in sel)
        
        cls = "sel-both" if i1 and i2 else "sel-1" if i1 else "sel-2" if i2 else ""
        if locked: cls += " locked"
        
        with cols[c]:
            # زرع العلامة المخفية للربط مع CSS
            st.markdown(f'<span class="btn-marker {cls}" style="display:none;"></span>', unsafe_allow_html=True)
            if st.button(str(n), key=f"btn_{n}"):
                if not locked:
                    if n in sel: sel.discard(n)
                    else: sel.add(n)
                    st.session_state.cards = []; st.session_state.show = False
                    st.rer