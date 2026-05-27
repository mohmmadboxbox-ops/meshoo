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
[data-testid="stVerticalBlock"] { gap: 0 !important; }
header, footer { display: none !important; }
#MainMenu { display: none !important; }

/* ── APP SHELL ── */
.misho-app {
    min-height: 100vh;
    background: #0a0a0f;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 16px 8px 24px;
    direction: rtl;
}

/* ── HEADER ── */
.misho-header {
    width: 100%;
    max-width: 520px;
    text-align: center;
    margin-bottom: 14px;
}
.misho-title {
    font-size: 2rem;
    font-weight: 900;
    letter-spacing: 4px;
    background: linear-gradient(135deg, #00d4ff, #7b2fff, #ff6b35);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 4px;
}
.misho-subtitle {
    font-size: 0.78rem;
    color: #555;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* ── TAB BAR ── */
.tab-bar {
    display: flex;
    gap: 8px;
    margin-bottom: 14px;
    background: #13131a;
    border-radius: 14px;
    padding: 5px;
    border: 1px solid #1e1e2e;
}
.tab-btn {
    flex: 1;
    padding: 10px 18px;
    border-radius: 10px;
    border: none;
    font-family: 'Tajawal', sans-serif;
    font-size: 0.9rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.25s;
    color: #555;
    background: transparent;
}
.tab-btn.active-1 {
    background: linear-gradient(135deg, #0066ff, #00d4ff);
    color: #fff;
    box-shadow: 0 0 18px #0066ff55;
}
.tab-btn.active-2 {
    background: linear-gradient(135deg, #00a844, #00ff88);
    color: #fff;
    box-shadow: 0 0 18px #00a84455;
}

/* ── COUNTER ── */
.counter-wrap {
    width: 100%;
    max-width: 520px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
    padding: 10px 16px;
    background: #13131a;
    border-radius: 14px;
    border: 1px solid #1e1e2e;
}
.counter-label { font-size: 0.8rem; color: #666; }
.counter-num {
    font-size: 1.5rem;
    font-weight: 900;
    color: #fff;
}
.counter-num span { font-size: 0.9rem; color: #444; }
.counter-bar-bg {
    flex: 1;
    margin: 0 12px;
    height: 6px;
    background: #1e1e2e;
    border-radius: 99px;
    overflow: hidden;
}
.counter-bar-fill {
    height: 100%;
    border-radius: 99px;
    transition: width 0.3s ease;
}
.bar-1 { background: linear-gradient(90deg, #0066ff, #00d4ff); }
.bar-2 { background: linear-gradient(90deg, #00a844, #00ff88); }
.counter-full { color: #ff4444 !important; }

/* ── GRID ── */
.numbers-grid {
    width: 100%;
    max-width: 520px;
    display: grid;
    grid-template-columns: repeat(10, 1fr);
    gap: 5px;
    margin-bottom: 14px;
}

/* ── CIRCLE ── */
.num-circle {
    aspect-ratio: 1;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: clamp(0.55rem, 2.2vw, 0.78rem);
    font-weight: 700;
    cursor: pointer;
    transition: transform 0.15s, box-shadow 0.15s;
    position: relative;
    overflow: hidden;
    user-select: none;
    -webkit-tap-highlight-color: transparent;
    border: 1.5px solid #1e1e2e;
    background: #13131a;
    color: #444;
}
.num-circle:active { transform: scale(0.88); }
.num-circle.locked { cursor: not-allowed; opacity: 0.5; }

/* card 1 only → blue */
.num-circle.sel-1 {
    background: #0066ff;
    border-color: #00d4ff;
    color: #fff;
    box-shadow: 0 0 10px #0066ff88;
}
/* card 2 only → green */
.num-circle.sel-2 {
    background: #00a844;
    border-color: #00ff88;
    color: #fff;
    box-shadow: 0 0 10px #00a84488;
}
/* both → half-half */
.num-circle.sel-both {
    border-color: #888;
    color: #fff;
    background: linear-gradient(135deg, #0066ff 50%, #00a844 50%);
    box-shadow: 0 0 12px #ffffff33;
}

/* ── ACTION BUTTONS ── */
.action-row {
    width: 100%;
    max-width: 520px;
    display: flex;
    gap: 8px;
    margin-bottom: 10px;
}
.action-btn {
    flex: 1;
    padding: 12px 8px;
    border-radius: 12px;
    border: none;
    font-family: 'Tajawal', sans-serif;
    font-size: 0.85rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s;
    letter-spacing: 0.5px;
}
.btn-reset {
    background: #1e1e2e;
    color: #888;
    border: 1px solid #2a2a3e;
}
.btn-reset:hover { background: #2a2a3e; color: #aaa; }
.btn-filter {
    background: linear-gradient(135deg, #7b2fff, #ff6b35);
    color: #fff;
    box-shadow: 0 0 16px #7b2fff55;
}
.btn-filter:hover { opacity: 0.88; }
.btn-filter:disabled { opacity: 0.35; cursor: not-allowed; }

/* ── RESULTS PANEL ── */
.results-panel {
    width: 100%;
    max-width: 520px;
    background: #13131a;
    border-radius: 16px;
    border: 1px solid #1e1e2e;
    padding: 16px;
    margin-top: 4px;
}
.results-title {
    font-size: 1rem;
    font-weight: 900;
    color: #fff;
    margin-bottom: 12px;
    text-align: center;
    letter-spacing: 1px;
}
.results-row {
    display: flex;
    gap: 8px;
    margin-bottom: 10px;
    flex-wrap: wrap;
    align-items: flex-start;
}
.results-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 6px;
    text-transform: uppercase;
}
.label-vessel { color: #00d4ff; }
.label-shared { color: #888; }
.label-card { color: #fff; }

.results-section { flex: 1; min-width: 120px; }
.results-nums {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
}
.r-num {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.65rem;
    font-weight: 700;
}
.r-num-vessel { background: #0066ff22; color: #00d4ff; border: 1px solid #0066ff44; }
.r-num-shared { background: #ffffff11; color: #888; border: 1px solid #333; }

/* ── GENERATED CARDS ── */
.cards-grid {
    width: 100%;
    max-width: 520px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 10px;
}
.gen-card {
    background: #0d0d14;
    border-radius: 14px;
    border: 1px solid #1e1e2e;
    padding: 12px 14px;
    position: relative;
}
.gen-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}
.gen-card-title {
    font-size: 0.78rem;
    font-weight: 700;
    color: #666;
    letter-spacing: 1px;
}
.gen-card-count {
    font-size: 0.7rem;
    color: #444;
}
.gen-card-nums {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
}
.g-num {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.68rem;
    font-weight: 700;
    border: 1px solid #2a2a3e;
    color: #ccc;
    background: #13131a;
}
.g-num-from-shared {
    background: #7b2fff22;
    color: #bf88ff;
    border-color: #7b2fff55;
}

.divider {
    width: 100%;
    max-width: 520px;
    height: 1px;
    background: #1e1e2e;
    margin: 10px 0;
}

/* scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #2a2a3e; border-radius: 99px; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "card1" not in st.session_state:
    st.session_state.card1 = set()
if "card2" not in st.session_state:
    st.session_state.card2 = set()
if "active_tab" not in st.session_state:
    st.session_state.active_tab = 1
if "generated_cards" not in st.session_state:
    st.session_state.generated_cards = []
if "show_results" not in st.session_state:
    st.session_state.show_results = False

MAX_SELECT = 50

# ── HELPERS ───────────────────────────────────────────────────────────────────
def toggle_number(n):
    tab = st.session_state.active_tab
    s = st.session_state.card1 if tab == 1 else st.session_state.card2
    if n in s:
        s.discard(n)
    else:
        if len(s) < MAX_SELECT:
            s.add(n)
    st.session_state.generated_cards = []
    st.session_state.show_results = False

def reset_current():
    if st.session_state.active_tab == 1:
        st.session_state.card1 = set()
    else:
        st.session_state.card2 = set()
    st.session_state.generated_cards = []
    st.session_state.show_results = False

def reset_all():
    st.session_state.card1 = set()
    st.session_state.card2 = set()
    st.session_state.generated_cards = []
    st.session_state.show_results = False

def generate_cards():
    c1 = st.session_state.card1
    c2 = st.session_state.card2
    shared = sorted(c1 & c2, reverse=True)
    vessel = sorted(c2 - c1)

    if not vessel and not shared:
        return

    # how many cards
    v_count = len(vessel)
    num_cards = v_count // 5
    remainder = v_count % 5

    if remainder >= 4:
        num_cards += 1

    if num_cards == 0:
        num_cards = 1

    total_needed = num_cards * 5
    from_vessel = vessel.copy()
    random.shuffle(from_vessel)

    # take only what we need from vessel
    take_from_vessel = from_vessel[:min(total_needed, len(from_vessel))]
    shortage = total_needed - len(take_from_vessel)

    # fill shortage from shared (descending)
    from_shared_pool = shared[:shortage]
    all_numbers = take_from_vessel + from_shared_pool

    random.shuffle(all_numbers)

    cards = []
    shared_set = set(shared)
    for i in range(num_cards):
        chunk = sorted(all_numbers[i*5:(i+1)*5])
        cards.append(chunk)

    st.session_state.generated_cards = cards
    st.session_state.show_results = True

# ── HANDLE URL PARAMS FOR TOGGLE ─────────────────────────────────────────────
params = st.query_params
if "toggle" in params:
    try:
        n = int(params["toggle"])
        toggle_number(n)
    except:
        pass
    st.query_params.clear()

if "tab" in params:
    try:
        t = int(params["tab"])
        if t in [1, 2]:
            st.session_state.active_tab = t
    except:
        pass
    st.query_params.clear()

if "action" in params:
    a = params["action"]
    if a == "reset":
        reset_current()
    elif a == "reset_all":
        reset_all()
    elif a == "generate":
        generate_cards()
    st.query_params.clear()

# ── BUILD HTML ────────────────────────────────────────────────────────────────
c1 = st.session_state.card1
c2 = st.session_state.card2
tab = st.session_state.active_tab
count = len(c1) if tab == 1 else len(c2)
pct = int(count / MAX_SELECT * 100)
bar_class = "bar-1" if tab == 1 else "bar-2"
is_full = count >= MAX_SELECT

shared = c1 & c2
vessel = c2 - c1
can_generate = len(c1) == MAX_SELECT and len(c2) == MAX_SELECT

# grid html
grid_html = '<div class="numbers-grid">'
for n in range(1, 91):
    in1 = n in c1
    in2 = n in c2
    if in1 and in2:
        cls = "sel-both"
    elif in1:
        cls = "sel-1"
    elif in2:
        cls = "sel-2"
    else:
        cls = ""

    locked = is_full and (n not in (c1 if tab == 1 else c2))
    lock_cls = " locked" if locked else ""

    if locked:
        grid_html += f'<div class="num-circle {cls}{lock_cls}">{n}</div>'
    else:
        grid_html += f'<a href="?toggle={n}" style="text-decoration:none;"><div class="num-circle {cls}{lock_cls}">{n}</div></a>'

grid_html += '</div>'

# counter
counter_color = ' counter-full' if is_full else ''
counter_html = f"""
<div class="counter-wrap">
    <span class="counter-label">{'البطاقة الأولى' if tab==1 else 'البطاقة الثانية'}</span>
    <span class="counter-num{counter_color}">{count}<span>/{MAX_SELECT}</span></span>
    <div class="counter-bar-bg">
        <div class="counter-bar-fill {bar_class}" style="width:{pct}%"></div>
    </div>
</div>
"""

# tabs
t1_cls = "tab-btn active-1" if tab == 1 else "tab-btn"
t2_cls = "tab-btn active-2" if tab == 2 else "tab-btn"
tabs_html = f"""
<div class="tab-bar">
    <a href="?tab=1" style="text-decoration:none;flex:1"><button class="{t1_cls}">البطاقة الأولى ({len(c1)})</button></a>
    <a href="?tab=2" style="text-decoration:none;flex:1"><button class="{t2_cls}">البطاقة الثانية ({len(c2)})</button></a>
</div>
"""

# action buttons
filter_disabled = "" if can_generate else "disabled"
actions_html = f"""
<div class="action-row">
    <a href="?action=reset" style="text-decoration:none;flex:1"><button class="action-btn btn-reset">مسح البطاقة</button></a>
    <a href="?action=reset_all" style="text-decoration:none;flex:1"><button class="action-btn btn-reset">مسح الكل</button></a>
    <a href="?action=generate" style="text-decoration:none;flex:1"><button class="action-btn btn-filter" {'disabled' if not can_generate else ''}>{'🎯 توليد' if can_generate else '⚠️ أكمل الاختيار'}</button></a>
</div>
"""

# results
results_html = ""
if st.session_state.show_results:
    vessel_nums = sorted(c2 - c1)
    shared_nums = sorted(c1 & c2)

    vessel_circles = "".join(f'<div class="r-num r-num-vessel">{n}</div>' for n in vessel_nums)
    shared_circles = "".join(f'<div class="r-num r-num-shared">{n}</div>' for n in shared_nums)

    results_html += f"""
    <div class="results-panel">
        <div class="results-title">📊 التحليل</div>
        <div class="results-row">
            <div class="results-section">
                <div class="results-label label-vessel">الوعاء ({len(vessel_nums)})</div>
                <div class="results-nums">{vessel_circles}</div>
            </div>
            <div class="results-section">
                <div class="results-label label-shared">المشترك ({len(shared_nums)})</div>
                <div class="results-nums">{shared_circles}</div>
            </div>
        </div>
    </div>
    <div class="divider"></div>
    """

    # generated cards
    if st.session_state.generated_cards:
        shared_set = set(shared_nums)
        vessel_set = set(vessel_nums)
        cards_html = '<div class="cards-grid">'
        for i, card in enumerate(st.session_state.generated_cards):
            nums_html = ""
            for num in card:
                extra = " g-num-from-shared" if num in shared_set else ""
                nums_html += f'<div class="g-num{extra}">{num}</div>'
            cards_html += f"""
            <div class="gen-card">
                <div class="gen-card-header">
                    <span class="gen-card-title">البطاقة {i+1}</span>
                    <span class="gen-card-count">{len(card)} أرقام</span>
                </div>
                <div class="gen-card-nums">{nums_html}</div>
            </div>
            """
        cards_html += '</div>'
        results_html += cards_html

# ── RENDER ────────────────────────────────────────────────────────────────────
html = f"""
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
"""

st.markdown(html, unsafe_allow_html=True)