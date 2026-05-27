import streamlit as st
import random

st.set_page_config(
    page_title="ميشو",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS - نخفي كل عناصر streamlit الزيادة ونضبط المسافات
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #0a0a0f !important;
    font-family: 'Tajawal', sans-serif !important;
}
.block-container {
    padding: 8px 4px 40px !important;
    max-width: 100% !important;
}
header, footer, #MainMenu { display: none !important; }

/* إزالة كل المسافات الزيادة */
[data-testid="stVerticalBlock"] > div { gap: 0 !important; }
.element-container { margin: 0 !important; padding: 0 !important; }

/* أزرار الأرقام */
[data-testid="stHorizontalBlock"] {
    gap: 3px !important;
    flex-wrap: nowrap !important;
}
[data-testid="stHorizontalBlock"] > div {
    flex: 1 !important;
    min-width: 0 !important;
    padding: 0 !important;
}

div.stButton > button {
    width: 100% !important;
    font-family: 'Tajawal', sans-serif !important;
    font-weight: 700 !important;
    padding: 0 !important;
    min-height: unset !important;
    line-height: 1 !important;
}

/* أزرار الأرقام فقط - داخل .numrow */
.numrow div.stButton > button {
    aspect-ratio: 1 !important;
    border-radius: 50% !important;
    font-size: clamp(0.45rem, 2.8vw, 0.72rem) !important;
    border: 1.5px solid #222 !important;
    background: #111 !important;
    color: #555 !important;
}

/* الألوان */
.n-s1 div.stButton > button { background: #0055dd !important; border-color: #00aaff !important; color: #fff !important; }
.n-s2 div.stButton > button { background: #009933 !important; border-color: #00ee66 !important; color: #fff !important; }
.n-sb div.stButton > button {
    background: linear-gradient(135deg,#0055dd 50%,#009933 50%) !important;
    border-color: #888 !important; color: #fff !important;
}
.n-lk div.stButton > button { opacity: 0.2 !important; pointer-events: none !important; }

/* أزرار التابات والإجراءات */
.tabrow div.stButton > button {
    aspect-ratio: unset !important;
    border-radius: 10px !important;
    padding: 10px 6px !important;
    font-size: 0.82rem !important;
    border: 1px solid #1e1e2e !important;
    background: #13131a !important;
    color: #555 !important;
}
.tab1on div.stButton > button {
    background: linear-gradient(135deg,#0055dd,#00aaff) !important;
    color: #fff !important; border: none !important;
}
.tab2on div.stButton > button {
    background: linear-gradient(135deg,#009933,#00ee66) !important;
    color: #fff !important; border: none !important;
}

.actrow div.stButton > button {
    aspect-ratio: unset !important;
    border-radius: 10px !important;
    padding: 10px 4px !important;
    font-size: 0.78rem !important;
    background: #1a1a2a !important;
    color: #777 !important;
    border: 1px solid #222 !important;
}
.genbtn div.stButton > button {
    background: linear-gradient(135deg,#7722ff,#ff5522) !important;
    color: #fff !important; border: none !important;
}
.genbtn-off div.stButton > button {
    background: #111 !important; color: #333 !important;
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
<div style="text-align:center;padding:6px 0 6px;direction:rtl">
  <span style="font-size:1.9rem;font-weight:900;letter-spacing:3px;
    background:linear-gradient(135deg,#00ccff,#8833ff,#ff5522);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent">ميشو</span><br>
  <span style="font-size:0.65rem;color:#333;letter-spacing:2px">لوحة الأرقام</span>
</div>
""", unsafe_allow_html=True)

# ── TABS ───────────────────────────────────────────────────────────────────────
st.markdown('<div class="tabrow">', unsafe_allow_html=True)
t1,t2 = st.columns(2)
with t1:
    st.markdown(f'<div class="{"tab1on" if tab==1 else ""}">', unsafe_allow_html=True)
    if st.button(f"● البطاقة الأولى ({len(c1)})", key="tb1"):
        st.session_state.tab=1; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
with t2:
    st.markdown(f'<div class="{"tab2on" if tab==2 else ""}">', unsafe_allow_html=True)
    if st.button(f"● البطاقة الثانية ({len(c2)})", key="tb2"):
        st.session_state.tab=2; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── COUNTER ────────────────────────────────────────────────────────────────────
cnt = len(sel)
pct = cnt/MAX*100
bc = ("#0055dd","#00aaff") if tab==1 else ("#009933","#00ee66")
nc = "#ff4444" if full else "#fff"
st.markdown(f"""
<div style="background:#0d0d18;border:1px solid #1a1a2a;border-radius:11px;
  padding:9px 12px;display:flex;align-items:center;gap:8px;direction:rtl;margin:4px 0">
  <span style="font-size:0.72rem;color:#444;white-space:nowrap">
    {'البطاقة الأولى' if tab==1 else 'البطاقة الثانية'}</span>
  <span style="font-size:1.3rem;font-weight:900;color:{nc};white-space:nowrap">
    {cnt}<span style="font-size:0.72rem;color:#2a2a2a">/{MAX}</span></span>
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
    for ci,col in enumerate(cols):
        n = row*10+ci+1
        i1,i2 = n in c1, n in c2
        lk = full and n not in sel
        if i1 and i2: css="n-sb"
        elif i1:       css="n-s1"
        elif i2:       css="n-s2"
        else:          css=""
        if lk:         css+=" n-lk"
        with col:
            st.markdown(f'<div class="{css}">', unsafe_allow_html=True)
            if st.button(str(n), key=f"n{n}"):
                if not lk: toggle(n); st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── ACTIONS ────────────────────────────────────────────────────────────────────
st.markdown('<div class="actrow">', unsafe_allow_html=True)
a1,a2,a3 = st.columns(3)
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
    vessel = sorted(c2-c1)
    shared = sorted(c1&c2)
    ss = set(shared)

    def rn(n,cls): return f'<div style="width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.58rem;font-weight:700;{cls}">{n}</div>'

    vh = "".join(rn(n,"background:#0055dd22;color:#00aaff;border:1px solid #0055dd44") for n in vessel)
    sh = "".join(rn(n,"background:#fff1;color:#555;border:1px solid #1a1a2a") for n in shared)

    st.markdown(f"""
    <div style="background:#0d0d18;border:1px solid #1a1a2a;border-radius:13px;padding:12px;direction:rtl;margin-top:8px">
      <div style="text-align:center;font-size:0.85rem;font-weight:900;margin-bottom:10px">📊 التحليل</div>
      <div style="display:flex;gap:10px">
        <div style="flex:1">
          <div style="font-size:0.62rem;font-weight:700;color:#00aaff;margin-bottom:5px">الوعاء ({len(vessel)})</div>
          <div style="display:flex;flex-wrap:wrap;gap:3px">{vh}</div>
        </div>
        <div style="flex:1">
          <div style="font-size:0.62rem;font-weight:700;color:#555;margin-bottom:5px">المشترك ({len(shared)})</div>
          <div style="display:flex;flex-wrap:wrap;gap:3px">{sh}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    for i,card in enumerate(st.session_state.cards):
        nh = "".join(
            f'<div style="width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.65rem;font-weight:700;{"background:#7722ff22;color:#bb77ff;border:1px solid #7722ff44" if n in ss else "background:#111;color:#aaa;border:1px solid #1a1a2a"}">{n}</div>'
            for n in card)
        st.markdown(f"""
        <div style="background:#080810;border:1px solid #1a1a2a;border-radius:11px;padding:11px;margin-top:8px;direction:rtl">
          <div style="display:flex;justify-content:space-between;margin-bottom:7px">
            <span style="font-size:0.72rem;font-weight:700;color:#444">البطاقة {i+1}</span>
            <span style="font-size:0.62rem;color:#222">{len(card)} أرقام</span>
          </div>
          <div style="display:flex;flex-wrap:wrap;gap:4px">{nh}</div>
        </div>
        """, unsafe_allow_html=True)