import os
from datetime import date, datetime

import streamlit as st
from agents import Agent, Runner


# =========================================================
# BO JASIM OS — PREMIUM CLOUD EDITION
# =========================================================

st.set_page_config(
    page_title="Bo Jasim OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# SECRETS
# =========================================================

try:
    if "OPENAI_API_KEY" in st.secrets:
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
except Exception:
    pass

try:
    APP_PIN = str(st.secrets.get("APP_PIN", "2580"))
except Exception:
    APP_PIN = "2580"


# =========================================================
# SESSION STATE
# =========================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "هلا بو جسيم 👋 أنا **Bo Jasim OS**. "
                "عطِني هدفك وأنا أرتبه وياك."
            ),
        }
    ]

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "notes" not in st.session_state:
    st.session_state.notes = []

if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "quick_prompt" not in st.session_state:
    st.session_state.quick_prompt = None


# =========================================================
# PREMIUM UI
# =========================================================

st.markdown(
    """
<style>

:root {
    --bg: #06080f;
    --panel: #0c111b;
    --panel2: #111827;

    --line: rgba(255,255,255,.08);

    --text: #f8fafc;
    --muted: #95a3b8;

    --blue: #7dd3fc;
    --violet: #a78bfa;

    --green: #86efac;
    --amber: #fcd34d;
    --danger: #fb7185;
}


/* ==========================================
   BASE
========================================== */

html,
body,
[class*="css"] {
    font-family:
        Inter,
        "Segoe UI",
        Tahoma,
        Arial,
        sans-serif;
}


.stApp {

    background:

        radial-gradient(
            circle at 15% -10%,
            rgba(56,189,248,.12),
            transparent 32%
        ),

        radial-gradient(
            circle at 92% 0%,
            rgba(139,92,246,.10),
            transparent 30%
        ),

        linear-gradient(
            160deg,
            #05070d 0%,
            #09101c 48%,
            #070a12 100%
        );

    color: var(--text);
}


/* subtle grid */

.stApp:before {

    content: "";

    position: fixed;

    inset: 0;

    pointer-events: none;

    opacity: .12;

    background-image:

        linear-gradient(
            rgba(255,255,255,.025) 1px,
            transparent 1px
        ),

        linear-gradient(
            90deg,
            rgba(255,255,255,.025) 1px,
            transparent 1px
        );

    background-size: 44px 44px;

    mask-image:
        linear-gradient(
            to bottom,
            black,
            transparent 92%
        );
}


.block-container {

    max-width: 1450px;

    padding-top: 1.25rem;

    padding-bottom: 2.5rem;
}


/* ==========================================
   SIDEBAR
========================================== */

[data-testid="stSidebar"] {

    background:
        rgba(6,9,16,.84);

    border-right:
        1px solid var(--line);

    backdrop-filter:
        blur(22px);
}


.brand {

    border:
        1px solid var(--line);

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,.07),
            rgba(255,255,255,.025)
        );

    border-radius: 24px;

    padding: 18px;

    margin-bottom: 18px;

    box-shadow:
        0 18px 50px rgba(0,0,0,.20);
}


.brand-kicker {

    color: var(--blue);

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 2px;
}


.brand-title {

    font-size: 25px;

    font-weight: 900;

    letter-spacing: -.6px;

    margin-top: 4px;
}


.brand-sub {

    color: var(--muted);

    font-size: 12px;

    margin-top: 2px;
}


/* ==========================================
   HERO
========================================== */

.hero {

    position: relative;

    overflow: hidden;

    border:
        1px solid var(--line);

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,.075),
            rgba(255,255,255,.025)
        );

    border-radius: 30px;

    padding: 34px 36px;

    min-height: 230px;

    box-shadow:
        0 30px 90px rgba(0,0,0,.28);

    backdrop-filter:
        blur(22px);
}


.hero:after {

    content: "";

    position: absolute;

    width: 330px;

    height: 330px;

    right: -90px;

    top: -120px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(125,211,252,.28),
            rgba(167,139,250,.08) 58%,
            transparent 72%
        );
}


.hero-kicker {

    color: var(--blue);

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 2px;

    margin-bottom: 10px;
}


.hero-title {

    font-size:
        clamp(38px, 5vw, 66px);

    line-height: .98;

    font-weight: 950;

    letter-spacing: -2.3px;

    margin: 0;
}


.gradient-text {

    background:
        linear-gradient(
            90deg,
            #ffffff,
            #92dcff 45%,
            #c4b5fd
        );

    -webkit-background-clip: text;

    -webkit-text-fill-color:
        transparent;
}


.hero-copy {

    max-width: 760px;

    color: #b3bfd1;

    margin-top: 16px;

    font-size: 15px;

    line-height: 1.9;
}


.status-pill {

    display: inline-flex;

    align-items: center;

    gap: 8px;

    margin-top: 18px;

    border:
        1px solid rgba(134,239,172,.20);

    background:
        rgba(134,239,172,.07);

    color: #bbf7d0;

    padding:
        7px 12px;

    border-radius: 999px;

    font-size: 12px;

    font-weight: 700;
}


.dot {

    width: 8px;

    height: 8px;

    border-radius: 50%;

    background:
        var(--green);

    box-shadow:
        0 0 16px rgba(134,239,172,.9);
}


/* ==========================================
   METRICS
========================================== */

.metric-card {

    min-height: 122px;

    border:
        1px solid var(--line);

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,.065),
            rgba(255,255,255,.025)
        );

    border-radius: 22px;

    padding: 19px;

    box-shadow:
        0 14px 36px rgba(0,0,0,.14);
}


.metric-label {

    color: var(--muted);

    font-size: 12px;

    font-weight: 700;
}


.metric-value {

    margin-top: 7px;

    font-size: 33px;

    font-weight: 900;

    letter-spacing: -1px;
}


.metric-foot {

    color: #718097;

    font-size: 11px;

    margin-top: 5px;
}


/* ==========================================
   SECTIONS
========================================== */

.section-title {

    font-size: 20px;

    font-weight: 850;

    margin:
        8px 0 5px;
}


.section-sub {

    color: var(--muted);

    font-size: 13px;

    margin-bottom: 15px;
}


/* ==========================================
   CHAT
========================================== */

[data-testid="stChatMessage"] {

    border:
        1px solid rgba(255,255,255,.07);

    background:
        rgba(255,255,255,.035);

    border-radius: 20px;

    padding:
        8px 12px;

    margin-bottom: 10px;

    backdrop-filter:
        blur(14px);
}


[data-testid="stChatInput"] {

    border:
        1px solid rgba(255,255,255,.08);

    background:
        rgba(255,255,255,.05);

    border-radius: 18px;
}


/* ==========================================
   BUTTONS
========================================== */

.stButton > button {

    width: 100%;

    min-height: 42px;

    border-radius: 15px;

    border:
        1px solid rgba(255,255,255,.09);

    background:
        rgba(255,255,255,.045);

    color: #f8fafc;

    font-weight: 700;

    transition:
        all .18s ease;
}


.stButton > button:hover {

    transform:
        translateY(-1px);

    border-color:
        rgba(125,211,252,.55);

    box-shadow:
        0 12px 32px rgba(56,189,248,.08);
}


/* ==========================================
   LOGIN
========================================== */

.login-shell {

    max-width: 520px;

    margin:
        86px auto 14px;
}


.login-card {

    border:
        1px solid var(--line);

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,.07),
            rgba(255,255,255,.025)
        );

    border-radius: 28px;

    padding: 30px;

    box-shadow:
        0 26px 80px rgba(0,0,0,.28);

    backdrop-filter:
        blur(22px);
}


.login-title {

    font-size: 42px;

    font-weight: 900;

    letter-spacing: -1.2px;
}


.login-sub {

    color: var(--muted);

    margin-top: 4px;

    font-size: 13px;
}


.task-done {

    opacity: .55;

    text-decoration:
        line-through;
}


.micro {

    color: var(--muted);

    font-size: 12px;
}


/* ==========================================
   MOBILE
========================================== */

@media (max-width: 768px) {

    .block-container {

        padding-left: .8rem;

        padding-right: .8rem;
    }


    .hero {

        padding: 24px;

        min-height: unset;

        border-radius: 24px;
    }


    .hero-title {

        font-size: 40px;
    }


    .metric-card {

        min-height: 108px;
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# LOGIN
# =========================================================

if not st.session_state.authenticated:

    st.markdown(
        """
<div class="login-shell">

    <div class="login-card">

        <div class="brand-kicker">
            PRIVATE PERSONAL INTELLIGENCE
        </div>

        <div class="login-title">
            ⚡ Bo Jasim OS
        </div>

        <div class="login-sub">
            Secure Access • Premium Cloud Edition
        </div>

    </div>

</div>
""",
        unsafe_allow_html=True,
    )

    pin = st.text_input(
        "PIN",
        type="password",
        placeholder="Enter your PIN",
        label_visibility="collapsed",
    )

    if st.button(
        "فتح النظام",
        use_container_width=True,
    ):

        if pin == APP_PIN:

            st.session_state.authenticated = True

            st.rerun()

        else:

            st.error("الرمز غلط")

    st.stop()


# =========================================================
# AI AGENT
# =========================================================

agent = Agent(

    name="Bo Jasim OS",

    instructions="""
أنت Bo Jasim OS، مدير شخصي رقمي ذكي وعملي.

تكلم باللهجة الإماراتية الطبيعية
وبأسلوب واضح ومرتب.

ساعد المستخدم في:

- ترتيب يومه وأولوياته
- تحويل الأفكار إلى خطوات عملية
- مشاريع الذكاء الاصطناعي
- القرارات والمقارنات
- التخطيط الشخصي

قواعد:

- لا تدّعي أنك نفذت إجراء خارج التطبيق
  إذا ما صار فعلاً.

- لا تدّعي أنك حفظت شي
  إلا إذا النظام حفظه داخل الجلسة.

- لا تنفذ أي إجراء مالي أو حساس
  بدون موافقة واضحة.

- إذا طلب خطة،
  عطه خطوات عملية مب كلام عام.
""",
)


# =========================================================
# HELPERS
# =========================================================

def pending_tasks():

    return [

        task

        for task in st.session_state.tasks

        if not task.get("done")
    ]


def expenses_total():

    return sum(

        float(item.get("amount", 0))

        for item in st.session_state.expenses
    )


def run_agent(prompt):

    recent = st.session_state.messages[-10:]

    history = "\n".join(

        f"{'المستخدم' if message['role'] == 'user' else 'المساعد'}: "
        f"{message['content']}"

        for message in recent
    )

    full_prompt = f"""
سياق المحادثة الأخيرة:

{history}


رسالة المستخدم الجديدة:

{prompt}
"""

    result = Runner.run_sync(
        agent,
        full_prompt,
    )

    return result.final_output


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
<div class="brand">

    <div class="brand-kicker">
        PERSONAL INTELLIGENCE SYSTEM
    </div>

    <div class="brand-title">
        ⚡ Bo Jasim OS
    </div>

    <div class="brand-sub">
        Premium Edition • Cloud Ready
    </div>

</div>
""",
        unsafe_allow_html=True,
    )

    page = st.radio(

        "Navigation",

        [
            "الرئيسية",
            "المساعد",
            "المهام",
            "الملاحظات",
            "المصاريف",
        ],

        label_visibility="collapsed",
    )

    st.markdown("---")

    st.caption("SYSTEM STATUS")

    st.success("● Online")

    st.caption("OpenAI Agents SDK")

    st.caption("Streamlit Cloud")

    if st.button(
        "تسجيل خروج",
        use_container_width=True,
    ):

        st.session_state.authenticated = False

        st.rerun()


# =========================================================
# HOME
# =========================================================

if page == "الرئيسية":

    st.markdown(
        """
<div class="hero">

    <div class="hero-kicker">
        BO JASIM PERSONAL OPERATING SYSTEM
    </div>

    <h1 class="hero-title">

        Your life.

        <br>

        <span class="gradient-text">
            Under command.
        </span>

    </h1>

    <div class="hero-copy">

        مركز قيادة شخصي يجمع الذكاء الاصطناعي
        والمهام والملاحظات والمصاريف في واجهة
        واحدة نظيفة وفخمة، كأنها منتج تقني حقيقي
        مب مجرد شات.

    </div>

    <div class="status-pill">

        <span class="dot"></span>

        All systems operational

    </div>

</div>
""",
        unsafe_allow_html=True,
    )

    st.write("")

    cards = [

        (
            "مهام مفتوحة",
            len(pending_tasks()),
            "Focus queue",
        ),

        (
            "ملاحظات",
            len(st.session_state.notes),
            "Knowledge vault",
        ),

        (
            "المصاريف",
            f"{expenses_total():,.0f} د.إ",
            "Tracked total",
        ),

        (
            "رسائل AI",
            len(st.session_state.messages),
            "Session memory",
        ),
    ]

    c1, c2, c3, c4 = st.columns(4)

    columns = (
        c1,
        c2,
        c3,
        c4,
    )

    for col, card in zip(
        columns,
        cards,
    ):

        label, value, foot = card

        with col:

            st.markdown(
                f"""
<div class="metric-card">

    <div class="metric-label">
        {label}
    </div>

    <div class="metric-value">
        {value}
    </div>

    <div class="metric-foot">
        {foot}
    </div>

</div>
""",
                unsafe_allow_html=True,
            )


    st.write("")


    left, right = st.columns(
        [1.35, 1],
        gap="large",
    )


    with left:

        st.markdown(
            '<div class="section-title">'
            '⚡ Quick Command'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-sub">'
            'أوامر سريعة عشان تبدأ بدون لف ودوران.'
            '</div>',
            unsafe_allow_html=True,
        )


        q1, q2 = st.columns(2)


        with q1:

            if st.button(
                "رتب لي يومي",
                use_container_width=True,
            ):

                st.session_state.quick_prompt = (
                    "رتب لي يومي بشكل عملي "
                    "وحدد أهم 3 أولويات."
                )

                st.info(
                    "روح صفحة المساعد، الأمر جاهز لك."
                )


            if st.button(
                "حلل لي قرار",
                use_container_width=True,
            ):

                st.session_state.quick_prompt = (
                    "ساعدني أحلل قرار مهم: "
                    "الفوائد، المخاطر، وأفضل خيار."
                )

                st.info(
                    "روح صفحة المساعد، الأمر جاهز لك."
                )


        with q2:

            if st.button(
                "خطة مشروع AI",
                use_container_width=True,
            ):

                st.session_state.quick_prompt = (
                    "ابنِ لي خطة مشروع AI "
                    "قابلة للتنفيذ خطوة بخطوة."
                )

                st.info(
                    "روح صفحة المساعد، الأمر جاهز لك."
                )


            if st.button(
                "Brain Dump",
                use_container_width=True,
            ):

                st.session_state.quick_prompt = (
                    "خلنا نسوي Brain Dump، "
                    "اسألني اللي في بالي "
                    "ورتبه لي إلى مهام وأولويات."
                )

                st.info(
                    "روح صفحة المساعد، الأمر جاهز لك."
                )


    with right:

        st.markdown(
            '<div class="section-title">'
            '🎯 Focus Queue'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-sub">'
            'أقرب المهام اللي تحتاج منك حركة.'
            '</div>',
            unsafe_allow_html=True,
        )


        items = pending_tasks()[:5]


        if not items:

            st.info(
                "ما عندك مهام مفتوحة."
            )


        else:

            for task in items:

                st.markdown(
                    f"""
**{task['title']}**

`{task.get('priority', 'عادي')}`
·
{task.get('due', 'بدون تاريخ')}
"""
                )


# =========================================================
# AI ASSISTANT
# =========================================================

elif page == "المساعد":

    st.markdown(
        '<div class="section-title">'
        '🧠 Command AI'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-sub">'
        'عطه الهدف، وهو يرتب لك الطريق.'
        '</div>',
        unsafe_allow_html=True,
    )


    a, b = st.columns(2)


    with a:

        if st.button(
            "مسح المحادثة",
            use_container_width=True,
        ):

            st.session_state.messages = [

                {
                    "role": "assistant",

                    "content": (
                        "هلا بو جسيم 👋 "
                        "أنا **Bo Jasim OS**. "
                        "عطِني هدفك وأنا أرتبه وياك."
                    ),
                }
            ]

            st.rerun()


    with b:

        if st.button(
            "تلخيص المحادثة",
            use_container_width=True,
        ):

            st.session_state.quick_prompt = (
                "لخص لي أهم النقاط "
                "والقرارات من المحادثة الحالية."
            )


    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    quick = (
        st.session_state.quick_prompt
    )


    prompt = st.chat_input(
        "شو تبا تسوي؟ عطِني الهدف مباشرة..."
    )


    if quick and not prompt:

        prompt = quick

        st.session_state.quick_prompt = None


    if prompt:

        st.session_state.messages.append(

            {
                "role": "user",
                "content": prompt,
            }
        )


        with st.chat_message("user"):

            st.markdown(prompt)


        with st.chat_message("assistant"):

            with st.spinner(
                "أحلل الموضوع..."
            ):

                try:

                    answer = run_agent(
                        prompt
                    )

                except Exception as error:

                    answer = (
                        "صار خطأ في الاتصال بالـAI: "
                        f"`{error}`"
                    )


            st.markdown(answer)


        st.session_state.messages.append(

            {
                "role": "assistant",
                "content": answer,
            }
        )


# =========================================================
# TASKS
# =========================================================

elif page == "المهام":

    st.markdown(
        '<div class="section-title">'
        '✅ Mission Control'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-sub">'
        'كل مهمة عندك في مكان واحد.'
        '</div>',
        unsafe_allow_html=True,
    )


    with st.expander(
        "➕ إضافة مهمة",
        expanded=True,
    ):

        with st.form(
            "task_form",
            clear_on_submit=True,
        ):

            title = st.text_input(
                "المهمة",
                placeholder="مثال: أخلص واجب الجامعة",
            )


            c1, c2 = st.columns(2)


            with c1:

                priority = st.selectbox(

                    "الأولوية",

                    [
                        "عالي",
                        "متوسط",
                        "عادي",
                    ],
                )


            with c2:

                due = st.date_input(

                    "التاريخ",

                    value=date.today(),
                )


            if st.form_submit_button(
                "إضافة المهمة",
                use_container_width=True,
            ):

                if title.strip():

                    st.session_state.tasks.append(

                        {
                            "id":
                                datetime.now().timestamp(),

                            "title":
                                title.strip(),

                            "priority":
                                priority,

                            "due":
                                due.isoformat(),

                            "done":
                                False,
                        }
                    )

                    st.rerun()


    if not st.session_state.tasks:

        st.info(
            "ما عندك مهام للحين."
        )


    else:

        for index, task in enumerate(
            st.session_state.tasks
        ):

            c1, c2, c3 = st.columns(
                [6, 1.3, 1]
            )


            with c1:

                cls = (
                    "task-done"
                    if task["done"]
                    else ""
                )

                st.markdown(
                    f"""
<div class="{cls}">

    <b>
        {task['title']}
    </b>

    <br>

    <span class="micro">

        {task['priority']}
        ·
        {task['due']}

    </span>

</div>
""",
                    unsafe_allow_html=True,
                )


            with c2:

                if st.button(

                    (
                        "رجّع"
                        if task["done"]
                        else "تم"
                    ),

                    key=(
                        f"task_done_"
                        f"{task['id']}"
                    ),

                    use_container_width=True,
                ):

                    task["done"] = (
                        not task["done"]
                    )

                    st.rerun()


            with c3:

                if st.button(

                    "🗑",

                    key=(
                        f"task_delete_"
                        f"{task['id']}"
                    ),

                    use_container_width=True,
                ):

                    st.session_state.tasks.pop(
                        index
                    )

                    st.rerun()


            st.markdown("---")


# =========================================================
# NOTES
# =========================================================

elif page == "الملاحظات":

    st.markdown(
        '<div class="section-title">'
        '🗂 Knowledge Vault'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-sub">'
        'أفكارك وقراراتك وملاحظاتك في مكان واحد.'
        '</div>',
        unsafe_allow_html=True,
    )


    with st.form(
        "note_form",
        clear_on_submit=True,
    ):

        title = st.text_input(
            "العنوان",
            placeholder="مثال: فكرة مشروع",
        )


        body = st.text_area(
            "الملاحظة",
            placeholder="اكتب اللي في بالك...",
            height=140,
        )


        if st.form_submit_button(
            "حفظ الملاحظة",
            use_container_width=True,
        ):

            if (
                title.strip()
                or body.strip()
            ):

                st.session_state.notes.insert(

                    0,

                    {
                        "id":
                            datetime.now().timestamp(),

                        "title":
                            title.strip()
                            or "بدون عنوان",

                        "body":
                            body.strip(),

                        "created":
                            datetime.now().strftime(
                                "%Y-%m-%d %H:%M"
                            ),
                    },
                )

                st.rerun()


    if not st.session_state.notes:

        st.info(
            "الخزنة فاضية للحين."
        )


    else:

        for index, note in enumerate(
            st.session_state.notes
        ):

            with st.expander(

                f"📝 {note['title']} "
                f"· {note['created']}"
            ):

                st.write(
                    note["body"]
                )


                if st.button(

                    "حذف",

                    key=(
                        f"note_delete_"
                        f"{note['id']}"
                    ),
                ):

                    st.session_state.notes.pop(
                        index
                    )

                    st.rerun()


# =========================================================
# EXPENSES
# =========================================================

elif page == "المصاريف":

    st.markdown(
        '<div class="section-title">'
        '💳 Money Radar'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-sub">'
        'صورة سريعة وواضحة عن اللي صرفته.'
        '</div>',
        unsafe_allow_html=True,
    )


    st.metric(

        "إجمالي المسجل",

        f"{expenses_total():,.2f} د.إ",
    )


    with st.form(
        "expense_form",
        clear_on_submit=True,
    ):

        c1, c2 = st.columns(2)


        with c1:

            amount = st.number_input(

                "المبلغ",

                min_value=0.0,

                step=10.0,
            )


        with c2:

            category = st.selectbox(

                "التصنيف",

                [
                    "أكل",
                    "سيارة",
                    "جامعة",
                    "تسوق",
                    "ترفيه",
                    "فواتير",
                    "غيره",
                ],
            )


        note = st.text_input(
            "ملاحظة",
            placeholder="اختياري",
        )


        if st.form_submit_button(
            "إضافة المصروف",
            use_container_width=True,
        ):

            if amount > 0:

                st.session_state.expenses.insert(

                    0,

                    {
                        "id":
                            datetime.now().timestamp(),

                        "amount":
                            float(amount),

                        "category":
                            category,

                        "note":
                            note.strip(),

                        "created":
                            datetime.now().strftime(
                                "%Y-%m-%d %H:%M"
                            ),
                    },
                )

                st.rerun()


    if not st.session_state.expenses:

        st.info(
            "ما سجلت مصاريف للحين."
        )


    else:

        for index, expense in enumerate(
            st.session_state.expenses
        ):

            c1, c2, c3, c4 = st.columns(
                [1.5, 1.3, 4, 1]
            )


            with c1:

                st.markdown(
                    f"**{expense['amount']:,.2f} د.إ**"
                )


            with c2:

                st.write(
                    expense["category"]
                )


            with c3:

                st.caption(

                    f"{expense['note']} "
                    f"· "
                    f"{expense['created']}"
                )


            with c4:

                if st.button(

                    "🗑",

                    key=(
                        f"expense_delete_"
                        f"{expense['id']}"
                    ),

                    use_container_width=True,
                ):

                    st.session_state.expenses.pop(
                        index
                    )

                    st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.write("")

st.markdown(
    """
<div
    style="
        text-align:center;
        color:#64748b;
        font-size:11px;
        padding:24px 0 4px;
    "
>
    BO JASIM OS • PREMIUM CLOUD EDITION
</div>
""",
    unsafe_allow_html=True,
)
