import streamlit as st
import random
import json

st.set_page_config(
    page_title="ميشو",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #0a0a0f !important;
    margin: 0 !important; padding: 0 !important;
    overflow: hidden !important;
}
.block-container { padding: 0 !important; max-width: 100% !important; }
header, footer, #MainMenu { display: none !important; }
iframe { border: none !important; display: block !important; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──────────────────────────────────────────────────────────────
for k, v in [("c1", []), ("c2", []), ("tab", 1), ("cards", []), ("show", False)]:
    if k not in st.session_state:
        st.session_state[k] = v

MAX = 50

def process(action, data=""):
    c1 = set(st.session_state.c1)
    c2 = set(st.session_state.c2)
    tab = st.session_state.tab

    if action == "toggle":
        n = int(data)
        s = c1 if tab == 1 else c2
        if n in s: s.discard(n)
        elif len(s) < MAX: s.add(n)
        st.session_state.c1 = sorted(c1) if tab == 1 else sorted(c1)
        st.session_state.c2 = sorted(c2) if tab == 2 else sorted(c2)
        if tab == 1: st.session_state.c1 = sorted(s)
        else:        st.session_state.c2 = sorted(s)
        st.session_state.cards = []
        st.session_state.show = False

    elif action == "tab":
        st.session_state.tab = int(data)

    elif action == "reset":
        if tab == 1: st.session_state.c1 = []
        else:        st.session_state.c2 = []
        st.session_state.cards = []
        st.session_state.show = False

    elif action == "reset_all":
        st.session_state.c1 = []
        st.session_state.c2 = []
        st.session_state.cards = []
        st.session_state.show = False

    elif action == "generate":
        c1s = set(st.session_state.c1)
        c2s = set(st.session_state.c2)
        shared = sorted(c1s & c2s, reverse=True)
        vessel = sorted(c2s - c1s)
        v = len(vessel)
        n_cards = v // 5
        rem = v % 5
        if rem >= 4: n_cards += 1
        if n_cards == 0: n_cards = 1
        total = n_cards * 5
        pool = vessel.copy(); random.shuffle(pool)
        take = pool[:min(total, len(pool))]
        shortage = total - len(take)
        extra = shared[:shortage]
        all_n = take + extra; random.shuffle(all_n)
        st.session_state.cards = [sorted(all_n[i*5:(i+1)*5]) for i in range(n_cards)]
        st.session_state.show = True

# ── HANDLE PARAMS ──────────────────────────────────────────────────────────────
p = st.query_params
if "a" in p:
    process(p["a"], p.get("d", ""))
    st.query_params.clear()
    st.rerun()

# ── BUILD STATE JSON ───────────────────────────────────────────────────────────
state = {
    "c1": st.session_state.c1,
    "c2": st.session_state.c2,
    "tab": st.session_state.tab,
    "cards": st.session_state.cards,
    "show": st.session_state.show,
    "vessel": sorted(set(st.session_state.c2) - set(st.session_state.c1)),
    "shared": sorted(set(st.session_state.c1) & set(st.session_state.c2)),
}

# ── FULL HTML APP ──────────────────────────────────────────────────────────────
html = f"""<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}}
body{{
  font-family:'Tajawal',sans-serif;
  background:#0a0a0f;color:#fff;
  min-height:100vh;
  padding:10px 8px 60px;
  display:flex;flex-direction:column;align-items:center;
}}
.w{{width:100%;max-width:460px}}

/* TITLE */
.ttl{{font-size:1.9rem;font-weight:900;letter-spacing:3px;text-align:center;
  background:linear-gradient(135deg,#00d4ff,#7b2fff,#ff6b35);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  margin-bottom:2px}}
.sub{{font-size:0.68rem;color:#444;letter-spacing:2px;text-align:center;margin-bottom:10px}}

/* TABS */
.tabs{{display:flex;gap:6px;background:#13131a;border-radius:12px;
  padding:4px;border:1px solid #1e1e2e;margin-bottom:8px}}
.tbtn{{flex:1;padding:9px 4px;border-radius:9px;border:none;
  font-family:'Tajawal',sans-serif;font-size:0.85rem;font-weight:700;
  cursor:pointer;color:#555;background:transparent;transition:all .2s}}
.tbtn.a1{{background:linear-gradient(135deg,#0066ff,#00d4ff);color:#fff;box-shadow:0 0 14px #0066ff44}}
.tbtn.a2{{background:linear-gradient(135deg,#00a844,#00ff88);color:#fff;box-shadow:0 0 14px #00a84444}}

/* COUNTER */
.ctr{{display:flex;align-items:center;gap:8px;background:#13131a;
  border:1px solid #1e1e2e;border-radius:11px;padding:9px 12px;margin-bottom:8px}}
.clbl{{font-size:0.75rem;color:#555;white-space:nowrap}}
.cnum{{font-size:1.3rem;font-weight:900;white-space:nowrap}}
.cnum.full{{color:#ff4444}}
.cnum span{{font-size:0.75rem;color:#333}}
.cbar-bg{{flex:1;height:5px;background:#1e1e2e;border-radius:99px;overflow:hidden}}
.cbar{{height:100%;border-radius:99px;transition:width .3s}}
.b1{{background:linear-gradient(90deg,#0066ff,#00d4ff)}}
.b2{{background:linear-gradient(90deg,#00a844,#00ff88)}}

/* GRID */
.grid{{
  display:grid;
  grid-template-columns:repeat(10,1fr);
  gap:4px;
  width:100%;
  margin-bottom:10px;
}}
.num{{
  aspect-ratio:1;
  border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-size:clamp(0.5rem,3.2vw,0.78rem);
  font-weight:700;
  cursor:pointer;
  border:1.5px solid #1e1e2e;
  background:#13131a;
  color:#555;
  transition:transform .12s;
  user-select:none;
}}
.num:active{{transform:scale(0.8)}}
.num.s1{{background:#0066ff;border-color:#00d4ff;color:#fff;box-shadow:0 0 7px #0066ff88}}
.num.s2{{background:#00a844;border-color:#00ff88;color:#fff;box-shadow:0 0 7px #00a84488}}
.num.sb{{background:linear-gradient(135deg,#0066ff 50%,#00a844 50%);border-color:#aaa;color:#fff;box-shadow:0 0 8px #fff2}}
.num.lk{{opacity:.25;cursor:not-allowed;pointer-events:none}}

/* ACTIONS */
.acts{{display:flex;gap:6px;width:100%;margin-bottom:10px}}
.abtn{{flex:1;padding:11px 4px;border-radius:10px;border:none;
  font-family:'Tajawal',sans-serif;font-size:0.8rem;font-weight:700;
  cursor:pointer;background:#1e1e2e;color:#888;transition:all .2s}}
.abtn:active{{background:#2a2a3e}}
.gbtn{{background:linear-gradient(135deg,#7b2fff,#ff6b35);color:#fff;box-shadow:0 0 14px #7b2fff44}}
.gbtn:disabled{{background:#1a1a2a;color:#333;box-shadow:none;cursor:not-allowed}}

/* RESULTS */
.panel{{background:#13131a;border:1px solid #1e1e2e;border-radius:13px;padding:13px;margin-bottom:10px}}
.ptitle{{text-align:center;font-size:0.88rem;font-weight:900;margin-bottom:10px}}
.srow{{display:flex;gap:8px}}
.scol{{flex:1}}
.slbl{{font-size:0.65rem;font-weight:700;letter-spacing:1px;margin-bottom:5px;text-transform:uppercase}}
.lv{{color:#00d4ff}}.ls{{color:#888}}
.rnums{{display:flex;flex-wrap:wrap;gap:3px}}
.rn{{width:25px;height:25px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.6rem;font-weight:700}}
.rnv{{background:#0066ff22;color:#00d4ff;border:1px solid #0066ff44}}
.rns{{background:#fff1;color:#666;border:1px solid #2a2a3e}}

/* CARDS */
.gcard{{background:#0d0d14;border:1px solid #1e1e2e;border-radius:11px;padding:11px;margin-bottom:8px}}
.gch{{display:flex;justify-content:space-between;margin-bottom:7px}}
.gct{{font-size:0.72rem;font-weight:700;color:#555}}
.gcc{{font-size:0.65rem;color:#333}}
.gcn{{display:flex;flex-wrap:wrap;gap:4px}}
.gn{{width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.65rem;font-weight:700;background:#13131a;color:#bbb;border:1px solid #2a2a3e}}
.gnx{{background:#7b2fff22;color:#bf88ff;border-color:#7b2fff55}}
</style>
</head>
<body>
<div class="w">
  <div class="ttl">ميشو</div>
  <div class="sub">لوحة الأرقام</div>

  <div class="tabs w" id="tabs"></div>
  <div class="ctr w" id="ctr"></div>
  <div class="grid w" id="grid"></div>
  <div class="acts w" id="acts"></div>
  <div id="results"></div>
</div>

<script>
const S = {json.dumps(state, ensure_ascii=False)};
const c1 = new Set(S.c1), c2 = new Set(S.c2);
let tab = S.tab;

function go(a, d='') {{
  const base = window.parent.location.href.split('?')[0];
  window.parent.location.href = base + '?a=' + a + '&d=' + d;
}}

function render() {{
  const sel = tab===1 ? c1 : c2;
  const cnt = sel.size;
  const full = cnt >= 50;
  const canGen = c1.size===50 && c2.size===50;

  // TABS
  document.getElementById('tabs').innerHTML = `
    <button class="tbtn ${{tab===1?'a1':''}}" onclick="go('tab','1')">البطاقة الأولى (${{c1.size}})</button>
    <button class="tbtn ${{tab===2?'a2':''}}" onclick="go('tab','2')">البطاقة الثانية (${{c2.size}})</button>`;

  // COUNTER
  const col = tab===1 ? '#0066ff' : '#00a844';
  const col2 = tab===1 ? '#00d4ff' : '#00ff88';
  const pct = cnt/50*100;
  document.getElementById('ctr').innerHTML = `
    <span class="clbl">${{tab===1?'البطاقة الأولى':'البطاقة الثانية'}}</span>
    <span class="cnum ${{full?'full':''}}">${{cnt}}<span>/50</span></span>
    <div class="cbar-bg"><div class="cbar ${{tab===1?'b1':'b2'}}" style="width:${{pct}}%"></div></div>`;

  // GRID
  let gh = '';
  for(let n=1;n<=90;n++){{
    const i1=c1.has(n),i2=c2.has(n);
    const lk = full && !sel.has(n);
    let cls = 'num';
    if(i1&&i2) cls+=' sb';
    else if(i1) cls+=' s1';
    else if(i2) cls+=' s2';
    if(lk) cls+=' lk';
    gh += `<div class="${{cls}}" onclick="go('toggle','${{n}}')">${{n}}</div>`;
  }}
  document.getElementById('grid').innerHTML = gh;

  // ACTIONS
  document.getElementById('acts').innerHTML = `
    <button class="abtn" onclick="go('reset')">🗑 مسح</button>
    <button class="abtn" onclick="go('reset_all')">🗑 مسح الكل</button>
    <button class="abtn gbtn" onclick="${{canGen?'go(\\'generate\\')':\\'\\'}}" ${{canGen?'':'disabled'}}>
      ${{canGen?'🎯 توليد':'⚠️ أكمل'}}
    </button>`;

  // RESULTS
  if(S.show) renderResults();
}}

function renderResults() {{
  const vessel = S.vessel, shared = S.shared, cards = S.cards;
  const shSet = new Set(shared);

  const vHTML = vessel.map(n=>`<div class="rn rnv">${{n}}</div>`).join('');
  const sHTML = shared.map(n=>`<div class="rn rns">${{n}}</div>`).join('');

  let html = `<div class="panel">
    <div class="ptitle">📊 التحليل</div>
    <div class="srow">
      <div class="scol"><div class="slbl lv">الوعاء (${{vessel.length}})</div><div class="rnums">${{vHTML}}</div></div>
      <div class="scol"><div class="slbl ls">المشترك (${{shared.length}})</div><div class="rnums">${{sHTML}}</div></div>
    </div></div>`;

  cards.forEach((card,i)=>{{
    const ns = card.map(n=>`<div class="gn ${{shSet.has(n)?'gnx':''}}">${{n}}</div>`).join('');
    html += `<div class="gcard">
      <div class="gch"><span class="gct">البطاقة ${{i+1}}</span><span class="gcc">${{card.length}} أرقام</span></div>
      <div class="gcn">${{ns}}</div></div>`;
  }});

  document.getElementById('results').innerHTML = html;
}}

render();
</script>
</body></html>"""

st.components.v1.html(html, height=3000, scrolling=True)