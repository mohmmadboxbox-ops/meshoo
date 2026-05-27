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

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    height: 100%; width: 100%;
    background: #0a0a0f !important;
    font-family: 'Tajawal', sans-serif;
    overflow-x: hidden;
}

[data-testid="stAppViewContainer"] { padding: 0 !important; }
[data-testid="stMain"] { padding: 0 !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
header, footer { display: none !important; }
#MainMenu { display: none !important; }

.misho-app {
    min-height: 100vh;
    background: #0a0a0f;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 16px 8px 24px;
    direction: rtl;
}

.misho-header { width: 100%; max-width: 520px; text-align: center; margin-bottom: 14px; }
.misho-title {
    font-size: 2rem; font-weight: 900; letter-spacing: 4px;
    background: linear-gradient(135deg, #00d4ff, #7b2fff, #ff6b35);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
}
.misho-subtitle { font-size: 0.78rem; color: #555; letter-spacing: 2px; text-transform: uppercase; }

.tab-bar {
    display: flex; gap: 8px; margin-bottom: 14px;
    background: #13131a; border-radius: 14px; padding: 5px; border: 1px solid #1e1e2e;
    width: 100%; max-width: 520px;
}
.tab-btn {
    flex: 1; padding: 10px 18px; border-radius: 10px; border: none;
    font-family: 'Tajawal', sans-serif; font-size: 0.9rem; font-weight: 700;
    cursor: pointer; color: #555; background: transparent; width: 100%;
}
.tab-btn.active-1 { background: linear-gradient(135deg, #0066ff, #00d4ff); color: #fff; box-shadow: 0 0 18px #0066ff55; }
.tab-btn.active-2 { background: linear-gradient(135deg, #00a844, #00ff88); color: #fff; box-shadow: 0 0 18px #00a84455; }

.counter-wrap {
    width: 100%; max-width: 520px; display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 12px; padding: 10px 16px; background: #13131a; border-radius: 14px; border: 1px solid #1e1e2e;
}
.counter-label { font-size: 0.8rem; color: #666; }
.counter-num { font-size: 1.5rem; font-weight: 900; color: #fff; }
.counter-num span { font-size: 0.9rem; color: #444; }
.counter-bar-bg { flex: 1; margin: 0 12px; height: 6px; background: #1e1e2e; border-radius: 99px; overflow: hidden; }
.counter-bar-fill { height: 100%; border-radius: 99px; }
.bar-1 { background: linear-gradient(90deg, #0066ff, #00d4ff); }
.bar-2 { background: linear-gradient(90deg, #00a844, #00ff88); }

.numbers-grid {
    width: 100%; max-width: 520px; display: grid; grid-template-columns: repeat(10, 1fr);
    gap: 5px; margin-bottom: 14px;
}
.num-circle {
    aspect-ratio: 1; border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-size: clamp(0.55rem, 2.2vw, 0.78rem); font-weight: 700; border: 1.5px solid #1e1e2e;
    background: #13131a; color: #444; transition: 0.2s;
}
.sel-1 { background: #0066ff; border-color: #00d4ff; color: #fff; box-shadow: 0 0 10px #0066ff88; }
.sel-2 { background: #00a844; border-color: #00ff88; color: #fff; box-shadow: 0 0 10px #00a84488; }
.sel-both { border-color: #888; color: #fff; background: linear-gradient(135deg, #0066ff 50%, #00a844 50%); box-shadow: 0 0 12px #ffffff33; }
.locked { opacity: 0.3; pointer-events: none; }

.action-row { width: 100%; max-width: 520px; display: flex; gap: 8px; margin-bottom: 10px; }
.action-btn {
    flex: 1; padding: 12px 8px; border-radius: 12px; border: none;
    font-family: 'Tajawal', sans-serif; font-size: 0.85rem; font-weight: 700; color: #fff; width: 100%;
}
.btn-reset { background: #1e1e2e; color: #888; border: 1px solid #2a2a3e; }
.btn-filter { background: linear-gradient(135deg, #7b2fff, #ff6b35); box-shadow: 0 0 16px #7b2fff55; }
.btn-disabled { opacity: 0.4; pointer-events: none; background: #1e1e2e; color: #666; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "c1" not in st.session_state: st.session_state.c1 = set()
if "c2" not in st.session_state: st.session_state.c2 = set()
if "tab" not in st.session_state: st.session_state.tab = 1
if "cards" not in st.session_state: st.session_state.cards = []
if "show" not in st.session_state: st.session_state.show = False

MAX = 50

# ── URL PARAMETERS HANDLING (NO BUGS) ─────────────────────────────────────────
params = st.query_params
if "toggle" in params:
    try:
        n = int(params["toggle"])
        s = st.session_state.c1 if st.session_state.tab == 1 else st.session_state.c2
        if n in s: s.discard(n)
        elif len(s) < MAX: s.add(n)
        st.session_state.cards = []
        st.session_state.show = False
    except: pass
    st.query_params.clear()

if "tab" in params:
    st.session_state.tab = int(params["tab"])
    st.query_params.clear()

if "action" in params:
    act = params["action"]
    if act == "reset":
        if st.session_state.tab == 1: st.session_state.c1 = set()
        else: st.session_state.c2 = set()
    elif act == "reset_all":
        st.session_state.c1 = set()
        st.session_state.c2 = set()
    elif act == "gen":
        # Generate Logic
        c1, c2 = st.session_state.c1, st.session_state.c2
        shared = sorted(c1 & c2, reverse=True)
        vessel = sorted(c2 - c1)
        v = len(vessel)
        nc = v // 5
        if v % 5 >= 4: nc += 1
        if nc == 0: nc = 1
        total = nc * 5
        pool = vessel.copy(); random.shuffle(pool)
        take = pool[:min(total, len(pool))]
        extra = shared[:total-len(take)]
        all_n = take + extra; random.shuffle(all_n)
        st.session_state.cards = [sorted(all_n[i*5:(i+1)*5]) for i in range(nc)]
        st.session_state.show = True
    
    if act in ["reset", "reset_all"]:
        st.session_state.cards = []
        st.session_state.show = False
        
    st.query_params.clear()

# ── RENDER VARIABLES ──────────────────────────────────────────────────────────
c1, c2 = st.session_state.c1, st.session_state.c2
tab = st.session_state.tab
sel = c1 if tab == 1 else c2
count = len(sel)
is_full = count >= MAX
can_gen = len(c1) == MAX and len(c2) == MAX

# ── HTML BUILDER ──────────────────────────────────────────────────────────────
grid_html = '<div class="numbers-grid">'
for n in range(1, 91):
    i1, i2 = n in c1, n in c2
    cls = "sel-both" if (i1 and i2) else "sel-1" if i1 else "sel-2" if i2 else ""
    locked = is_full and (n not in sel)
    lock_cls = " locked" if locked else ""
    
    if locked:
        grid_html += f'<div class="num-circle {cls}{lock_cls}">{n}</div>'
    else:
        grid_html += f'<a href="?toggle={n}" style="text-decoration:none;"><div class="num-circle {cls}{lock_cls}">{n}</div></a>'
grid_html += '</div>'

tabs_html = f"""
<div class="tab-bar">
    <a href="?tab=1" style="text-decoration:none;flex:1"><button class="tab-btn {'active-1' if tab==1 else ''}">البطاقة الأولى ({len(c1)})</button></a>
    <a href="?tab=2" style="text-decoration:none;flex:1"><button class="tab-btn {'active-2' if tab==2 else ''}">البطاقة الثانية ({len(c2)})</button></a>
</div>
"""

counter_html = f"""
<div class="counter-wrap">
    <span class="counter-label">{'البطاقة الأولى' if tab==1 else 'البطاقة الثانية'}</span>
    <span class="counter-num">{count}<span>/{MAX}</span></span>
    <div class="counter-bar-bg"><div class="counter-bar-fill {'bar-1' if tab==1 else 'bar-2'}" style="width:{int(count/MAX*100)}%"></div></div>
</div>
"""

actions_html = f"""
<div class="action-row">
    <a href="?action=reset" style="text-decoration:none;flex:1"><button class="action-btn btn-reset">🗑 مسح</button></a>
    <a href="?action=reset_all" style="text-decoration:none;flex:1"><button class="action-btn btn-reset">🗑 مسح الكل</button></a>
    <a href="?action=gen" style="text-decoration:none;flex:1; pointer-events:{'auto' if can_gen else 'none'}">
        <button class="action-btn {'btn-filter' if can_gen else 'btn-disabled'}">{'🎯 توليد' if can_gen else '⚠️ أكمل'}</button>
    </a>
</div>
"""

results_html = ""
if st.session_state.show:
    v_nums = sorted(c2 - c1)
    s_nums = sorted(c1 & c2)
    s_set = set(s_nums)
    
    # Simple summary results
    results_html += f"""
    <div style="width:100%;max-width:520px;background:#13131a;border-radius:14px;padding:12px;margin-top:10px;border:1px solid #1e1e2e;">
        <div style="color:#fff;font-weight:900;text-align:center;margin-bottom:8px;">📊 التحليل</div>
        <div style="display:flex;gap:10px;font-size:0.8rem;color:#888;">
            <div style="flex:1;">الوعاء: <span style="color:#00d4ff;">{len(v_nums)}</span></div>
            <div style="flex:1;">المشترك: <span style="color:#aaa;">{len(s_nums)}</span></div>
        </div>
    </div>
    """
    
    # Generated Cards
    for i, card in enumerate(st.session_state.cards):
        nums_divs = "".join(f'<div style="width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.7rem;font-weight:700;{"background:#7b2fff33;color:#d0aaff;border:1px solid #7b2fff" if n in s_set else "background:#111;color:#ccc;border:1px solid #333"}">{n}</div>' for n in card)
        results_html += f"""
        <div style="width:100%;max-width:520px;background:#0d0d14;border-radius:12px;padding:12px;margin-top:8px;border:1px solid #1e1e2e;">
            <div style="display:flex;justify-content:space-between;margin-bottom:8px;color:#888;font-size:0.75rem;">
                <span>البطاقة {i+1}</span><span>{len(card)} أرقام</span>
            </div>
            <div style="display:flex;flex-wrap:wrap;gap:5px;">{nums_divs}</div>
        </div>
        """

st.markdown(f"""
<div class="misho-app">
    <div class="misho-header">
        <div class="misho-title">ميشو</div>
        <div class="misho-subtitle">لوحة الأرقام</div>
    </div>
    {tabs_html}
    {counter_html}
    {grid_html}
    {actions_html}
    {results_html}
</div>
""", unsafe_allow_html=True)