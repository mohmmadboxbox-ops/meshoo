import streamlit as st
import random

st.set_page_config(
    page_title="ميشو",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #0a0a0f !important;
    font-family: 'Tajawal', sans-serif !important;
}
.block-container {
    padding: 10px 6px 40px !important;
    max-width: 480px !important;
    margin: auto !important;
}
header, footer, #MainMenu { display: none !important; }
[data-testid="stVerticalBlock"] { gap: 2px !important; }

/* ── كل الأزرار الافتراضية ── */
div.stButton > button {
    font-family: 'Tajawal', sans-serif !important;
    font-weight: 700 !important;
    transition: all 0.15s !important;
    outline: none !important;
}

/* ── أزرار الأرقام ── */
.numgrid [data-testid="stHorizontalBlock"] {
    gap: 3px !important;
}
.numgrid div.stButton > button {
    width: 100% !important;
    aspect-ratio: 1 !important;
    border-radius: 50% !important;
    padding: 0 !important;
    font-size: clamp(0.48rem, 1.9vw, 0.72rem) !important;
    border: 1.5px solid #1e1e2e !important;
    background: #13131a !important;
    color: #444 !important;
    min-height: unset !important;
    line-height: 1 !important;
}
.numgrid div.stButton > button:hover {
    border-color: #555 !important;
    color: #bbb !important;
}

/* ── ألوان الاختيار ── */
.s1 div.stButton > button {
    background: #0066ff !important;
    border-color: #00d4ff !important;
    color: #fff !important;
    box-shadow: 0 0 7px #0066ff88 !important;
}
.s2 div.stButton > button {
    background: #00a844 !important;
    border-color: #00ff88 !important;
    color: #fff !important;
    box-shadow: 0 0 7px #00a84488 !important;
}
.sb div.stButton > button {
    background: linear-gradient(135deg, #0066ff 50%, #00a844 50%) !important;
    border-color: #aaa !important;
    color: #fff !important;
    box-shadow: 0 0 8px #ffffff22 !important;
}
.lk div.stButton > button {
    opacity: 0.25 !important;
    pointer-events: none !important;
    cursor: not-allowed !important;
}

/* ── أزرار التابات ── */
.tabrow div.stButton > button {
    width: 100% !important;
    aspect-ratio: unset !important;
    border-radius: 10px !important;
    padding: 9px 4px !important;
    font-size: 0.82rem !important;
    border: 1px solid #1e1e2e !important;
    background: #13131a !important;
    color: #555 !important;
}
.tab-active-1 div.stButton > button {
    background: linear-gradient(135deg,#0066ff,#00d4ff) !important;
    color: #fff !important;
    border: none !important;
    box-shadow: 0 0 14px #0066ff44 !important;
}
.tab-active-2 div.stButton > button {
    background: linear-gradient(135deg,#00a844,#00ff88) !important;
    color: #fff !important;
    border: none !important;
    box-shadow: 0 0 14px #00a84444 !important;
}

/* ── أزرار الإجراءات ── */
.actrow div.stButton > button {
    width: 100% !important;
    aspect-ratio: unset !important;
    border-radius: 10px !important;
    padding: 10px 4px !important;
    font-size: 0.8rem !important;
    background: #1e1e2e !important;
    color: #888 !important;
    border: 1px solid #2a2a3e !important;
}
.genbtn div.stButton > button {
    background: linear-gradient(135deg,#7b2fff,#ff6b35) !important;
    color: #fff !important;
    border: none !important;
    box-shadow: 0 0 14px #7b2fff44 !important;
}
.genbtn-off div.stButton > button {
    background: #1e1e2e !important;
    color: #333 !important;
    border: 1px solid #1e1e2e !important;
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──────────────────────────────────────────────────────────────
for k, v in [("c1", set()), ("c2", set()), ("tab", 1), ("cards", []), ("show", False)]:
    if k not in st.session_state:
        st.session_state[k] = v

MAX = 50

def toggle(n):
    s = st.session_state.c1 if st.session_state.tab == 1 else st.session_state.c2
    if n in s:
        s.discard(n)
    else:
        if len(s) < MAX:
            s.add(n)
    st.session_state.cards = []
    st.session_state.show = False

def do_generate():
    c1 = st.session_state.c1
    c2 = st.session_state.c2
    shared = sorted(c1 & c2, reverse=True)
    vessel = sorted(c2 - c1)
    v = len(vessel)
    n_cards = v // 5
    rem = v % 5
    if rem >= 4:
        n_cards += 1
    if n_cards == 0:
        n_cards = 1
    total = n_cards * 5
    pool = vessel.copy()
    random.shuffle(pool)
    take = pool[:min(total, len(pool))]
    shortage = total - len(take)
    extra = shared[:shortage]
    all_n = take + extra
    random.shuffle(all_n)
    result = [sorted(all_n[i*5:(i+1)*5]) for i in range(n_cards)]
    st.session_state.cards = result
    st.session_state.show = True

# ── STATE ──────────────────────────────────────────────────────────────────────
c1 = st.session_state.c1
c2 = st.session_state.c2
tab = st.session_state.tab
sel = c1 if tab == 1 else c2
count = len(sel)
full = count >= MAX
can_gen = len(c1) == MAX and len(c2) == MAX

# ── TITLE ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:6px 0 4px;direction:rtl">
  <div style="font-size:2rem;font-weight:900;letter-spacing:4px;
    background:linear-gradient(135deg,#00d4ff,#7b2fff,#ff6b35);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">ميشو</div>
  <div style="font-size:0.7rem;color:#444;letter-spacing:2px">لوحة الأرقام</div>
</div>
""", unsafe_allow_html=True)

# ── TABS ───────────────────────────────────────────────────────────────────────
st.markdown('<div class="tabrow">', unsafe_allow_html=True)
tc1, tc2 = st.columns(2)
with tc1:
    cls = "tab-active-1" if tab == 1 else ""
    st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
    if st.button(f"البطاقة الأولى ({len(c1)})", key="tab1"):
        st.session_state.tab = 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
with tc2:
    cls = "tab-active-2" if tab == 2 else ""
    st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
    if st.button(f"البطاقة الثانية ({len(c2)})", key="tab2"):
        st.session_state.tab = 2
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── COUNTER ────────────────────────────────────────────────────────────────────
pct = int(count / MAX * 100)
bar_col  = "#0066ff" if tab == 1 else "#00a844"
bar_col2 = "#00d4ff" if tab == 1 else "#00ff88"
num_col  = "#ff4444" if full else "#ffffff"
st.markdown(f"""
<div style="background:#13131a;border:1px solid #1e1e2e;border-radius:12px;
  padding:10px 14px;display:flex;align-items:center;gap:10px;direction:rtl;margin:4px 0">
  <span style="font-size:0.78rem;color:#555;white-space:nowrap">
    {'البطاقة الأولى' if tab==1 else 'البطاقة الثانية'}
  </span>
  <span style="font-size:1.4rem;font-weight:900;color:{num_col};white-space:nowrap">
    {count}<span style="font-size:0.8rem;color:#333">/{MAX}</span>
  </span>
  <div style="flex:1;height:6px;background:#1e1e2e;border-radius:99px;overflow:hidden">
    <div style="width:{pct}%;height:100%;border-radius:99px;
      background:linear-gradient(90deg,{bar_col},{bar_col2})"></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── NUMBER GRID ────────────────────────────────────────────────────────────────
st.markdown('<div class="numgrid">', unsafe_allow_html=True)
for row in range(9):
    cols = st.columns(10)
    for ci, col in enumerate(cols):
        n = row * 10 + ci + 1
        in1 = n in c1
        in2 = n in c2
        is_locked = full and n not in sel

        if in1 and in2:   css = "sb"
        elif in1:          css = "s1"
        elif in2:          css = "s2"
        else:              css = ""
        if is_locked:      css += " lk"

        with col:
            st.markdown(f'<div class="{css}">', unsafe_allow_html=True)
            if st.button(str(n), key=f"n{n}"):
                if not is_locked:
                    toggle(n)
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── ACTION BUTTONS ─────────────────────────────────────────────────────────────
st.markdown('<div class="actrow">', unsafe_allow_html=True)
a1, a2, a3 = st.columns(3)
with a1:
    if st.button("🗑 مسح البطاقة", key="reset"):
        if tab == 1: st.session_state.c1 = set()
        else:        st.session_state.c2 = set()
        st.session_state.cards = []
        st.session_state.show = False
        st.rerun()
with a2:
    if st.button("🗑 مسح الكل", key="reset_all"):
        st.session_state.c1 = set()
        st.session_state.c2 = set()
        st.session_state.cards = []
        st.session_state.show = False
        st.rerun()
with a3:
    gen_cls = "genbtn" if can_gen else "genbtn-off"
    st.markdown(f'<div class="{gen_cls}">', unsafe_allow_html=True)
    if st.button("🎯 توليد" if can_gen else "⚠️ أكمل", key="gen"):
        if can_gen:
            do_generate()
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── RESULTS ────────────────────────────────────────────────────────────────────
if st.session_state.show:
    vessel = sorted(c2 - c1)
    shared = sorted(c1 & c2)
    shared_set = set(shared)

    def circle(n, style):
        return (f'<div style="width:26px;height:26px;border-radius:50%;display:flex;'
                f'align-items:center;justify-content:center;font-size:0.62rem;font-weight:700;{style}">{n}</div>')

    vessel_html = "".join(circle(n,"background:#0066ff22;color:#00d4ff;border:1px solid #0066ff44") for n in vessel)
    shared_html = "".join(circle(n,"background:#ffffff0a;color:#666;border:1px solid #2a2a3e") for n in shared)

    st.markdown(f"""
    <div style="background:#13131a;border:1px solid #1e1e2e;border-radius:14px;
      padding:14px;direction:rtl;margin-top:8px">
      <div style="text-align:center;font-size:0.9rem;font-weight:900;margin-bottom:10px">📊 التحليل</div>
      <div style="display:flex;gap:10px">
        <div style="flex:1">
          <div style="font-size:0.68rem;font-weight:700;color:#00d4ff;margin-bottom:6px">الوعاء ({len(vessel)})</div>
          <div style="display:flex;flex-wrap:wrap;gap:3px">{vessel_html}</div>
        </div>
        <div style="flex:1">
          <div style="font-size:0.68rem;font-weight:700;color:#888;margin-bottom:6px">المشترك ({len(shared)})</div>
          <div style="display:flex;flex-wrap:wrap;gap:3px">{shared_html}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    for i, card in enumerate(st.session_state.cards):
        nums_html = "".join(
            f'<div style="width:32px;height:32px;border-radius:50%;display:flex;align-items:center;'
            f'justify-content:center;font-size:0.68rem;font-weight:700;'
            f'{"background:#7b2fff22;color:#bf88ff;border:1px solid #7b2fff55" if n in shared_set else "background:#13131a;color:#bbb;border:1px solid #2a2a3e"}">{n}</div>'
            for n in card
        )
        st.markdown(f"""
        <div style="background:#0d0d14;border:1px solid #1e1e2e;border-radius:12px;
          padding:12px;margin-top:8px;direction:rtl">
          <div style="display:flex;justify-content:space-between;margin-bottom:8px">
            <span style="font-size:0.75rem;font-weight:700;color:#555">البطاقة {i+1}</span>
            <span style="font-size:0.68rem;color:#333">{len(card)} أرقام</span>
          </div>
          <div style="display:flex;flex-wrap:wrap;gap:4px">{nums_html}</div>
        </div>
        """, unsafe_allow_html=True)