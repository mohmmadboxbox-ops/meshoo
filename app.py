import streamlit as st
import random

st.set_page_config(
    page_title="ميشو",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #0a0a0f !important;
    font-family: 'Tajawal', sans-serif !important;
    direction: rtl;
}
.block-container {
    padding: 16px 8px 40px !important;
    max-width: 520px !important;
    margin: 0 auto !important;
}
header, footer, #MainMenu { display: none !important; }

/* إزالة مسافات Streamlit الافتراضية لمنع التقطيع */
[data-testid="stVerticalBlock"] { gap: 0 !important; }
.element-container { margin: 0 !important; padding: 0 !important; min-height: 0 !important; }
[data-testid="stMarkdownContainer"] p { margin-bottom: 0 !important; }

/* ── تصميم العناوين والعداد ── */
.misho-title {
    font-size: 2.2rem; font-weight: 900; letter-spacing: 4px; text-align: center;
    background: linear-gradient(135deg, #00d4ff, #7b2fff, #ff6b35);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 4px;
}
.misho-subtitle { font-size: 0.8rem; color: #555; letter-spacing: 2px; text-transform: uppercase; text-align: center; margin-bottom: 16px;}

.counter-wrap {
    display: flex; align-items: center; justify-content: space-between;
    margin: 14px 0; padding: 10px 16px; background: #13131a; border-radius: 14px; border: 1px solid #1e1e2e;
}
.counter-label { font-size: 0.8rem; color: #666; }
.counter-num { font-size: 1.5rem; font-weight: 900; color: #fff; }
.counter-num span { font-size: 0.9rem; color: #444; }
.counter-bar-bg { flex: 1; margin: 0 12px; height: 6px; background: #1e1e2e; border-radius: 99px; overflow: hidden; }
.counter-bar-fill { height: 100%; border-radius: 99px; transition: width 0.3s; }
.bar-1 { background: linear-gradient(90deg, #0066ff, #00d4ff); }
.bar-2 { background: linear-gradient(90deg, #00a844, #00ff88); }

/* ── التابات والتحكم ── */
.tabs-wrapper [data-testid="stHorizontalBlock"] { display: flex !important; gap: 8px !important; }
.tab-btn div.stButton > button {
    width: 100% !important; border-radius: 10px !important; padding: 10px !important;
    background: #13131a !important; color: #555 !important; border: 1px solid #1e1e2e !important; font-family: 'Tajawal' !important; font-weight: 700 !important;
}
.tab-active-1 div.stButton > button { background: linear-gradient(135deg, #0066ff, #00d4ff) !important; color: #fff !important; border: none !important; box-shadow: 0 0 14px #0066ff55 !important; }
.tab-active-2 div.stButton > button { background: linear-gradient(135deg, #00a844, #00ff88) !important; color: #fff !important; border: none !important; box-shadow: 0 0 14px #00a84455 !important; }

.actions-wrapper [data-testid="stHorizontalBlock"] { display: flex !important; gap: 8px !important; margin-top: 12px !important; }
.action-btn div.stButton > button {
    width: 100% !important; padding: 12px 4px !important; border-radius: 12px !important;
    font-size: 0.85rem !important; font-family: 'Tajawal' !important; font-weight: 700 !important; color: #fff !important;
}
.btn-reset div.stButton > button { background: #1e1e2e !important; color: #888 !important; border: 1px solid #2a2a3e !important; }
.btn-gen div.stButton > button { background: linear-gradient(135deg, #7b2fff, #ff6b35) !important; border: none !important; box-shadow: 0 0 16px #7b2fff55 !important; }
.btn-gen-off div.stButton > button { background: #111 !important; color: #444 !important; border: 1px solid #222 !important; pointer-events: none !important; }

/* ── شبكة الأرقام (السر هنا) ── */
.num-grid-wrapper [data-testid="stHorizontalBlock"] {
    display: grid !important;
    grid-template-columns: repeat(10, 1fr) !important; /* 10 أعمدة متساوية */
    gap: 4px !important;
    margin-bottom: 4px !important;
    direction: ltr !important; /* قراءة الأرقام من اليسار لليمين */
}
.num-grid-wrapper [data-testid="column"] { width: 100% !important; min-width: 0 !important; padding: 0 !important; }

/* الأزرار الأصلية لتكون دائرية */
.num-grid-wrapper div.stButton > button {
    width: 100% !important;
    aspect-ratio: 1 !important; /* دائرية 100% */
    border-radius: 50% !important;
    padding: 0 !important;
    font-size: clamp(0.6rem, 2.4vw, 0.85rem) !important;
    font-weight: 700 !important;
    border: 1.5px solid #1e1e2e !important;
    background: #13131a !important;
    color: #444 !important;
    box-shadow: none !important;
    transition: 0.15s transform !important;
}
.num-grid-wrapper div.stButton > button:active { transform: scale(0.8) !important; }

/* ألوان التحديد */
.sel-1 div.stButton > button { background: #0066ff !important; border-color: #00d4ff !important; color: #fff !important; box-shadow: 0 0 8px #0066ff88 !important; }
.sel-2 div.stButton > button { background: #00a844 !important; border-color: #00ff88 !important; color: #fff !important; box-shadow: 0 0 8px #00a84488 !important; }
.sel-both div.stButton > button { background: linear-gradient(135deg, #0066ff 50%, #00a844 50%) !important; border-color: #888 !important; color: #fff !important; box-shadow: 0 0 10px #ffffff33 !important; }
.locked div.stButton > button { opacity: 0.25 !important; pointer-events: none !important; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
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

# ── العناوين ──────────────────────────────────────────────────────────────────
st.markdown('<div class="misho-title">ميشو</div><div class="misho-subtitle">لوحة الأرقام</div>', unsafe_allow_html=True)

# ── التابات (بدون رفرش) ───────────────────────────────────────────────────────
st.markdown('<div class="tabs-wrapper">', unsafe_allow_html=True)
t1, t2 = st.columns(2)
with t1:
    st.markdown(f'<div class="tab-btn {"tab-active-1" if tab==1 else ""}">', unsafe_allow_html=True)
    if st.button(f"البطاقة الأولى ({len(c1)})", key="tab1"):
        st.session_state.tab = 1; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
with t2:
    st.markdown(f'<div class="tab-btn {"tab-active-2" if tab==2 else ""}">', unsafe_allow_html=True)
    if st.button(f"البطاقة الثانية ({len(c2)})", key="tab2"):
        st.session_state.tab = 2; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── العداد ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="counter-wrap">
    <span class="counter-label">{'البطاقة الأولى' if tab==1 else 'البطاقة الثانية'}</span>
    <span class="counter-num">{count}<span>/{MAX}</span></span>
    <div class="counter-bar-bg"><div class="counter-bar-fill {'bar-1' if tab==1 else 'bar-2'}" style="width:{int(count/MAX*100) if MAX > 0 else 0}%"></div></div>
</div>
""", unsafe_allow_html=True)

# ── شبكة الأرقام (أزرار أصلية سريعة) ──────────────────────────────────────────
st.markdown('<div class="num-grid-wrapper">', unsafe_allow_html=True)
for r in range(9):
    cols = st.columns(10)
    for c in range(10):
        n = r * 10 + c + 1
        i1, i2 = n in c1, n in c2
        locked = is_full and (n not in sel)
        
        classes = []
        if i1 and i2: classes.append("sel-both")
        elif i1: classes.append("sel-1")
        elif i2: classes.append("sel-2")
        if locked: classes.append("locked")
        cls_str = " ".join(classes)
        
        with cols[c]:
            st.markdown(f'<div class="{cls_str}">', unsafe_allow_html=True)
            if st.button(str(n), key=f"n_{n}"):
                if not locked:
                    if n in sel: sel.discard(n)
                    else: sel.add(n)
                    st.session_state.cards = []; st.session_state.show = False
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── أزرار التحكم ──────────────────────────────────────────────────────────────
st.markdown('<div class="actions-wrapper">', unsafe_allow_html=True)
a1, a2, a3 = st.columns(3)
with a1:
    st.markdown('<div class="action-btn btn-reset">', unsafe_allow_html=True)
    if st.button("🗑 مسح البطاقة", key="btn_clr_tab"):
        if tab == 1: st.session_state.c1 = set()
        else: st.session_state.c2 = set()
        st.session_state.cards = []; st.session_state.show = False; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
with a2:
    st.markdown('<div class="action-btn btn-reset">', unsafe_allow_html=True)
    if st.button("🗑 مسح الكل", key="btn_clr_all"):
        st.session_state.c1 = set(); st.session_state.c2 = set()
        st.session_state.cards = []; st.session_state.show = False; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
with a3:
    st.markdown(f'<div class="action-btn {"btn-gen" if can_gen else "btn-gen-off"}">', unsafe_allow_html=True)
    if st.button("🎯 توليد" if can_gen else "⚠️ أكمل", key="btn_gen"):
        if can_gen:
            shared = sorted(c1 & c2, reverse=True); vessel = sorted(c2 - c1)
            v = len(vessel); nc = v // 5
            if v % 5 >= 4: nc += 1
            if nc == 0: nc = 1
            tot = nc * 5; pool = vessel.copy(); random.shuffle(pool)
            take = pool[:min(tot, len(pool))]
            extra = shared[:tot-len(take)]; all_n = take + extra; random.shuffle(all_n)
            st.session_state.cards = [sorted(all_n[i*5:(i+1)*5]) for i in range(nc)]
            st.session_state.show = True; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── النتائج ───────────────────────────────────────────────────────────────────
if st.session_state.show:
    v_nums, s_nums = sorted(c2 - c1), sorted(c1 & c2)
    s_set = set(s_nums)
    
    st.markdown(f"""
    <div style="background:#13131a;border-radius:14px;padding:12px;margin:10px 0;border:1px solid #1e1e2e;text-align:center;">
        <div style="color:#fff;font-weight:900;margin-bottom:8px;">📊 التحليل</div>
        <div style="display:flex;gap:10px;font-size:0.8rem;color:#888;">
            <div style="flex:1;">الوعاء: <span style="color:#00d4ff;">{len(v_nums)}</span></div>
            <div style="flex:1;">المشترك: <span style="color:#aaa;">{len(s_nums)}</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    for i, card in enumerate(st.session_state.cards):
        nums_divs = "".join(f'<div style="width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.7rem;font-weight:700;{"background:#7b2fff33;color:#d0aaff;border:1px solid #7b2fff" if n in s_set else "background:#111;color:#ccc;border:1px solid #333"}">{n}</div>' for n in card)
        st.markdown(f"""
        <div style="background:#0d0d14;border-radius:12px;padding:12px;margin-bottom:8px;border:1px solid #1e1e2e;">
            <div style="display:flex;justify-content:space-between;margin-bottom:8px;color:#888;font-size:0.75rem;">
                <span>البطاقة {i+1}</span><span>{len(card)} أرقام</span>
            </div>
            <div style="display:flex;flex-wrap:wrap;gap:5px;">{nums_divs}</div>
        </div>
        """, unsafe_allow_html=True)