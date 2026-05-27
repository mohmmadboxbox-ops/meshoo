import streamlit as st
import streamlit.components.v1 as components
import random
import json

st.set_page_config(page_title="ميشو", page_icon="🎯", layout="wide", initial_sidebar_state="collapsed")

# ── CSS (حل مشكلة التكسير والترتيب للموبايل) ──────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #0a0a0f !important;
    font-family: 'Tajawal', sans-serif !important;
    direction: rtl;
}
.block-container { padding: 16px 8px 40px !important; max-width: 520px !important; margin: 0 auto !important; }
header, footer, #MainMenu { display: none !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }
.element-container { margin: 0 !important; padding: 0 !important; min-height: 0 !important; }

/* 1. السحر هنا: غصب Streamlit يخلي الأعمدة أفقية بالموبايل وما يكسرها */
[data-testid="stHorizontalBlock"] {
    flex-direction: row-reverse !important; /* من اليمين لليسار */
    flex-wrap: nowrap !important;
    align-items: center !important;
    gap: 4px !important;
    margin-bottom: 6px !important;
}
[data-testid="column"] {
    width: auto !important;
    flex: 1 1 0% !important;
    min-width: 0 !important;
    padding: 0 !important;
}

/* 2. الشكل الأساسي لكل الأزرار */
div.stButton > button {
    width: 100% !important;
    border: 1.5px solid #1e1e2e !important;
    background: #13131a !important;
    color: #555 !important;
    font-family: 'Tajawal', sans-serif !important;
    font-weight: 700 !important;
    transition: all 0.15s !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    line-height: 1 !important;
}
div.stButton > button:active { transform: scale(0.85) !important; }
div.stButton > button p { margin: 0 !important; }

/* 3. التصاميم اللي يضيفها الجافاسكربت (بدون أكواد معقدة) */
.text-btn {
    border-radius: 10px !important;
    min-height: 42px !important;
    font-size: 0.85rem !important;
}
.num-btn {
    border-radius: 50% !important;
    height: clamp(30px, 8vw, 42px) !important; /* يجبر الزر يكون دائرة مثالية */
    min-height: 0 !important;
    padding: 0 !important;
    font-size: clamp(0.6rem, 2.2vw, 0.9rem) !important;
}

/* 4. ألوان الأرقام والتابات */
.sel-1 { background: #0066ff !important; border-color: #00d4ff !important; color: #fff !important; box-shadow: 0 0 8px #0066ff66 !important; }
.sel-2 { background: #00a844 !important; border-color: #00ff88 !important; color: #fff !important; box-shadow: 0 0 8px #00a84466 !important; }
.sel-both { background: linear-gradient(135deg, #0066ff 50%, #00a844 50%) !important; border-color: #aaa !important; color: #fff !important; }
.locked { opacity: 0.25 !important; pointer-events: none !important; }

.tab-active-1 { background: linear-gradient(135deg, #0066ff, #00d4ff) !important; color: #fff !important; border: none !important; box-shadow: 0 0 12px #0066ff55 !important; }
.tab-active-2 { background: linear-gradient(135deg, #00a844, #00ff88) !important; color: #fff !important; border: none !important; box-shadow: 0 0 12px #00a84455 !important; }
.btn-gen { background: linear-gradient(135deg, #7b2fff, #ff6b35) !important; color: #fff !important; border: none !important; box-shadow: 0 0 14px #7b2fff55 !important; }

/* العناوين والعداد */
.misho-title { font-size: 2.2rem; font-weight: 900; letter-spacing: 4px; text-align: center; background: linear-gradient(135deg, #00d4ff, #7b2fff, #ff6b35); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 4px; }
.misho-subtitle { font-size: 0.8rem; color: #555; letter-spacing: 2px; text-transform: uppercase; text-align: center; margin-bottom: 16px;}
.counter-wrap { display: flex; align-items: center; justify-content: space-between; margin: 10px 0 16px 0; padding: 10px 16px; background: #13131a; border-radius: 12px; border: 1px solid #1e1e2e; }
.counter-label { font-size: 0.8rem; color: #666; font-weight: bold; }
.counter-num { font-size: 1.4rem; font-weight: 900; color: #fff; }
.counter-num span { font-size: 0.8rem; color: #444; }
.counter-bar-bg { flex: 1; margin: 0 12px; height: 6px; background: #1e1e2e; border-radius: 99px; overflow: hidden; }
.counter-bar-fill { height: 100%; border-radius: 99px; transition: width 0.3s; }
.bar-1 { background: linear-gradient(90deg, #0066ff, #00d4ff); }
.bar-2 { background: linear-gradient(90deg, #00a844, #00ff88); }
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

# ── التابات ───────────────────────────────────────────────────────────────────
t1, t2 = st.columns(2)
with t1:
    if st.button(f"البطاقة الأولى ({len(c1)})", key="tab1"):
        st.session_state.tab = 1; st.rerun()
with t2:
    if st.button(f"البطاقة الثانية ({len(c2)})", key="tab2"):
        st.session_state.tab = 2; st.rerun()

# ── العداد ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="counter-wrap">
    <span class="counter-label">{'البطاقة الأولى' if tab==1 else 'البطاقة الثانية'}</span>
    <span class="counter-num">{count}<span>/{MAX}</span></span>
    <div class="counter-bar-bg"><div class="counter-bar-fill {'bar-1' if tab==1 else 'bar-2'}" style="width:{int(count/MAX*100) if MAX > 0 else 0}%"></div></div>
</div>
""", unsafe_allow_html=True)

# ── شبكة الأرقام (سريعة جداً بدون رفرش) ─────────────────────────────────────────
for r in range(9):
    cols = st.columns(10)
    for c in range(10):
        n = r * 10 + c + 1
        locked = is_full and (n not in sel)
        with cols[c]:
            if st.button(str(n), key=f"btn_{n}", disabled=locked):
                if n in sel: sel.discard(n)
                else: sel.add(n)
                st.session_state.cards = []; st.session_state.show = False
                st.rerun()

# ── أزرار التحكم ──────────────────────────────────────────────────────────────
a1, a2, a3 = st.columns(3)
with a1:
    if st.button("🗑 مسح", key="btn_clr_tab"):
        if tab == 1: st.session_state.c1 = set()
        else: st.session_state.c2 = set()
        st.session_state.cards = []; st.session_state.show = False; st.rerun()
with a2:
    if st.button("🗑 مسح الكل", key="btn_clr_all"):
        st.session_state.c1 = set(); st.session_state.c2 = set()
        st.session_state.cards = []; st.session_state.show = False; st.rerun()
with a3:
    if st.button("🎯 توليد" if can_gen else "⚠️ أكمل", key="btn_gen", disabled=not can_gen):
        shared = sorted(c1 & c2, reverse=True); vessel = sorted(c2 - c1)
        v = len(vessel); nc = v // 5
        if v % 5 >= 4: nc += 1
        if nc == 0: nc = 1
        tot = nc * 5; pool = vessel.copy(); random.shuffle(pool)
        take = pool[:min(tot, len(pool))]
        extra = shared[:tot-len(take)]; all_n = take + extra; random.shuffle(all_n)
        st.session_state.cards = [sorted(all_n[i*5:(i+1)*5]) for i in range(nc)]
        st.session_state.show = True; st.rerun()

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

# ── JAVASCRIPT (لتلوين الأزرار بسرعة وبدون تخريب الواجهة) ─────────────────────
js_code = f"""
<script>
const c1 = {json.dumps(list(c1))};
const c2 = {json.dumps(list(c2))};
const both = {json.dumps(list(c1 & c2))};
const activeTab = {tab};

function applyStyles() {{
    const btns = window.parent.document.querySelectorAll('div[data-testid="stButton"] > button');
    btns.forEach(btn => {{
        const p = btn.querySelector('p');
        const txt = p ? p.innerText.trim() : btn.innerText.trim();
        const num = parseInt(txt);

        // تنظيف الكلاسات القديمة
        btn.classList.remove("num-btn", "text-btn", "sel-1", "sel-2", "sel-both", "locked", "btn-gen", "tab-active-1", "tab-active-2");

        if (/^\\d+$/.test(txt)) {{
            btn.classList.add("num-btn");
            if (both.includes(num)) btn.classList.add("sel-both");
            else if (c1.includes(num)) btn.classList.add("sel-1");
            else if (c2.includes(num)) btn.classList.add("sel-2");

            if (btn.disabled) btn.classList.add("locked");
        }} else {{
            btn.classList.add("text-btn");
            if (txt.includes("توليد")) btn.classList.add("btn-gen");
            if (txt.includes("الأولى") && activeTab === 1) btn.classList.add("tab-active-1");
            if (txt.includes("الثانية") && activeTab === 2) btn.classList.add("tab-active-2");
        }}
    }});
}}

// التنفيذ والمراقبة
applyStyles();
const observer = new MutationObserver(applyStyles);
observer.observe(window.parent.document.body, {{ childList: true, subtree: true }});
</script>
"""
components.html(js_code, height=0, width=0)