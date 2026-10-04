import json
import os
from datetime import date, datetime
from pathlib import Path

import streamlit as st
from agents import Agent, Runner

# =========================================================
# BO JASIM OS — LEGENDARY EDITION
# =========================================================

APP_NAME = "Bo Jasim OS"
DATA_FILE = Path("bo_jasim_os_data.json")

st.set_page_config(
    page_title=APP_NAME,
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)
APP_PIN = "2004"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("⚡ Bo Jasim OS")
    st.caption("Private Access")

    pin = st.text_input(
        "PIN",
        type="password",
        placeholder="Enter PIN"
    )

    if st.button("فتح النظام"):
        if pin == APP_PIN:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("الرمز غلط")

    st.stop()
# -----------------------------
# Persistence
# -----------------------------
DEFAULT_DATA = {
    "messages": [
        {
            "role": "assistant",
            "content": "هلا بو جسيم 👋 أنا **Bo Jasim OS**. عطِني هدفك وأنا أرتبه وياك."
        }
    ],
    "tasks": [],
    "notes": [],
    "expenses": [],
}

def load_data():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
            for k, v in DEFAULT_DATA.items():
                saved.setdefault(k, v.copy() if isinstance(v, list) else v)
            return saved
        except Exception:
            pass
    return json.loads(json.dumps(DEFAULT_DATA, ensure_ascii=False))

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.data, f, ensure_ascii=False, indent=2)

if "data" not in st.session_state:
    st.session_state.data = load_data()

if "page" not in st.session_state:
    st.session_state.page = "الرئيسية"

# -----------------------------
# Agent
# -----------------------------
agent = Agent(
    name="Bo Jasim OS",
    instructions="""
أنت Bo Jasim OS، مدير شخصي رقمي ذكي وعملي.

تكلم باللهجة الإماراتية الطبيعية وبأسلوب واضح ومرتب.
لا تتكلف ولا تستخدم فصحى ثقيلة.

دورك:
- ترتيب اليوم والأولويات
- تحويل الأفكار إلى خطوات تنفيذ
- مساعدة المستخدم في مشاريع الذكاء الاصطناعي
- تحليل الخيارات واتخاذ قرارات عملية
- إعطاء خطط قصيرة وواضحة
- تنبيه المستخدم إذا كان في نقص معلومات أو مخاطرة

قواعد:
- لا تدّعي أنك نفذت إجراء خارج التطبيق إذا ما صار فعلاً.
- لا تدّعي أنك حفظت معلومة إلا إذا النظام فعلاً حفظها.
- أي إجراء مالي أو حساس يحتاج موافقة واضحة.
- إذا المستخدم طلب خطة، عطه خطوات تنفيذية مب كلام عام.
"""
)

# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
<style>
:root {
    --bg0: #05070d;
    --bg1: #090d17;
    --card: rgba(255,255,255,.055);
    --card2: rgba(255,255,255,.035);
    --line: rgba(255,255,255,.09);
    --text: #f6f7fb;
    --muted: #95a0b5;
    --accent: #8bd8ff;
    --accent2: #9b8cff;
    --good: #74f0b5;
}

html, body, [class*="css"] {
    font-family: Inter, "Segoe UI", Tahoma, Arial, sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(73, 130, 255, .15), transparent 28%),
        radial-gradient(circle at 88% 8%, rgba(147, 88, 255, .12), transparent 30%),
        radial-gradient(circle at 50% 100%, rgba(0, 209, 255, .08), transparent 34%),
        linear-gradient(160deg, var(--bg0) 0%, var(--bg1) 52%, #070a12 100%);
    color: var(--text);
}

.stApp:before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    opacity: .18;
    background-image:
        linear-gradient(rgba(255,255,255,.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.025) 1px, transparent 1px);
    background-size: 44px 44px;
    mask-image: linear-gradient(to bottom, black, transparent 86%);
}

.block-container {
    max-width: 1480px;
    padding-top: 1.6rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: rgba(5, 8, 15, .78);
    border-right: 1px solid var(--line);
    backdrop-filter: blur(24px);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.2rem;
}

.brand {
    border: 1px solid var(--line);
    background: linear-gradient(135deg, rgba(125,211,252,.10), rgba(139,92,246,.08));
    border-radius: 24px;
    padding: 18px 18px 16px;
    margin-bottom: 16px;
    box-shadow: 0 22px 70px rgba(0,0,0,.22);
}
.brand-kicker {
    color: var(--accent);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2.2px;
}
.brand-title {
    font-size: 25px;
    font-weight: 900;
    letter-spacing: -.5px;
    margin-top: 5px;
}
.brand-sub {
    color: var(--muted);
    font-size: 12px;
    margin-top: 3px;
}

.hero {
    position: relative;
    overflow: hidden;
    border: 1px solid var(--line);
    background:
        linear-gradient(135deg, rgba(255,255,255,.07), rgba(255,255,255,.025));
    border-radius: 30px;
    padding: 34px 36px;
    min-height: 230px;
    box-shadow: 0 30px 100px rgba(0,0,0,.30);
    backdrop-filter: blur(24px);
}
.hero:after {
    content: "";
    position: absolute;
    width: 280px;
    height: 280px;
    border-radius: 50%;
    right: -80px;
    top: -110px;
    background: radial-gradient(circle, rgba(98, 196, 255, .28), rgba(132, 81, 255, .06) 60%, transparent 72%);
    filter: blur(2px);
}
.hero-kicker {
    color: var(--accent);
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2.2px;
    margin-bottom: 10px;
}
.hero-title {
    font-size: clamp(38px, 5vw, 66px);
    line-height: .98;
    font-weight: 950;
    letter-spacing: -2.5px;
    margin: 0;
}
.gradient-text {
    background: linear-gradient(90deg, #fff, #9adfff 45%, #b6a4ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-copy {
    max-width: 720px;
    color: #aeb8ca;
    margin-top: 18px;
    font-size: 15px;
    line-height: 1.9;
}
.status-pill {
    display: inline-flex;
    gap: 8px;
    align-items: center;
    margin-top: 18px;
    border: 1px solid rgba(116,240,181,.20);
    background: rgba(116,240,181,.07);
    border-radius: 999px;
    padding: 7px 12px;
    color: #b8f9da;
    font-size: 12px;
    font-weight: 700;
}
.dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--good);
    box-shadow: 0 0 16px rgba(116,240,181,.9);
}

.glass {
    border: 1px solid var(--line);
    background: var(--card);
    border-radius: 24px;
    padding: 20px;
    backdrop-filter: blur(18px);
    box-shadow: 0 18px 60px rgba(0,0,0,.18);
}
.metric-card {
    min-height: 126px;
    border: 1px solid var(--line);
    background: linear-gradient(145deg, rgba(255,255,255,.065), rgba(255,255,255,.025));
    border-radius: 23px;
    padding: 20px;
}
.metric-label {
    color: var(--muted);
    font-size: 12px;
    font-weight: 700;
}
.metric-value {
    font-size: 34px;
    font-weight: 900;
    margin-top: 7px;
    letter-spacing: -1px;
}
.metric-foot {
    color: #78869e;
    font-size: 11px;
    margin-top: 5px;
}

.section-heading {
    font-size: 20px;
    font-weight: 850;
    margin: 7px 0 14px;
}
.section-sub {
    color: var(--muted);
    font-size: 13px;
    margin-top: -8px;
    margin-bottom: 15px;
}

[data-testid="stChatMessage"] {
    border: 1px solid rgba(255,255,255,.07);
    background: rgba(255,255,255,.035);
    border-radius: 22px;
    padding: 8px 13px;
    margin-bottom: 11px;
    backdrop-filter: blur(16px);
}
[data-testid="stChatMessageContent"] p,
[data-testid="stChatMessageContent"] li {
    line-height: 1.8;
}

[data-testid="stChatInput"] {
    border: 1px solid rgba(255,255,255,.09);
    background: rgba(255,255,255,.055);
    border-radius: 20px;
    backdrop-filter: blur(18px);
}

.stButton > button {
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,.09);
    background: rgba(255,255,255,.045);
    color: #f5f7fb;
    font-weight: 720;
    min-height: 42px;
    transition: all .18s ease;
}
.stButton > button:hover {
    border-color: rgba(139,216,255,.55);
    color: white;
    transform: translateY(-1px);
    box-shadow: 0 12px 35px rgba(59,130,246,.12);
}

div[data-testid="stMetric"] {
    border: 1px solid var(--line);
    background: var(--card2);
    border-radius: 20px;
    padding: 14px;
}

.stTextInput input, .stTextArea textarea, .stNumberInput input, .stDateInput input {
    border-radius: 14px !important;
}

hr {
    border-color: rgba(255,255,255,.07) !important;
}

.small-muted {
    color: var(--muted);
    font-size: 12px;
}

.task-done {
    opacity: .55;
    text-decoration: line-through;
}
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------
# Helpers
# -----------------------------
def money_total():
    return sum(float(x.get("amount", 0)) for x in st.session_state.data["expenses"])

def pending_tasks():
    return [x for x in st.session_state.data["tasks"] if not x.get("done")]

def ai_reply(prompt):
    recent = st.session_state.data["messages"][-10:]
    history = "\n".join(
        f"{'المستخدم' if m['role']=='user' else 'المساعد'}: {m['content']}"
        for m in recent
    )
    full_prompt = f"""
هذا سياق المحادثة الأخيرة:
{history}

رسالة المستخدم الجديدة:
{prompt}
"""
    result = Runner.run_sync(agent, full_prompt)
    return result.final_output

# -----------------------------
# Sidebar / Navigation
# -----------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-kicker">PERSONAL INTELLIGENCE</div>
            <div class="brand-title">⚡ Bo Jasim OS</div>
            <div class="brand-sub">Legendary Edition • Local Command Center</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    page = st.radio(
        "التنقل",
        ["الرئيسية", "المساعد", "المهام", "الملاحظات", "المصاريف"],
        label_visibility="collapsed",
    )
    st.session_state.page = page

    st.markdown("---")
    st.caption("SYSTEM STATUS")
    st.success("● Agent Online")
    st.caption("OpenAI Agents SDK • Streamlit")
    st.caption(f"Data: {DATA_FILE.name}")

# =========================================================
# HOME
# =========================================================
if page == "الرئيسية":
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-kicker">BO JASIM PERSONAL OPERATING SYSTEM</div>
            <h1 class="hero-title">
                Your life.<br>
                <span class="gradient-text">Under command.</span>
            </h1>
            <div class="hero-copy">
                مركز قيادة شخصي يجمع لك الذكاء الاصطناعي، المهام، الملاحظات والمصاريف
                في مكان واحد — مب مجرد شات، هذا أساس نظامك الشخصي.
            </div>
            <div class="status-pill"><span class="dot"></span> All systems operational</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    pending = len(pending_tasks())
    notes_count = len(st.session_state.data["notes"])
    expenses_total = money_total()
    msg_count = len(st.session_state.data["messages"])

    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        ("مهام مفتوحة", pending, "Focus queue"),
        ("ملاحظات", notes_count, "Knowledge vault"),
        ("المصاريف", f"{expenses_total:,.0f} د.إ", "Tracked total"),
        ("رسائل AI", msg_count, "Conversation memory"),
    ]
    for col, (label, value, foot) in zip((c1, c2, c3, c4), metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-foot">{foot}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    left, right = st.columns([1.45, 1], gap="large")

    with left:
        st.markdown('<div class="section-heading">⚡ Quick Command</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">أوامر سريعة تشغّل مخك الثاني.</div>', unsafe_allow_html=True)

        q1, q2 = st.columns(2)
        with q1:
            if st.button("رتب لي يومي", use_container_width=True):
                st.session_state.quick_prompt = "رتب لي يومي بشكل عملي وحدد أهم 3 أولويات."
                st.session_state.page = "المساعد"
                st.rerun()
            if st.button("حلل لي قرار", use_container_width=True):
                st.session_state.quick_prompt = "ساعدني أحلل قرار مهم بطريقة واضحة: المخاطر، الفوائد، وأفضل خيار."
                st.session_state.page = "المساعد"
                st.rerun()
        with q2:
            if st.button("ابنِ لي خطة مشروع AI", use_container_width=True):
                st.session_state.quick_prompt = "ابنِ لي خطة مشروع AI قابلة للتنفيذ خطوة بخطوة."
                st.session_state.page = "المساعد"
                st.rerun()
            if st.button("سو لي Brain Dump", use_container_width=True):
                st.session_state.quick_prompt = "خلنا نسوي Brain Dump، اسألني عن اللي في بالي وعقب رتبه إلى مهام وأولويات."
                st.session_state.page = "المساعد"
                st.rerun()

    with right:
        st.markdown('<div class="section-heading">🎯 Focus Queue</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">أقرب المهام اللي تنتظر منك حركة.</div>', unsafe_allow_html=True)

        tasks = pending_tasks()[:5]
        if not tasks:
            st.info("ما عندك مهام مفتوحة. الوضع هادي بشكل مشبوه 😂")
        else:
            for t in tasks:
                priority = t.get("priority", "عادي")
                due = t.get("due", "بدون تاريخ")
                st.markdown(f"**{t['title']}**  \n`{priority}` · {due}")

# =========================================================
# CHAT
# =========================================================
elif page == "المساعد":
    st.markdown('<div class="section-heading">🧠 Command AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">تكلمه بهدف، وهو يرتب لك الطريق.</div>', unsafe_allow_html=True)

    top1, top2, top3 = st.columns([1, 1, 4])
    with top1:
        if st.button("مسح الشات", use_container_width=True):
            st.session_state.data["messages"] = DEFAULT_DATA["messages"].copy()
            save_data()
            st.rerun()
    with top2:
        if st.button("تلخيص", use_container_width=True):
            st.session_state.quick_prompt = "لخص لي أهم النقاط والقرارات من المحادثة الحالية."

    for message in st.session_state.data["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    quick_prompt = st.session_state.pop("quick_prompt", None)
    prompt = quick_prompt or st.chat_input("شو تبا تسوي؟ عطِني الهدف مباشرة...")

    if prompt:
        st.session_state.data["messages"].append({"role": "user", "content": prompt})
        save_data()

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("أحلل الموضوع..."):
                try:
                    answer = ai_reply(prompt)
                except Exception as e:
                    answer = f"صار خطأ في الاتصال بالـAI: `{e}`"
            st.markdown(answer)

        st.session_state.data["messages"].append({"role": "assistant", "content": answer})
        save_data()

# =========================================================
# TASKS
# =========================================================
elif page == "المهام":
    st.markdown('<div class="section-heading">✅ Mission Control</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">كل شي لازم تسويه، بدون ما يضيع بين السوالف.</div>', unsafe_allow_html=True)

    with st.expander("➕ إضافة مهمة", expanded=True):
        with st.form("task_form", clear_on_submit=True):
            title = st.text_input("المهمة", placeholder="مثال: أخلص واجب الجامعة")
            c1, c2 = st.columns(2)
            with c1:
                priority = st.selectbox("الأولوية", ["عالي", "متوسط", "عادي"])
            with c2:
                due = st.date_input("التاريخ", value=date.today())
            submitted = st.form_submit_button("إضافة المهمة", use_container_width=True)
            if submitted and title.strip():
                st.session_state.data["tasks"].append({
                    "id": datetime.now().timestamp(),
                    "title": title.strip(),
                    "priority": priority,
                    "due": due.isoformat(),
                    "done": False,
                })
                save_data()
                st.rerun()

    tasks = st.session_state.data["tasks"]
    if not tasks:
        st.info("ما عندك مهام للحين.")
    else:
        for i, task in enumerate(tasks):
            a, b, c, d = st.columns([6, 1.2, 1.2, 1])
            with a:
                klass = "task-done" if task.get("done") else ""
                st.markdown(
                    f"<div class='{klass}'><b>{task['title']}</b><br>"
                    f"<span class='small-muted'>{task.get('priority','عادي')} · {task.get('due','')}</span></div>",
                    unsafe_allow_html=True,
                )
            with b:
                if st.button("تم" if not task.get("done") else "رجّع", key=f"done_{task['id']}", use_container_width=True):
                    task["done"] = not task.get("done")
                    save_data()
                    st.rerun()
            with c:
                st.caption("مكتملة" if task.get("done") else "مفتوحة")
            with d:
                if st.button("🗑", key=f"del_task_{task['id']}", use_container_width=True):
                    st.session_state.data["tasks"].pop(i)
                    save_data()
                    st.rerun()
            st.markdown("---")

# =========================================================
# NOTES
# =========================================================
elif page == "الملاحظات":
    st.markdown('<div class="section-heading">🗂 Knowledge Vault</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">أي فكرة، قرار، رابط أو ملاحظة — خله محفوظ هني.</div>', unsafe_allow_html=True)

    with st.form("note_form", clear_on_submit=True):
        title = st.text_input("العنوان", placeholder="مثال: فكرة مشروع")
        body = st.text_area("الملاحظة", placeholder="اكتب اللي في بالك...", height=140)
        if st.form_submit_button("حفظ الملاحظة", use_container_width=True) and (title.strip() or body.strip()):
            st.session_state.data["notes"].insert(0, {
                "id": datetime.now().timestamp(),
                "title": title.strip() or "بدون عنوان",
                "body": body.strip(),
                "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
            })
            save_data()
            st.rerun()

    if not st.session_state.data["notes"]:
        st.info("الخزنة فاضية للحين.")
    else:
        for i, note in enumerate(st.session_state.data["notes"]):
            with st.expander(f"📝 {note['title']} · {note['created']}"):
                st.write(note["body"])
                if st.button("حذف", key=f"del_note_{note['id']}"):
                    st.session_state.data["notes"].pop(i)
                    save_data()
                    st.rerun()

# =========================================================
# EXPENSES
# =========================================================
elif page == "المصاريف":
    st.markdown('<div class="section-heading">💳 Money Radar</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">سجل سريع يعطيك صورة واضحة وين تروح فلوسك.</div>', unsafe_allow_html=True)

    total = money_total()
    st.metric("إجمالي المسجل", f"{total:,.2f} د.إ")

    with st.form("expense_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            amount = st.number_input("المبلغ", min_value=0.0, step=10.0)
        with c2:
            category = st.selectbox("التصنيف", ["أكل", "سيارة", "جامعة", "تسوق", "ترفيه", "فواتير", "غيره"])
        note = st.text_input("ملاحظة", placeholder="اختياري")
        if st.form_submit_button("إضافة المصروف", use_container_width=True) and amount > 0:
            st.session_state.data["expenses"].insert(0, {
                "id": datetime.now().timestamp(),
                "amount": float(amount),
                "category": category,
                "note": note.strip(),
                "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
            })
            save_data()
            st.rerun()

    if not st.session_state.data["expenses"]:
        st.info("ما سجلت مصاريف للحين.")
    else:
        for i, exp in enumerate(st.session_state.data["expenses"]):
            a, b, c, d = st.columns([1.6, 1.4, 4, 1])
            with a:
                st.markdown(f"**{exp['amount']:,.2f} د.إ**")
            with b:
                st.write(exp["category"])
            with c:
                st.caption(f"{exp.get('note','')} · {exp['created']}")
            with d:
                if st.button("🗑", key=f"del_exp_{exp['id']}", use_container_width=True):
                    st.session_state.data["expenses"].pop(i)
                    save_data()
                    st.rerun()

# Footer
st.write("")
st.markdown(
    "<div style='text-align:center;color:#65728a;font-size:11px;padding:24px 0 4px;'>"
    "BO JASIM OS • LEGENDARY EDITION • LOCAL FIRST"
    "</div>",
    unsafe_allow_html=True,
)
