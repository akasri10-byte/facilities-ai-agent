import streamlit as st
import pandas as pd
from datetime import datetime
import random
import re

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="XDATA | Facilities AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 85% 5%, rgba(59,130,246,0.08), transparent 25%),
        linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%);
}

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}

/* Main container */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1450px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0b1220;
    border-right: 1px solid #1e293b;
}

section[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

section[data-testid="stSidebar"] .stRadio label {
    padding: 8px 10px;
    border-radius: 8px;
}

section[data-testid="stSidebar"] .stRadio label:hover {
    background: #172033;
}

/* Buttons */
.stButton > button {
    border-radius: 9px;
    border: 1px solid #d7dee8;
    font-weight: 600;
    min-height: 40px;
    transition: all 0.15s ease;
}

.stButton > button:hover {
    border-color: #3b82f6;
    color: #2563eb;
    transform: translateY(-1px);
}

/* Primary buttons */
button[kind="primary"] {
    background: #2563eb !important;
    border-color: #2563eb !important;
    color: white !important;
}

/* Header */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 4px 0 22px 0;
}

.brand-wrap {
    display: flex;
    align-items: center;
    gap: 12px;
}

.brand-mark {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    background: linear-gradient(135deg, #2563eb, #06b6d4);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 20px;
    font-weight: 800;
    box-shadow: 0 8px 24px rgba(37,99,235,0.25);
}

.brand-title {
    font-size: 20px;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.4px;
}

.brand-subtitle {
    font-size: 11px;
    color: #64748b;
    margin-top: 2px;
}

.live-pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 7px 11px;
    border-radius: 999px;
    background: #ecfdf5;
    border: 1px solid #bbf7d0;
    color: #15803d;
    font-size: 11px;
    font-weight: 700;
}

.live-dot {
    width: 7px;
    height: 7px;
    background: #22c55e;
    border-radius: 50%;
}

/* Hero */
.hero {
    background: linear-gradient(135deg, #0f172a 0%, #172554 60%, #164e63 100%);
    border-radius: 18px;
    padding: 26px 28px;
    color: white;
    margin-bottom: 22px;
    box-shadow: 0 15px 40px rgba(15,23,42,0.14);
    position: relative;
    overflow: hidden;
}

.hero:after {
    content: "";
    position: absolute;
    width: 240px;
    height: 240px;
    border-radius: 50%;
    right: -70px;
    top: -90px;
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow:
        0 0 0 30px rgba(255,255,255,0.025),
        0 0 0 60px rgba(255,255,255,0.018);
}

.hero-title {
    font-size: 27px;
    font-weight: 800;
    letter-spacing: -0.8px;
    margin-bottom: 7px;
}

.hero-text {
    color: #cbd5e1;
    font-size: 13px;
    max-width: 700px;
    line-height: 1.6;
}

.hero-chip {
    display: inline-block;
    margin-top: 14px;
    padding: 6px 10px;
    border-radius: 7px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.10);
    color: #dbeafe;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.3px;
}

/* KPI cards */
.kpi {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 17px;
    min-height: 108px;
    box-shadow: 0 5px 20px rgba(15,23,42,0.04);
}

.kpi-label {
    color: #64748b;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.kpi-value {
    color: #0f172a;
    font-size: 27px;
    font-weight: 800;
    margin-top: 7px;
}

.kpi-meta {
    color: #16a34a;
    font-size: 10px;
    font-weight: 600;
    margin-top: 5px;
}

/* Cards */
.card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 19px;
    box-shadow: 0 5px 20px rgba(15,23,42,0.035);
    margin-bottom: 14px;
}

.card-title {
    font-size: 14px;
    color: #0f172a;
    font-weight: 750;
    margin-bottom: 3px;
}

.card-subtitle {
    font-size: 10px;
    color: #64748b;
    margin-bottom: 15px;
}

/* Request cards */
.request-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 13px;
    padding: 16px;
    margin-bottom: 10px;
    box-shadow: 0 3px 14px rgba(15,23,42,0.03);
}

.request-id {
    color: #2563eb;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.3px;
}

.request-text {
    color: #0f172a;
    font-size: 13px;
    font-weight: 600;
    margin-top: 7px;
    line-height: 1.45;
}

.request-meta {
    color: #64748b;
    font-size: 10px;
    margin-top: 8px;
}

/* Status badges */
.badge {
    display: inline-flex;
    align-items: center;
    padding: 5px 8px;
    border-radius: 6px;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 0.35px;
    white-space: nowrap;
}

.badge-review {
    background: #fff7ed;
    color: #c2410c;
    border: 1px solid #fed7aa;
}

.badge-auto {
    background: #eff6ff;
    color: #1d4ed8;
    border: 1px solid #bfdbfe;
}

.badge-closed {
    background: #f1f5f9;
    color: #475569;
    border: 1px solid #cbd5e1;
}

.badge-safety {
    background: #fef2f2;
    color: #b91c1c;
    border: 1px solid #fecaca;
}

.badge-vendor {
    background: #f0fdf4;
    color: #15803d;
    border: 1px solid #bbf7d0;
}

.badge-pending {
    background: #fefce8;
    color: #a16207;
    border: 1px solid #fde68a;
}

/* Category pill */
.category {
    display: inline-block;
    padding: 4px 7px;
    background: #f1f5f9;
    color: #475569;
    border-radius: 5px;
    font-size: 9px;
    font-weight: 700;
    margin-right: 5px;
}

/* Timeline */
.timeline {
    position: relative;
    padding-left: 22px;
}

.timeline:before {
    content: "";
    position: absolute;
    left: 6px;
    top: 5px;
    bottom: 5px;
    width: 2px;
    background: #dbeafe;
}

.timeline-item {
    position: relative;
    margin-bottom: 17px;
}

.timeline-dot {
    position: absolute;
    left: -21px;
    top: 2px;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #2563eb;
    border: 3px solid #dbeafe;
}

.timeline-name {
    font-size: 11px;
    font-weight: 800;
    color: #0f172a;
}

.timeline-detail {
    font-size: 10px;
    color: #64748b;
    margin-top: 3px;
}

/* Tool trace */
.tool {
    display: flex;
    gap: 11px;
    padding: 12px 0;
    border-bottom: 1px solid #f1f5f9;
}

.tool:last-child {
    border-bottom: none;
}

.tool-icon {
    width: 29px;
    height: 29px;
    border-radius: 8px;
    background: #eff6ff;
    color: #2563eb;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 800;
    flex-shrink: 0;
}

.tool-name {
    color: #0f172a;
    font-size: 11px;
    font-weight: 750;
}

.tool-result {
    color: #64748b;
    font-size: 10px;
    margin-top: 3px;
}

/* Architecture */
.arch-box {
    border: 1px solid #dbe4ef;
    border-radius: 12px;
    padding: 13px;
    background: white;
    text-align: center;
    min-height: 82px;
}

.arch-icon {
    font-size: 18px;
    margin-bottom: 6px;
}

.arch-title {
    font-size: 10px;
    font-weight: 800;
    color: #0f172a;
}

.arch-desc {
    font-size: 8px;
    color: #64748b;
    margin-top: 3px;
}

.arch-arrow {
    display: flex;
    align-items: center;
    justify-content: center;
    color: #94a3b8;
    font-size: 18px;
}

/* Decision panel */
.decision {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 13px;
}

.decision-label {
    font-size: 9px;
    color: #64748b;
    text-transform: uppercase;
    font-weight: 700;
    letter-spacing: .5px;
}

.decision-value {
    font-size: 13px;
    font-weight: 800;
    color: #0f172a;
    margin-top: 3px;
}

/* Progress */
.progress-track {
    height: 6px;
    background: #e2e8f0;
    border-radius: 10px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg,#2563eb,#06b6d4);
    border-radius: 10px;
}

/* Small table */
.data-table {
    width: 100%;
    border-collapse: collapse;
}

.data-table th {
    text-align: left;
    color: #64748b;
    font-size: 9px;
    text-transform: uppercase;
    letter-spacing: .5px;
    padding: 9px;
    border-bottom: 1px solid #e2e8f0;
}

.data-table td {
    color: #334155;
    font-size: 10px;
    padding: 11px 9px;
    border-bottom: 1px solid #f1f5f9;
}

/* Mobile */
@media (max-width: 768px) {

    .block-container {
        padding-left: 0.8rem;
        padding-right: 0.8rem;
        padding-top: 1rem;
    }

    .hero {
        padding: 20px;
        border-radius: 14px;
    }

    .hero-title {
        font-size: 22px;
    }

    .topbar {
        padding-bottom: 15px;
    }

    .brand-title {
        font-size: 17px;
    }

    .kpi {
        min-height: 95px;
        padding: 13px;
    }

    .kpi-value {
        font-size: 22px;
    }

    .card {
        padding: 14px;
    }

    .arch-arrow {
        transform: rotate(90deg);
        height: 20px;
    }
}

</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# DEMO DATA
# ============================================================

DEMO_REQUESTS = [
    {
        "id": "REQ-1042",
        "text": "There are sparks coming from the socket near the pantry.",
        "category": "Electrical",
        "confidence": 0.96,
        "status": "HUMAN REVIEW",
        "urgency": "Immediate",
        "safety": True,
        "location": "Pantry",
        "created": "2 min ago",
    },
    {
        "id": "REQ-1039",
        "text": "The AC in meeting room 4B is running but not cooling.",
        "category": "HVAC",
        "confidence": 0.91,
        "status": "AUTO ROUTED",
        "urgency": "Normal",
        "safety": False,
        "location": "Meeting Room 4B",
        "created": "8 min ago",
    },
    {
        "id": "REQ-1035",
        "text": "Water is leaking below the pantry sink.",
        "category": "Plumbing",
        "confidence": 0.94,
        "status": "CLOSED DUPLICATE",
        "urgency": "Normal",
        "safety": False,
        "location": "Pantry",
        "created": "13 min ago",
    },
    {
        "id": "REQ-1045",
        "text": "Something seems wrong with the air and ventilation here.",
        "category": "HVAC",
        "confidence": 0.64,
        "status": "HUMAN REVIEW",
        "urgency": "Normal",
        "safety": False,
        "location": "Open Office",
        "created": "17 min ago",
    },
    {
        "id": "REQ-1047",
        "text": "The washroom tap is continuously dripping.",
        "category": "Plumbing",
        "confidence": 0.95,
        "status": "AUTO ROUTED",
        "urgency": "Normal",
        "safety": False,
        "location": "Washroom",
        "created": "21 min ago",
    },
    {
        "id": "REQ-1048",
        "text": "The lights in the corridor are not working.",
        "category": "Electrical",
        "confidence": 0.97,
        "status": "AUTO ROUTED",
        "urgency": "Normal",
        "safety": False,
        "location": "Corridor",
        "created": "25 min ago",
    },
    {
        "id": "REQ-1049",
        "text": "Please clean the pantry area. There is food waste around the tables.",
        "category": "Cleaning/Custodial",
        "confidence": 0.98,
        "status": "AUTO ROUTED",
        "urgency": "Normal",
        "safety": False,
        "location": "Pantry",
        "created": "29 min ago",
    },
    {
        "id": "REQ-1050",
        "text": "A person without an employee badge is waiting near the restricted server room.",
        "category": "Security",
        "confidence": 0.98,
        "status": "HUMAN REVIEW",
        "urgency": "Immediate",
        "safety": True,
        "location": "Server Room",
        "created": "34 min ago",
    },
    {
        "id": "REQ-1051",
        "text": "The AC is making a strange noise and temperature is increasing.",
        "category": "HVAC",
        "confidence": 0.89,
        "status": "AUTO ROUTED",
        "urgency": "High",
        "safety": False,
        "location": "Open Office",
        "created": "41 min ago",
    },
    {
        "id": "REQ-1052",
        "text": "The restroom floor is wet and there may be a leak.",
        "category": "Plumbing",
        "confidence": 0.88,
        "status": "AUTO ROUTED",
        "urgency": "High",
        "safety": True,
        "location": "Restroom",
        "created": "48 min ago",
    },
]

VENDOR_CONTRACTS = [
    {
        "category": "HVAC",
        "vendor": "CoolAir Services",
        "coverage": "Covered",
        "cost": 280,
        "contract": "CON-HVAC-001",
    },
    {
        "category": "Electrical",
        "vendor": "PowerFix Solutions",
        "coverage": "Covered",
        "cost": 350,
        "contract": "CON-ELEC-001",
    },
    {
        "category": "Plumbing",
        "vendor": "AquaCare Facilities",
        "coverage": "Covered",
        "cost": 220,
        "contract": "CON-PLUMB-001",
    },
    {
        "category": "Cleaning/Custodial",
        "vendor": "CleanPro",
        "coverage": "Covered",
        "cost": 150,
        "contract": "CON-CLEAN-001",
    },
]

# ============================================================
# SESSION STATE
# ============================================================

if "requests" not in st.session_state:
    st.session_state.requests = DEMO_REQUESTS.copy()

if "selected_request" not in st.session_state:
    st.session_state.selected_request = "REQ-1039"

if "agent_runs" not in st.session_state:
    st.session_state.agent_runs = []

if "vendor_orders" not in st.session_state:
    st.session_state.vendor_orders = []

if "overrides" not in st.session_state:
    st.session_state.overrides = []

# ============================================================
# HELPERS
# ============================================================

def status_badge(status):
    if status == "HUMAN REVIEW":
        cls = "badge-review"
    elif status == "AUTO ROUTED":
        cls = "badge-auto"
    elif status == "CLOSED DUPLICATE":
        cls = "badge-closed"
    elif status == "VENDOR DISPATCHED":
        cls = "badge-vendor"
    else:
        cls = "badge-pending"

    return f'<span class="badge {cls}">{status}</span>'


def category_from_text(text):
    t = text.lower()

    if any(x in t for x in ["spark", "socket", "light", "electric", "power", "switch", "bulb"]):
        return "Electrical", 0.96

    if any(x in t for x in ["water", "leak", "tap", "sink", "drip", "pipe", "flood"]):
        return "Plumbing", 0.94

    if any(x in t for x in ["ac", "air", "cool", "cooling", "ventilation", "temperature", "hvac"]):
        return "HVAC", 0.91

    if any(x in t for x in ["clean", "waste", "dirty", "spill", "garbage", "pantry area"]):
        return "Cleaning/Custodial", 0.95

    if any(x in t for x in ["badge", "security", "unauthorized", "person without", "server room"]):
        return "Security", 0.97

    return "HVAC", 0.61


def run_agent(request_text):

    category, confidence = category_from_text(request_text)

    safety_terms = [
        "spark",
        "smoke",
        "fire",
        "unauthorized",
        "without badge",
        "server room",
        "flood",
        "wet floor",
    ]

    safety = any(x in request_text.lower() for x in safety_terms)

    urgency = "Immediate" if safety else "Normal"

    # Simulated history tool
    duplicate = False

    for r in st.session_state.requests:
        if r["text"].lower() == request_text.lower():
            duplicate = True
            break

    if "leak" in request_text.lower() and category == "Plumbing":
        duplicate = random.choice([True, False])

    if duplicate:
        decision = "CLOSED DUPLICATE"
        route = "No new routing required"
        vendor = "Not dispatched"
    elif safety or confidence < 0.70:
        decision = "HUMAN REVIEW"
        route = {
            "Electrical": "Electrical Team",
            "Plumbing": "Plumbing Team",
            "HVAC": "HVAC Team",
            "Cleaning/Custodial": "Custodial Team",
            "Security": "Security Team",
        }.get(category, "Facilities Team")
        vendor = "Pending human approval"
    else:
        decision = "AUTO ROUTED"
        route = {
            "Electrical": "Electrical Team",
            "Plumbing": "Plumbing Team",
            "HVAC": "HVAC Team",
            "Cleaning/Custodial": "Custodial Team",
            "Security": "Security Team",
        }.get(category, "Facilities Team")
        vendor = "Contract check required"

    # Vendor contract simulation
    contract = next(
        (c for c in VENDOR_CONTRACTS if c["category"] == category),
        None,
    )

    work_order = None

    if (
        decision == "AUTO ROUTED"
        and category in ["Electrical", "Plumbing", "HVAC"]
        and contract
        and contract["coverage"] == "Covered"
        and contract["cost"] <= 500
    ):
        work_order = f"WO-{random.randint(1000,9999)}"

        st.session_state.vendor_orders.append(
            {
                "work_order": work_order,
                "category": category,
                "vendor": contract["vendor"],
                "cost": contract["cost"],
                "contract": contract["contract"],
                "status": "DISPATCHED",
                "created": datetime.now().strftime("%H:%M:%S"),
            }
        )

        decision = "VENDOR DISPATCHED"

    rationale = (
        f"Classified as {category} with {confidence:.0%} confidence. "
        f"History/context checks were evaluated. "
        f"{'Safety signal detected, so human attention is required.' if safety else 'No immediate safety signal detected.'}"
    )

    return {
        "category": category,
        "confidence": confidence,
        "safety": safety,
        "urgency": urgency,
        "decision": decision,
        "route": route,
        "vendor": vendor,
        "contract": contract,
        "work_order": work_order,
        "rationale": rationale,
    }


def create_request(text):

    category, confidence = category_from_text(text)

    new_id = f"REQ-{1055 + len(st.session_state.requests)}"

    result = run_agent(text)

    new_request = {
        "id": new_id,
        "text": text,
        "category": result["category"],
        "confidence": result["confidence"],
        "status": result["decision"],
        "urgency": result["urgency"],
        "safety": result["safety"],
        "location": "New Request",
        "created": "just now",
    }

    st.session_state.requests.insert(0, new_request)
    st.session_state.selected_request = new_id

    st.session_state.agent_runs.insert(
        0,
        {
            "request_id": new_id,
            "result": result,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
        },
    )

    return new_request


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="padding:10px 4px 20px 4px;">
            <div style="font-size:22px;font-weight:800;color:white;">
                XDATA
            </div>
            <div style="font-size:10px;color:#94a3b8;margin-top:3px;">
                FACILITIES AI PLATFORM
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    page = st.radio(
        "NAVIGATION",
        [
            "Command Center",
            "Request Queue",
            "Agent Execution",
            "Vendor Operations",
            "Human Review & Audit",
            "Architecture",
        ],
        label_visibility="visible",
    )

    st.markdown("---")

    st.markdown(
        """
        <div style="
            padding:12px;
            border:1px solid #253149;
            border-radius:10px;
            background:#111a2b;
        ">
            <div style="font-size:9px;color:#64748b;font-weight:700;">
                AGENT STATUS
            </div>
            <div style="font-size:12px;color:#e2e8f0;font-weight:700;margin-top:5px;">
                ● Operational
            </div>
            <div style="font-size:9px;color:#64748b;margin-top:7px;">
                Decision engine · Online
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="
            margin-top:12px;
            padding:12px;
            border:1px solid #253149;
            border-radius:10px;
            background:#111a2b;
        ">
            <div style="font-size:9px;color:#64748b;font-weight:700;">
                LLM MODE
            </div>
            <div style="font-size:12px;color:#e2e8f0;font-weight:700;margin-top:5px;">
                DEMO / FAKE LLM
            </div>
            <div style="font-size:9px;color:#64748b;margin-top:7px;">
                Deterministic local inference
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# TOP BAR
# ============================================================

st.markdown(
    """
<div class="topbar">
    <div class="brand-wrap">
        <div class="brand-mark">✦</div>
        <div>
            <div class="brand-title">Facilities AI Command Center</div>
            <div class="brand-subtitle">
                Autonomous issue intake · classification · routing · vendor operations
            </div>
        </div>
    </div>
    <div class="live-pill">
        <span class="live-dot"></span>
        SYSTEM ONLINE
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# COMMAND CENTER
# ============================================================

if page == "Command Center":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">Facilities operations, powered by AI.</div>
            <div class="hero-text">
                The agent continuously evaluates employee requests, classifies the issue,
                checks history and context, determines urgency, routes the request and
                can autonomously dispatch covered vendor work.
            </div>
            <div class="hero-chip">
                AGENTIC WORKFLOW · HUMAN-IN-THE-LOOP · AUDITABLE
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    total = len(st.session_state.requests)
    reviews = sum(
        1 for r in st.session_state.requests
        if r["status"] == "HUMAN REVIEW"
    )
    duplicates = sum(
        1 for r in st.session_state.requests
        if r["status"] == "CLOSED DUPLICATE"
    )
    vendor_count = len(st.session_state.vendor_orders)

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(
            f"""
            <div class="kpi">
                <div class="kpi-label">Requests processed</div>
                <div class="kpi-value">{total}</div>
                <div class="kpi-meta">↑ Continuous intake</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k2:
        st.markdown(
            f"""
            <div class="kpi">
                <div class="kpi-label">Human attention</div>
                <div class="kpi-value">{reviews}</div>
                <div class="kpi-meta">Safety / uncertainty</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k3:
        st.markdown(
            f"""
            <div class="kpi">
                <div class="kpi-label">Duplicate closures</div>
                <div class="kpi-value">{duplicates}</div>
                <div class="kpi-meta">Autonomous resolution</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k4:
        st.markdown(
            f"""
            <div class="kpi">
                <div class="kpi-label">Vendor orders</div>
                <div class="kpi-value">{vendor_count}</div>
                <div class="kpi-meta">Contract validated</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    left, right = st.columns([1.35, 0.9])

    # --------------------------------------------------------
    # Active requests
    # --------------------------------------------------------

    with left:

        st.markdown(
            """
            <div class="card">
                <div class="card-title">Active Requests</div>
                <div class="card-subtitle">
                    Latest employee-submitted facilities issues
                </div>
            """,
            unsafe_allow_html=True,
        )

        for r in st.session_state.requests[:6]:

            safety_badge = (
                '<span class="badge badge-safety">SAFETY SIGNAL</span>'
                if r["safety"]
                else ""
            )

            st.markdown(
                f"""
                <div class="request-card">
                    <div style="display:flex;justify-content:space-between;gap:8px;">
                        <div>
                            <span class="request-id">{r["id"]}</span>
                            <span class="category">{r["category"]}</span>
                        </div>
                        <div>
                            {status_badge(r["status"])}
                        </div>
                    </div>

                    <div class="request-text">{r["text"]}</div>

                    <div class="request-meta">
                        {r["location"]} · {r["created"]}
                        &nbsp;&nbsp; {safety_badge}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # Agent activity
    # --------------------------------------------------------

    with right:

        st.markdown(
            """
            <div class="card">
                <div class="card-title">Agent Activity</div>
                <div class="card-subtitle">
                    Latest autonomous decisions
                </div>
            """,
            unsafe_allow_html=True,
        )

        activity = [
            ("Classification", "HVAC · 91% confidence"),
            ("History check", "No matching duplicate"),
            ("Context check", "Location + issue context"),
            ("Contract check", "Coverage confirmed"),
            ("Vendor dispatch", "Work order created"),
        ]

        st.markdown('<div class="timeline">', unsafe_allow_html=True)

        for name, detail in activity:

            st.markdown(
                f"""
                <div class="timeline-item">
                    <div class="timeline-dot"></div>
                    <div class="timeline-name">{name}</div>
                    <div class="timeline-detail">{detail}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("</div></div>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # Simulate request
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="card">
            <div class="card-title">Simulate New Employee Request</div>
            <div class="card-subtitle">
                Test the complete agentic workflow without external data sources.
            </div>
        """,
        unsafe_allow_html=True,
    )

    new_text = st.text_input(
        "Request",
        placeholder="Example: The AC in room 5A is not cooling...",
        label_visibility="collapsed",
    )

    if st.button("Run Agent", type="primary", use_container_width=True):

        if new_text.strip():

            create_request(new_text)

            st.success("Request processed by the agent.")

            st.rerun()

        else:
            st.warning("Enter a request first.")

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# REQUEST QUEUE
# ============================================================

elif page == "Request Queue":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">Request Queue</div>
            <div class="hero-text">
                Every request passes through classification, history/context checks,
                decisioning and routing.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    search = st.text_input(
        "Search",
        placeholder="Search request ID, issue or category...",
        label_visibility="collapsed",
    )

    filtered = st.session_state.requests

    if search:
        s = search.lower()
        filtered = [
            r for r in filtered
            if s in r["id"].lower()
            or s in r["text"].lower()
            or s in r["category"].lower()
        ]

    for r in filtered:

        c1, c2, c3 = st.columns([1.5, 4, 1.5])

        with c1:
            st.markdown(
                f"""
                <div style="padding:12px 0;">
                    <div class="request-id">{r["id"]}</div>
                    <div style="margin-top:7px;">
                        {status_badge(r["status"])}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c2:

            st.markdown(
                f"""
                <div style="padding:12px 0;">
                    <div class="request-text">{r["text"]}</div>
                    <div class="request-meta">
                        {r["location"]} · {r["created"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c3:

            st.markdown(
                f"""
                <div style="padding:12px 0;">
                    <div class="decision-label">Classification</div>
                    <div class="decision-value">{r["category"]}</div>
                    <div class="request-meta">{r["confidence"]:.0%} confidence</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            "<hr style='border:none;border-top:1px solid #e2e8f0;'>",
            unsafe_allow_html=True,
        )

# ============================================================
# AGENT EXECUTION
# ============================================================

elif page == "Agent Execution":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">Agent Execution</div>
            <div class="hero-text">
                Transparent execution trace showing how the agent reaches an operational
                decision without exposing private chain-of-thought.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    request_ids = [r["id"] for r in st.session_state.requests]

    selected = st.selectbox(
        "Select request",
        request_ids,
        index=request_ids.index(st.session_state.selected_request)
        if st.session_state.selected_request in request_ids
        else 0,
    )

    request = next(r for r in st.session_state.requests if r["id"] == selected)

    left, right = st.columns([1, 1])

    with left:

        st.markdown(
            """
            <div class="card">
                <div class="card-title">Request</div>
                <div class="card-subtitle">
                    Incoming employee issue
                </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="request-id">{request["id"]}</div>

            <div style="
                font-size:17px;
                line-height:1.5;
                font-weight:700;
                color:#0f172a;
                margin-top:12px;
            ">
                {request["text"]}
            </div>

            <div style="margin-top:15px;">
                {status_badge(request["status"])}
            </div>

            <div style="margin-top:18px;">
                <div class="decision">
                    <div class="decision-label">Category</div>
                    <div class="decision-value">{request["category"]}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div style="margin-top:12px;">
                <div class="decision-label">Confidence</div>
                <div style="font-size:20px;font-weight:800;margin-top:4px;">
                    {request["confidence"]:.0%}
                </div>
                <div class="progress-track" style="margin-top:7px;">
                    <div class="progress-fill"
                         style="width:{request["confidence"]*100}%;">
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with right:

        st.markdown(
            """
            <div class="card">
                <div class="card-title">Tool Trace</div>
                <div class="card-subtitle">
                    Operational tools invoked by the agent
                </div>
            """,
            unsafe_allow_html=True,
        )

        tools = [
            ("01", "Fake LLM", f'{request["category"]} · {request["confidence"]:.0%}'),
            ("02", "History Tool", "Duplicate history evaluated"),
        ]

        if request["confidence"] < 0.70:
            tools.append(
                ("03", "Context Tool", "Additional context requested")
            )

        tools.extend(
            [
                ("04", "Routing Tool", f'{request["category"]} Team'),
                ("05", "Contract Tool", "Vendor coverage evaluated"),
            ]
        )

        if request["status"] == "VENDOR DISPATCHED":
            tools.append(
                ("06", "Vendor Dispatch", "Work order created")
            )

        for number, name, result in tools:

            st.markdown(
                f"""
                <div class="tool">
                    <div class="tool-icon">{number}</div>
                    <div>
                        <div class="tool-name">{name}</div>
                        <div class="tool-result">{result}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="card">
            <div class="card-title">Decision Rationale</div>
            <div class="card-subtitle">
                Concise operational explanation for human review
            </div>

            <div class="decision">
                The agent classified the request using the issue description,
                evaluated duplicate history and contextual signals, then selected
                the appropriate operational path.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# VENDOR OPERATIONS
# ============================================================

elif page == "Vendor Operations":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">Vendor Operations</div>
            <div class="hero-text">
                Contract-aware automation ensures vendor work is dispatched only
                when coverage and cost conditions are satisfied.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="card">
            <div class="card-title">Active Vendor Work Orders</div>
            <div class="card-subtitle">
                Autonomous dispatch activity
            </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.vendor_orders:

        rows = ""

        for order in st.session_state.vendor_orders:

            rows += f"""
            <tr>
                <td>{order["work_order"]}</td>
                <td>{order["category"]}</td>
                <td>{order["vendor"]}</td>
                <td>₹{order["cost"]}</td>
                <td>{order["contract"]}</td>
                <td>
                    <span class="badge badge-vendor">
                        {order["status"]}
                    </span>
                </td>
            </tr>
            """

        st.markdown(
            f"""
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Work Order</th>
                        <th>Category</th>
                        <th>Vendor</th>
                        <th>Cost</th>
                        <th>Contract</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            """
            <div style="
                padding:30px;
                text-align:center;
                color:#64748b;
                font-size:11px;
            ">
                No vendor work orders have been created yet.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="card">
            <div class="card-title">Service Contracts</div>
            <div class="card-subtitle">
                Coverage available to the agent
            </div>
        """,
        unsafe_allow_html=True,
    )

    rows = ""

    for c in VENDOR_CONTRACTS:

        rows += f"""
        <tr>
            <td>{c["category"]}</td>
            <td>{c["vendor"]}</td>
            <td>
                <span class="badge badge-vendor">
                    {c["coverage"]}
                </span>
            </td>
            <td>₹{c["cost"]}</td>
            <td>{c["contract"]}</td>
        </tr>
        """

    st.markdown(
        f"""
        <table class="data-table">
            <thead>
                <tr>
                    <th>Category</th>
                    <th>Vendor</th>
                    <th>Coverage</th>
                    <th>Estimated Cost</th>
                    <th>Contract</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# HUMAN REVIEW
# ============================================================

elif page == "Human Review & Audit":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">Human Review & Audit</div>
            <div class="hero-text">
                Humans remain in control for safety signals, low-confidence decisions,
                vendor actions and exceptional cases.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    review_items = [
        r for r in st.session_state.requests
        if r["status"] == "HUMAN REVIEW"
    ]

    if not review_items:

        st.markdown(
            """
            <div class="card" style="text-align:center;padding:40px;">
                <div style="font-size:28px;">✓</div>
                <div class="card-title" style="margin-top:10px;">
                    No requests awaiting review
                </div>
                <div class="card-subtitle">
                    The agent has no outstanding human-review actions.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    for r in review_items:

        st.markdown(
            f"""
            <div class="card">
                <div style="display:flex;justify-content:space-between;">
                    <div>
                        <div class="request-id">{r["id"]}</div>
                        <div class="request-text">{r["text"]}</div>
                    </div>
                    <div>
                        {status_badge(r["status"])}
                    </div>
                </div>

                <div style="margin-top:17px;">
                    <div class="decision">
                        <div class="decision-label">Agent classification</div>
                        <div class="decision-value">{r["category"]}</div>
                    </div>
                </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                f"""
                <div class="decision">
                    <div class="decision-label">Confidence</div>
                    <div class="decision-value">{r["confidence"]:.0%}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                f"""
                <div class="decision">
                    <div class="decision-label">Urgency</div>
                    <div class="decision-value">{r["urgency"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                f"""
                <div class="decision">
                    <div class="decision-label">Safety signal</div>
                    <div class="decision-value">
                        {"Detected" if r["safety"] else "None"}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.write("")

        override = st.selectbox(
            "Human decision",
            [
                "Keep agent decision",
                "Override → Electrical",
                "Override → Plumbing",
                "Override → HVAC",
                "Override → Cleaning/Custodial",
                "Override → Security",
            ],
            key=f"override_{r['id']}",
        )

        if st.button(
            "Apply Decision",
            key=f"apply_{r['id']}",
            type="primary",
        ):

            if override == "Keep agent decision":

                r["status"] = "AUTO ROUTED"

                action = "Kept agent decision"

            else:

                new_category = override.replace("Override → ", "")

                r["category"] = new_category
                r["status"] = "AUTO ROUTED"

                action = f"Overridden category to {new_category}"

            st.session_state.overrides.append(
                {
                    "request_id": r["id"],
                    "action": action,
                    "time": datetime.now().strftime("%H:%M:%S"),
                }
            )

            st.success("Decision applied.")

            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # Audit
    st.markdown(
        """
        <div class="card">
            <div class="card-title">Audit Trail</div>
            <div class="card-subtitle">
                Human intervention history
            </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.overrides:

        rows = ""

        for o in st.session_state.overrides:

            rows += f"""
            <tr>
                <td>{o["request_id"]}</td>
                <td>{o["action"]}</td>
                <td>{o["time"]}</td>
            </tr>
            """

        st.markdown(
            f"""
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Request</th>
                        <th>Action</th>
                        <th>Time</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            """
            <div style="
                padding:22px;
                text-align:center;
                color:#64748b;
                font-size:10px;
            ">
                No human overrides recorded.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# ARCHITECTURE
# ============================================================

elif page == "Architecture":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">Agent Architecture</div>
            <div class="hero-text">
                A tool-driven workflow that separates classification, context,
                operational decisions and human governance.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="card">
            <div class="card-title">End-to-End Agent Flow</div>
            <div class="card-subtitle">
                From employee request to autonomous resolution
            </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(9)

    architecture = [
        ("✉", "Request", "Employee issue"),
        ("✦", "LLM", "Classification"),
        ("◉", "History", "Duplicate check"),
        ("◎", "Context", "Uncertainty"),
        ("◆", "Decision", "Action"),
        ("↗", "Route", "Team"),
        ("▣", "Contract", "Coverage"),
        ("⚙", "Vendor", "Work order"),
        ("✓", "Human", "Governance"),
    ]

    for i, (icon, title, desc) in enumerate(architecture):

        with cols[i]:

            st.markdown(
                f"""
                <div class="arch-box">
                    <div class="arch-icon">{icon}</div>
                    <div class="arch-title">{title}</div>
                    <div class="arch-desc">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:

        st.markdown(
            """
            <div class="card">
                <div class="card-title">Agent Tools</div>
                <div class="card-subtitle">
                    Deterministic operational interfaces
                </div>

                <div class="tool">
                    <div class="tool-icon">01</div>
                    <div>
                        <div class="tool-name">History Tool</div>
                        <div class="tool-result">
                            Finds related or duplicate requests
                        </div>
                    </div>
                </div>

                <div class="tool">
                    <div class="tool-icon">02</div>
                    <div>
                        <div class="tool-name">Context Tool</div>
                        <div class="tool-result">
                            Retrieves additional issue context
                        </div>
                    </div>
                </div>

                <div class="tool">
                    <div class="tool-icon">03</div>
                    <div>
                        <div class="tool-name">Routing Tool</div>
                        <div class="tool-result">
                            Assigns the responsible facilities team
                        </div>
                    </div>
                </div>

                <div class="tool">
                    <div class="tool-icon">04</div>
                    <div>
                        <div class="tool-name">Contract Tool</div>
                        <div class="tool-result">
                            Validates vendor coverage and cost
                        </div>
                    </div>
                </div>

                <div class="tool">
                    <div class="tool-icon">05</div>
                    <div>
                        <div class="tool-name">Vendor Dispatch</div>
                        <div class="tool-result">
                            Creates an authorized work order
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:

        st.markdown(
            """
            <div class="card">
                <div class="card-title">Governance Model</div>
                <div class="card-subtitle">
                    Human control remains part of the workflow
                </div>

                <div class="decision" style="margin-bottom:9px;">
                    <div class="decision-label">Automatic</div>
                    <div class="decision-value">
                        Genuine duplicates
                    </div>
                </div>

                <div class="decision" style="margin-bottom:9px;">
                    <div class="decision-label">Automatic</div>
                    <div class="decision-value">
                        Low-cost covered vendor work
                    </div>
                </div>

                <div class="decision" style="margin-bottom:9px;">
                    <div class="decision-label">Human review</div>
                    <div class="decision-value">
                        Safety-critical requests
                    </div>
                </div>

                <div class="decision">
                    <div class="decision-label">Human review</div>
                    <div class="decision-value">
                        Low-confidence classifications
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#94a3b8;
        font-size:9px;
        padding:25px 0 5px 0;
    ">
        XDATA · Facilities AI Agent · AI Day Demo · Demo environment
    </div>
    """,
    unsafe_allow_html=True,
)
