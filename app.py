import streamlit as st
import streamlit.components.v1 as components
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
    margin: 0; padding: 0;
}
.block-container { padding: 0 !important; max-width: 100% !important; }
header, footer, #MainMenu { display: none !important; }
iframe { border: none !important; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
for key, default in [
    ("card1", []),
    ("card2", []),
    ("active_tab", 1),
    ("generated_cards", []),
    ("show_results", False),
    ("action", None),
    ("toggle_num", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default

MAX_SELECT = 50

# ── PROCESS ACTIONS ───────────────────────────────────────────────────────────
def process_action(action, data=None):
    c1 = set(st.session_state.card1)
    c2 = set(st.session_state.card2)
    tab = st.session_state.active_tab

    if action == "toggle":
        n = int(data)
        s = c1 if tab == 1 else c2
        if n in s:
            s.discard(n)
        else:
            if len(s) < MAX_SELECT:
                s.add(n)
        if tab == 1:
            st.session_state.card1 = sorted(s)
        else:
            st.session_state.card2 = sorted(s)
        st.session_state.generated_cards = []
        st.session_state.show_results = False

    elif action == "tab":
        st.session_state.active_tab = int(data)
        st.session_state.generated_cards = []
        st.session_state.show_results = False

    elif action == "reset":
        if tab == 1:
            st.session_state.card1 = []
        else:
            st.session_state.card2 = []
        st.session_state.generated_cards = []
        st.session_state.show_results = False

    elif action == "reset_all":
        st.session_state.card1 = []
        st.session_state.card2 = []
        st.session_state.generated_cards = []
        st.session_state.show_results = False

    elif action == "generate":
        c1s = set(st.session_state.card1)
        c2s = set(st.session_state.card2)
        shared = sorted(c1s & c2s, reverse=True)
        vessel = sorted(c2s - c1s)

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
        take = from_vessel[:min(total_needed, len(from_vessel))]
        shortage = total_needed - len(take)
        from_shared = shared[:shortage]
        all_nums = take + from_shared
        random.shuffle(all_nums)

        cards = []
        for i in range(num_cards):
            chunk = sorted(all_nums[i*5:(i+1)*5])
            cards.append(chunk)

        st.session_state.generated_cards = cards
        st.session_state.show_results = True

# ── CHECK FOR INCOMING MESSAGE ────────────────────────────────────────────────
params = st.query_params
if "action" in params and "data" in params:
    process_action(params["action"], params["data"])
    st.query_params.clear()
    st.rerun()

# ── BUILD STATE FOR JS ────────────────────────────────────────────────────────
c1 = set(st.session_state.card1)
c2 = set(st.session_state.card2)
tab = st.session_state.active_tab
can_generate = len(c1) == MAX_SELECT and len(c2) == MAX_SELECT
shared_set = c1 & c2
vessel_set = c2 - c1

state_json = json.dumps({
    "card1": list(c1),
    "card2": list(c2),
    "tab": tab,
    "canGenerate": can_generate,
    "generatedCards": st.session_state.generated_cards,
    "showResults": st.session_state.show_results,
    "vessel": sorted(vessel_set),
    "shared": sorted(shared_set),
})

# ── HTML/JS APP ───────────────────────────────────────────────────────────────
html = """
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap" rel="stylesheet">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: 'Tajawal', sans-serif;
    background: #0a0a0f;
    color: #fff;
    min-height: 100vh;
    padding: 12px 8px 32px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

/* TITLE */
.title {
    font-size: 2rem; font-weight: 900; letter-spacing: 4px;
    background: linear-gradient(135deg, #00d4ff, #7b2fff, #ff6b35);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    text-align: center; margin-bottom: 2px;
}
.subtitle { font-size: 0.72rem; color: #444; letter-spacing: 2px; text-align: center; margin-bottom: 12px; }

/* TABS */
.tab-bar {
    display: flex; gap: 6px; width: 100%; max-width: 500px;
    background: #13131a; border-radius: 12px; padding: 5px;
    border: 1px solid #1e1e2e; margin-bottom: 10px;
}
.tab-btn {
    flex: 1; padding: 9px; border-radius: 9px; border: none;
    font-family: 'Tajawal', sans-serif; font-size: 0.85rem; font-weight: 700;
    cursor: pointer; transition: all 0.2s; color: #555; background: transparent;
}
.tab-btn.active-1 { background: linear-gradient(135deg,#0066ff,#00d4ff); color:#fff; box-shadow:0 0 16px #0066ff44; }
.tab-btn.active-2 { background: linear-gradient(135deg,#00a844,#00ff88); color:#fff; box-shadow:0 0 16px #00a84444; }

/* COUNTER */
.counter {
    width: 100%; max-width: 500px; display: flex; align-items: center;
    gap: 10px; background: #13131a; border: 1px solid #1e1e2e;
    border-radius: 12px; padding: 10px 14px; margin-bottom: 10px;
}
.c-label { font-size: 0.78rem; color: #555; white-space: nowrap; }
.c-num { font-size: 1.4rem; font-weight: 900; white-space: nowrap; }
.c-num.full { color: #ff4444; }
.c-num span { font-size: 0.8rem; color: #333; }
.c-bar-bg { flex:1; height:6px; background:#1e1e2e; border-radius:99px; overflow:hidden; }
.c-bar { height:100%; border-radius:99px; transition:width 0.3s; }
.bar-1 { background: linear-gradient(90deg,#0066ff,#00d4ff); }
.bar-2 { background: linear-gradient(90deg,#00a844,#00ff88); }

/* GRID */
.grid {
    width: 100%; max-width: 500px;
    display: grid; grid-template-columns: repeat(10, 1fr);
    gap: 4px; margin-bottom: 12px;
}
.num {
    aspect-ratio: 1; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: clamp(0.52rem, 2vw, 0.75rem); font-weight: 700;
    cursor: pointer; border: 1.5px solid #1e1e2e;
    background: #13131a; color: #444;
    transition: transform 0.12s;
    -webkit-tap-highlight-color: transparent;
    user-select: none;
}
.num:active { transform: scale(0.82); }
.num.locked { cursor: not-allowed; opacity: 0.4; }
.num.s1 { background:#0066ff; border-color:#00d4ff; color:#fff; box-shadow:0 0 8px #0066ff66; }
.num.s2 { background:#00a844; border-color:#00ff88; color:#fff; box-shadow:0 0 8px #00a84466; }
.num.sb {
    border-color:#aaa; color:#fff;
    background: linear-gradient(135deg, #0066ff 50%, #00a844 50%);
    box-shadow: 0 0 10px #ffffff22;
}

/* ACTIONS */
.actions { width:100%; max-width:500px; display:flex; gap:6px; margin-bottom:10px; }
.abtn {
    flex:1; padding:11px 6px; border-radius:11px; border:none;
    font-family:'Tajawal',sans-serif; font-size:0.82rem; font-weight:700;
    cursor:pointer; transition:all 0.2s;
}
.abtn-reset { background:#1e1e2e; color:#777; }
.abtn-reset:active { background:#2a2a3e; }
.abtn-gen {
    background: linear-gradient(135deg,#7b2fff,#ff6b35);
    color:#fff; box-shadow:0 0 14px #7b2fff44;
}
.abtn-gen:disabled { opacity:0.3; cursor:not-allowed; box-shadow:none; }

/* RESULTS */
.results { width:100%; max-width:500px; }
.panel {
    background:#13131a; border:1px solid #1e1e2e;
    border-radius:14px; padding:14px; margin-bottom:10px;
}
.panel-title { font-size:0.9rem; font-weight:900; text-align:center; margin-bottom:10px; letter-spacing:1px; }
.stats-row { display:flex; gap:10px; }
.stat-col { flex:1; }
.stat-label { font-size:0.68rem; font-weight:700; letter-spacing:1px; text-transform:uppercase; margin-bottom:6px; }
.lv { color:#00d4ff; } .ls { color:#888; }
.nums-wrap { display:flex; flex-wrap:wrap; gap:3px; }
.rn {
    width:26px; height:26px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-size:0.62rem; font-weight:700;
}
.rn-v { background:#0066ff22; color:#00d4ff; border:1px solid #0066ff44; }
.rn-s { background:#ffffff0a; color:#666; border:1px solid #2a2a3e; }

/* CARDS */
.gen-card {
    background:#0d0d14; border:1px solid #1e1e2e;
    border-radius:12px; padding:12px; margin-bottom:8px;
}
.gc-header { display:flex; justify-content:space-between; margin-bottom:8px; }
.gc-title { font-size:0.75rem; font-weight:700; color:#555; }
.gc-count { font-size:0.68rem; color:#333; }
.gc-nums { display:flex; flex-wrap:wrap; gap:4px; }
.gn {
    width:32px; height:32px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-size:0.68rem; font-weight:700;
    background:#13131a; color:#bbb; border:1px solid #2a2a3e;
}
.gn-shared { background:#7b2fff22; color:#bf88ff; border-color:#7b2fff55; }
</style>
</head>
<body>

<div class="title">ميشو</div>
<div class="subtitle">لوحة الأرقام</div>

<div class="tab-bar">
  <button class="tab-btn" id="tab1btn" onclick="setTab(1)">البطاقة الأولى</button>
  <button class="tab-btn" id="tab2btn" onclick="setTab(2)">البطاقة الثانية</button>
</div>

<div class="counter" id="counterWrap">
  <span class="c-label" id="cLabel"></span>
  <span class="c-num" id="cNum"></span>
  <div class="c-bar-bg"><div class="c-bar" id="cBar"></div></div>
</div>

<div class="grid" id="grid"></div>

<div class="actions">
  <button class="abtn abtn-reset" onclick="sendAction('reset','0')">مسح البطاقة</button>
  <button class="abtn abtn-reset" onclick="sendAction('reset_all','0')">مسح الكل</button>
  <button class="abtn abtn-gen" id="genBtn" onclick="sendAction('generate','0')">🎯 توليد</button>
</div>

<div class="results" id="results"></div>

<script>
const STATE = """ + state_json + """;

const c1 = new Set(STATE.card1);
const c2 = new Set(STATE.card2);
let activeTab = STATE.tab;

function sendAction(action, data) {
  const url = new URL(window.location.href);
  url.searchParams.set('action', action);
  url.searchParams.set('data', data);
  window.location.href = url.toString();
}

function setTab(t) { sendAction('tab', t); }
function toggleNum(n) { sendAction('toggle', n); }

function render() {
  const sel = activeTab === 1 ? c1 : c2;
  const count = sel.size;
  const full = count >= 50;

  // tabs
  document.getElementById('tab1btn').className = 'tab-btn' + (activeTab===1?' active-1':'');
  document.getElementById('tab2btn').className = 'tab-btn' + (activeTab===2?' active-2':'');
  document.getElementById('tab1btn').textContent = `البطاقة الأولى (${c1.size})`;
  document.getElementById('tab2btn').textContent = `البطاقة الثانية (${c2.size})`;

  // counter
  document.getElementById('cLabel').textContent = activeTab===1 ? 'البطاقة الأولى' : 'البطاقة الثانية';
  const cn = document.getElementById('cNum');
  cn.className = 'c-num' + (full?' full':'');
  cn.innerHTML = `${count}<span>/50</span>`;
  const bar = document.getElementById('cBar');
  bar.style.width = (count/50*100)+'%';
  bar.className = 'c-bar ' + (activeTab===1?'bar-1':'bar-2');

  // grid
  const grid = document.getElementById('grid');
  grid.innerHTML = '';
  for (let n = 1; n <= 90; n++) {
    const in1 = c1.has(n), in2 = c2.has(n);
    let cls = 'num';
    if (in1 && in2) cls += ' sb';
    else if (in1) cls += ' s1';
    else if (in2) cls += ' s2';

    const locked = full && !sel.has(n);
    if (locked) cls += ' locked';

    const div = document.createElement('div');
    div.className = cls;
    div.textContent = n;
    if (!locked) div.onclick = () => toggleNum(n);
    grid.appendChild(div);
  }

  // gen button
  const genBtn = document.getElementById('genBtn');
  const canGen = c1.size === 50 && c2.size === 50;
  genBtn.disabled = !canGen;
  genBtn.textContent = canGen ? '🎯 توليد' : '⚠️ أكمل الاختيار';

  // results
  if (STATE.showResults) {
    renderResults();
  }
}

function renderResults() {
  const vessel = STATE.vessel;
  const shared = STATE.shared;
  const cards = STATE.generatedCards;
  const sharedSet = new Set(shared);

  let html = `<div class="panel">
    <div class="panel-title">📊 التحليل</div>
    <div class="stats-row">
      <div class="stat-col">
        <div class="stat-label lv">الوعاء (${vessel.length})</div>
        <div class="nums-wrap">${vessel.map(n=>`<div class="rn rn-v">${n}</div>`).join('')}</div>
      </div>
      <div class="stat-col">
        <div class="stat-label ls">المشترك (${shared.length})</div>
        <div class="nums-wrap">${shared.map(n=>`<div class="rn rn-s">${n}</div>`).join('')}</div>
      </div>
    </div>
  </div>`;

  cards.forEach((card, i) => {
    const nums = card.map(n => {
      const cls = sharedSet.has(n) ? 'gn gn-shared' : 'gn';
      return `<div class="${cls}">${n}</div>`;
    }).join('');
    html += `<div class="gen-card">
      <div class="gc-header">
        <span class="gc-title">البطاقة ${i+1}</span>
        <span class="gc-count">${card.length} أرقام</span>
      </div>
      <div class="gc-nums">${nums}</div>
    </div>`;
  });

  document.getElementById('results').innerHTML = html;
}

render();
</script>
</body>
</html>
"""

components.html(html, height=2200, scrolling=True)