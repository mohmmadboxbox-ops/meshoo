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
    padding: 6px 4px 40px !important;
    max-width: 100% !important;
}
header, footer, #MainMenu { display: none !important; }

/* إزالة كل المسافات الزيادة بين العناصر */
[data-testid="stVerticalBlock"] { gap: 0 !important; }
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] { padding: 0 !important; }
.element-container { margin: 0 !important; padding: 0 !important; min-height: 0 !important; }
[data-testid="stMarkdownContainer"] { margin: 0 !important; padding: 0 !important; }

/* الأعمدة */
[data-testid="stHorizontalBlock"] {
    gap: 3px !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
}
[data-testid="stHorizontalBlock"] > div {
    flex: 1 !important;
    min-width: 0 !important;
    padding: 0 !important;
    flex-shrink: 1 !important;
}

/* جميع الأزرار - بيس */
div.stButton { margin: 0 !important; padding: 0 !important; }
div.stButton > button {
    width: 100% !important;
    font-family: 'Tajawal', sans-serif !important;
    font-weight: 700 !important;
    padding: 0 !important;
    min-height: unset !important;
    line-height: 1 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.12s !important;
    -webkit-tap-highlight-color: transparent !important;
}

/* ── أزرار الأرقام ── */
.numrow div.stButton > button {
    aspect-ratio: 1 !important;
    border-radius: 50% !important;
    font-size: clamp(0.44rem, 2.6vw, 0.7rem) !important;
    border: 1.5px solid #1e1e2a !important;
    background: #111118 !important;
    color: #4a4a5a !important;
    box-shadow: none !important;
}
.numrow div.stButton > button:hover {
    border-color: #444 !important; color: #aaa !important;
}
.n-s1 div.stButton > button {
    background: #0055cc !important; border-color: #0099ff !important; color: #fff !important;
    box-shadow: 0 0 6px #0055cc88 !important;
}
.n-s2 div.stButton > button {
    background: #008833 !important; border-color: #00cc55 !important; color: #fff !important;
    box-shadow: 0 0 6px #00883388 !important;
}
.n-sb div.stButton > button {
    background: linear-gradient(135deg,#0055cc 50%,#008833 50%) !important;
    border-color: #888 !important; color: #fff !important;
    box-shadow: 0 0 6px #ffffff22 !important;
}
.n-lk div.stButton > button {
    opacity: 0.18 !important; pointer-events: none !important;
}

/* ── أزرار التابات ── */
.tabrow div.stButton > button {
    aspect-ratio: unset !important;
    border-radius: 9px !important;
    padding: 8px 4px !important;
    font-size: 0.78rem !important;
    border: 1px solid #1e1e2a !important;
    background: #111118 !important;
    color: #555 !important;
    box-shadow: none !important;
}
.tab1on div.stButton > button {
    background: linear-gradient(135deg,#0055cc,#0099ff) !important;
    color: #fff !important; border: none !important;
    box-shadow: 0 0 12px #0055cc55 !important;
}
.tab2on div.stButton > button {
    background: linear-gradient(135deg,#008833,#00cc55) !important;
    color: #fff !important; border: none !important;
    box-shadow: 0 0 12px #00883355 !important;
}

/* ── أزرار الإجراءات ── */
.actrow div.stButton > button {
    aspect-ratio: unset !important;
    border-radius: 9px !important;
    padding: 9px 4px !important;
    font-size: 0.75rem !important;
    background: #111118 !important;
    color: #666 !important;
    border: 1px solid #1e1e2a !important;
    box-shadow: none !important;
}
.genbtn div.stButton > button {
    background: linear-gradient(135deg,#6600ff,#ff4400) !important;
    color: #fff !important; border: none !important;
    box-shadow: 0 0 14px #6600ff55 !important;
}
.genbtn-off div.stButton > button {
    background: #0d0d14 !important; color: #2a2a3a !important;
    border: 1px solid #111118 !important;
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──────────────────────────────────────────────────────────────
for k, v in [("c1",set()), ("c2",set()), ("tab",1), ("cards",[]), ("show",False)]:
    if k not in st.session_state:
        st.session_state[k] = v

MAX = 50

def toggle(n):
    s = st.session_state.c1 if st.session_state.tab==1 else st.session_state.c2
    if n in s: s.discard(n)
    elif len(s) < MAX: s.add(n)
    st.session_state.cards = []
    st.session_state.show = False

def do_generate():
    c1,c2 = st.session_state.c1, st.session_state.c2
    shared = sorted(c1 & c2, reverse=True)
    vessel = sorted(c2 - c1)
    v = len(vessel)
    nc = v // 5
    if v % 5 >= 4: nc += 1
    if nc == 0: nc = 1
    total = nc * 5
    pool = vessel.copy(); random.shuffle(pool)
    take = pool[:min(total,len(pool))]
    extra = shared[:total-len(take)]
    all_n = take + extra; random.shuffle(all_n)
    st.session_state.cards = [sorted(all_n[i*5:(i+1)*5]) for i in range(nc)]
    st.session_state.show = True

c1,c2 = st.session_state.c1, st.session_state.c2
tab = st.session_state.tab
sel = c1 if tab==1 else c2
full = len(sel) >= MAX
can_gen = len(c1)==MAX and len(c2)==MAX

# ── TITLE ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:4px 0;direction:rtl">
  <span style="font-size:1.8rem;font-weight:900;letter-spacing:3px;
    background:linear-gradient(135deg,#00ccff,#8833ff,#ff5522);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent">ميشو</span>
  <div style="font-size:0.6rem;color:#2a2a3a;letter-spacing:2px;margin-top:1px">لوحة الأرقام</div>
</div>
""", unsafe_allow_html=True)

# ── TABS ───────────────────────────────────────────────────────────────────────
st.markdown('<div class="tabrow">', unsafe_allow_html=True)
t1, t2 = st.columns(2)
with t1:
    st.markdown(f'<div class="{"tab1on" if tab==1 else ""}">', unsafe_allow_html=True)
    if st.button(f"البطاقة الأولى  {len(c1)}/50", key="tb1"):
        st.session_state.tab=1; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
with t2:
    st.markdown(f'<div class="{"tab2on" if tab==2 else ""}">', unsafe_allow_html=True)
    if st.button(f"البطاقة الثانية  {len(c2)}/50", key="tb2"):
        st.session_state.tab=2; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── COUNTER ────────────────────────────────────────────────────────────────────
cnt = len(sel)
pct = cnt / MAX * 100
bc = ("#0055cc","#0099ff") if tab==1 else ("#008833","#00cc55")
nc_col = "#ff4444" if full else "#ffffff"
st.markdown(f"""
<div style="background:#0d0d14;border:1px solid #1a1a26;border-radius:10px;
  padding:8px 12px;display:flex;align-items:center;gap:8px;direction:rtl;margin:3px 0">
  <span style="font-size:0.7rem;color:#3a3a4a;white-space:nowrap">
    {'البطاقة الأولى' if tab==1 else 'البطاقة الثانية'}</span>
  <span style="font-size:1.25rem;font-weight:900;color:{nc_col};white-space:nowrap">
    {cnt}<span style="font-size:0.68rem;color:#222">/{MAX}</span></span>
  <div style="flex:1;height:5px;background:#111;border-radius:99px;overflow:hidden">
    <div style="width:{pct}%;height:100%;border-radius:99px;
      background:linear-gradient(90deg,{bc[0]},{bc[1]})"></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── GRID ───────────────────────────────────────────────────────────────────────
st.markdown('<div class="numrow">', unsafe_allow_html=True)
for row in range(9):
    cols = st.columns(10)
    for ci, col in enumerate(cols):
        n = row*10 + ci + 1
        i1, i2 = n in c1, n in c2
        lk = full and n not in sel
        if i1 and i2:  css = "n-sb"
        elif i1:        css = "n-s1"
        elif i2:        css = "n-s2"
        else:           css = ""
        if lk:          css += " n-lk"
        with col:
            st.markdown(f'<div class="{css}">', unsafe_allow_html=True)
            if st.button(str(n), key=f"n{n}"):
                if not lk: toggle(n); st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── ACTIONS ────────────────────────────────────────────────────────────────────
st.markdown('<div class="actrow">', unsafe_allow_html=True)
a1, a2, a3 = st.columns(3)
with a1:
    if st.button("🗑 مسح", key="rst"):
        if tab==1: st.session_state.c1=set()
        else:      st.session_state.c2=set()
        st.session_state.cards=[]; st.session_state.show=False; st.rerun()
with a2:
    if st.button("🗑 مسح الكل", key="rsta"):
        st.session_state.c1=set(); st.session_state.c2=set()
        st.session_state.cards=[]; st.session_state.show=False; st.rerun()
with a3:
    st.markdown(f'<div class="{"genbtn" if can_gen else "genbtn-off"}">', unsafe_allow_html=True)
    if st.button("🎯 توليد" if can_gen else "⚠️ أكمل", key="gen"):
        if can_gen: do_generate(); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── RESULTS ────────────────────────────────────────────────────────────────────
if st.session_state.show:
    vessel = sorted(c2 - c1)
    shared = sorted(c1 & c2)
    ss = set(shared)

    def rn(n, s):
        return f'<div style="width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.58rem;font-weight:700;{s}">{n}</div>'

    vh = "".join(rn(n,"background:#0055cc22;color:#0099ff;border:1px solid #0055cc44") for n in vessel)
    sh = "".join(rn(n,"background:#ffffff08;color:#444;border:1px solid #1a1a2a") for n in shared)

    st.markdown(f"""
    <div style="background:#0d0d14;border:1px solid #1a1a26;border-radius:12px;
      padding:12px;direction:rtl;margin-top:6px">
      <div style="text-align:center;font-size:0.82rem;font-weight:900;margin-bottom:9px">📊 التحليل</div>
      <div style="display:flex;gap:8px">
        <div style="flex:1">
          <div style="font-size:0.6rem;font-weight:700;color:#0099ff;margin-bottom:4px">
            الوعاء ({len(vessel)})</div>
          <div style="display:flex;flex-wrap:wrap;gap:2px">{vh}</div>
        </div>
        <div style="flex:1">
          <div style="font-size:0.6rem;font-weight:700;color:#444;margin-bottom:4px">
            المشترك ({len(shared)})</div>
          <div style="display:flex;flex-wrap:wrap;gap:2px">{sh}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    for i, card in enumerate(st.session_state.cards):
        nh = "".join(
            f'<div style="width:30px;height:30px;border-radius:50%;display:flex;align-items:center;'
            f'justify-content:center;font-size:0.65rem;font-weight:700;'
            f'{"background:#6600ff22;color:#aa66ff;border:1px solid #6600ff44" if n in ss else "background:#111;color:#aaa;border:1px solid #1a1a2a"}">{n}</div>'
            for n in card)
        st.markdown(f"""
        <div style="background:#080810;border:1px solid #1a1a26;border-radius:10px;
          padding:10px;margin-top:6px;direction:rtl">
          <div style="display:flex;justify-content:space-between;margin-bottom:6px">
            <span style="font-size:0.7rem;font-weight:700;color:#3a3a4a">البطاقة {i+1}</span>
            <span style="font-size:0.6rem;color:#1a1a2a">{len(card)} أرقام</span>
          </div>
          <div style="display:flex;flex-wrap:wrap;gap:4px">{nh}</div>
        </div>
        """, unsafe_allow_html=True)