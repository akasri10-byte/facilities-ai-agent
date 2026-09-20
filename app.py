import streamlit as st
import pandas as pd
import re
import uuid
from datetime import datetime
from difflib import SequenceMatcher

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Facilities AI Agent",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CSS - ENTERPRISE AI OPERATIONS CENTER
# ============================================================

st.markdown("""
<style>

    .stApp {
        background: #0b1020;
        color: #e8ecf7;
    }

    section[data-testid="stSidebar"] {
        background: #080d19;
        border-right: 1px solid #20283a;
    }

    .block-container {
        padding-top: 1.5rem;
        max-width: 1500px;
    }

    .brand {
        font-size: 25px;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: white;
    }

    .brand-sub {
        font-size: 12px;
        color: #7f8aa3;
        margin-bottom: 20px;
    }

    .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #11182a;
        border: 1px solid #222c40;
        border-radius: 14px;
        padding: 18px 22px;
        margin-bottom: 18px;
    }

    .page-title {
        font-size: 27px;
        font-weight: 750;
        color: #ffffff;
    }

    .page-subtitle {
        color: #8d98ae;
        font-size: 13px;
        margin-top: 4px;
    }

    .online {
        background: #123426;
        color: #62e6a4;
        border: 1px solid #1e6649;
        border-radius: 20px;
        padding: 7px 13px;
        font-size: 12px;
        font-weight: 700;
    }

    .metric {
        background: #11182a;
        border: 1px solid #222c40;
        border-radius: 14px;
        padding: 17px;
        min-height: 105px;
    }

    .metric-label {
        color: #7f8aa3;
        font-size: 12px;
    }

    .metric-value {
        font-size: 29px;
        font-weight: 800;
        color: white;
        margin-top: 8px;
    }

    .metric-note {
        font-size: 11px;
        color: #5ed99b;
        margin-top: 3px;
    }

    .card {
        background: #11182a;
        border: 1px solid #222c40;
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 14px;
    }

    .card-title {
        font-size: 15px;
        font-weight: 750;
        color: white;
        margin-bottom: 10px;
    }

    .small {
        color: #8d98ae;
        font-size: 12px;
    }

    .request-id {
        color: #6aa8ff;
        font-size: 12px;
        font-weight: 700;
    }

    .request-text {
        font-size: 14px;
        color: #e8ecf7;
        margin-top: 6px;
    }

    .badge {
        display: inline-block;
        padding: 4px 9px;
        border-radius: 12px;
        font-size: 10px;
        font-weight: 750;
        margin-right: 5px;
    }

    .badge-review {
        background: #493816;
        color: #ffd66b;
    }

    .badge-auto {
        background: #123b30;
        color: #6ce7ad;
    }

    .badge-duplicate {
        background: #292c40;
        color: #b9c0d7;
    }

    .badge-urgent {
        background: #492020;
        color: #ff8585;
    }

    .badge-vendor {
        background: #173d52;
        color: #73d8ff;
    }

    .confidence-high {
        color: #5fe3a0;
        font-weight: 750;
    }

    .confidence-medium {
        color: #ffd66b;
        font-weight: 750;
    }

    .confidence-low {
        color: #ff8c8c;
        font-weight: 750;
    }

    .trace {
        border-left: 3px solid #33415e;
        padding-left: 15px;
        margin-left: 5px;
    }

    .trace-step {
        background: #0d1424;
        border: 1px solid #202a3d;
        border-radius: 10px;
        padding: 11px;
        margin-bottom: 8px;
    }

    .trace-tool {
        color: #7db0ff;
        font-weight: 700;
        font-size: 12px;
    }

    .trace-output {
        color: #c4cad8;
        font-size: 12px;
        margin-top: 4px;
    }

    .decision {
        background: linear-gradient(135deg, #121e34, #11182a);
        border: 1px solid #2d4268;
        border-radius: 15px;
        padding: 20px;
    }

    .decision-main {
        font-size: 22px;
        font-weight: 800;
        color: white;
    }

    .decision-rationale {
        color: #aeb8ca;
        font-size: 13px;
        margin-top: 10px;
        line-height: 1.5;
    }

    .flow {
        background: #0d1424;
        border: 1px solid #202a3d;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        color: #b7c0d2;
        font-size: 12px;
    }

    .flow-arrow {
        color: #6c7fa5;
        text-align: center;
        padding-top: 12px;
        font-size: 20px;
    }

    .success-box {
        background: #102b21;
        border: 1px solid #1f694b;
        border-radius: 12px;
        padding: 14px;
        color: #72e4ad;
    }

    .warning-box {
        background: #302715;
        border: 1px solid #725b21;
        border-radius: 12px;
        padding: 14px;
        color: #ffd66b;
    }

    .danger-box {
        background: #32191b;
        border: 1px solid #713033;
        border-radius: 12px;
        padding: 14px;
        color: #ff9292;
    }

    .architecture {
        background: #080d18;
        border: 1px solid #273149;
        border-radius: 15px;
        padding: 20px;
        font-family: monospace;
        color: #aeb9cd;
        line-height: 1.8;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# CONSTANTS
# ============================================================

CATEGORIES = [
    "Electrical",
    "Plumbing",
    "HVAC",
    "Cleaning/Custodial",
    "Security",
]

TEAM_MAP = {
    "Electrical": "Electrical Team",
    "Plumbing": "Plumbing Team",
    "HVAC": "HVAC Team",
    "Cleaning/Custodial": "Facilities Cleaning Team",
    "Security": "Security Operations",
}


# ============================================================
# DEMO DATA
# No files / CSV required
# ============================================================

DEMO_REQUESTS = [
    {
        "request_id": "REQ-1042",
        "description": "There are sparks coming from the socket near the pantry.",
        "location": "Mumbai - Floor 4 Pantry",
        "employee": "Rahul",
    },
    {
        "request_id": "REQ-1039",
        "description": "The AC in meeting room 4B is running but not cooling.",
        "location": "Mumbai - Floor 4 Meeting Room 4B",
        "employee": "Neha",
    },
    {
        "request_id": "REQ-1035",
        "description": "Water is leaking below the pantry sink.",
        "location": "Mumbai - Floor 4 Pantry",
        "employee": "Amit",
    },
    {
        "request_id": "REQ-1045",
        "description": "Something seems wrong with the air and ventilation here.",
        "location": "Mumbai - Floor 6",
        "employee": "Priya",
    },
    {
        "request_id": "REQ-1047",
        "description": "The washroom tap is continuously dripping.",
        "location": "Mumbai - Floor 3 Washroom",
        "employee": "Rohan",
    },
    {
        "request_id": "REQ-1048",
        "description": "The lights in the corridor are not working.",
        "location": "Mumbai - Floor 2 Corridor",
        "employee": "Sneha",
    },
    {
        "request_id": "REQ-1049",
        "description": "Please clean the pantry area. There is food waste around the tables.",
        "location": "Mumbai - Floor 4 Pantry",
        "employee": "Vikas",
    },
    {
        "request_id": "REQ-1050",
        "description": "A person without an employee badge is waiting near the restricted server room.",
        "location": "Mumbai - Floor 7 Server Area",
        "employee": "Karan",
    },
    {
        "request_id": "REQ-1051",
        "description": "The AC is making a strange noise and temperature is increasing.",
        "location": "Mumbai - Floor 5",
        "employee": "Anjali",
    },
    {
        "request_id": "REQ-1052",
        "description": "The restroom floor is wet and there may be a leak.",
        "location": "Mumbai - Floor 3 Washroom",
        "employee": "Suresh",
    },
    {
        "request_id": "REQ-1053",
        "description": "Can someone replace the broken light near the elevators?",
        "location": "Mumbai - Floor 2 Elevator Lobby",
        "employee": "Meera",
    },
    {
        "request_id": "REQ-1054",
        "description": "The office area needs cleaning after an event.",
        "location": "Mumbai - Floor 8",
        "employee": "Arjun",
    },
]


# ============================================================
# DEMO VENDOR CONTRACTS
# ============================================================

DEMO_CONTRACTS = [
    {
        "vendor": "CoolAir Services",
        "category": "HVAC",
        "covered": True,
        "estimated_cost": 280,
        "contract_id": "CON-HVAC-001",
    },
    {
        "vendor": "PowerFix Solutions",
        "category": "Electrical",
        "covered": True,
        "estimated_cost": 350,
        "contract_id": "CON-ELEC-001",
    },
    {
        "vendor": "AquaCare Facilities",
        "category": "Plumbing",
        "covered": True,
        "estimated_cost": 220,
        "contract_id": "CON-PLUMB-001",
    },
    {
        "vendor": "CleanPro",
        "category": "Cleaning/Custodial",
        "covered": True,
        "estimated_cost": 150,
        "contract_id": "CON-CLEAN-001",
    },
]


# ============================================================
# SESSION STATE
# ============================================================

if "requests" not in st.session_state:
    st.session_state.requests = {}

if "events" not in st.session_state:
    st.session_state.events = {}

if "vendor_orders" not in st.session_state:
    st.session_state.vendor_orders = []

if "processed" not in st.session_state:
    st.session_state.processed = False

if "selected_request" not in st.session_state:
    st.session_state.selected_request = None

if "llm_mode" not in st.session_state:
    st.session_state.llm_mode = "DEMO"

if "confidence_threshold" not in st.session_state:
    st.session_state.confidence_threshold = 0.72

if "low_cost_threshold" not in st.session_state:
    st.session_state.low_cost_threshold = 500


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def generate_request_id():
    return "REQ-" + str(1000 + len(st.session_state.requests) + 1)


def generate_work_order():
    return "WO-" + uuid.uuid4().hex[:9].upper()


def confidence_class(value):
    if value >= 0.85:
        return "confidence-high"
    if value >= 0.72:
        return "confidence-medium"
    return "confidence-low"


# ============================================================
# FAKE LLM
# ============================================================

class FakeLLM:

    def classify(self, description, context=""):

        text = description.lower()

        # ----------------------------------------------------
        # ELECTRICAL
        # ----------------------------------------------------
        electrical = [
            "spark",
            "sparks",
            "socket",
            "power",
            "electric",
            "electricity",
            "switch",
            "light",
            "lights",
            "bulb",
            "wiring",
            "short circuit",
        ]

        # ----------------------------------------------------
        # PLUMBING
        # ----------------------------------------------------
        plumbing = [
            "water",
            "leak",
            "leaking",
            "tap",
            "faucet",
            "sink",
            "pipe",
            "toilet",
            "washroom",
            "drain",
        ]

        # ----------------------------------------------------
        # HVAC
        # ----------------------------------------------------
        hvac = [
            "ac",
            "air conditioning",
            "air conditioner",
            "cooling",
            "temperature",
            "ventilation",
            "heating",
            "heater",
            "hvac",
            "air",
        ]

        # ----------------------------------------------------
        # CLEANING
        # ----------------------------------------------------
        cleaning = [
            "clean",
            "cleaning",
            "dirty",
            "waste",
            "garbage",
            "trash",
            "spill",
            "dust",
        ]

        # ----------------------------------------------------
        # SECURITY
        # ----------------------------------------------------
        security = [
            "badge",
            "unauthorized",
            "unknown person",
            "security",
            "intruder",
            "restricted",
            "access",
            "suspicious",
        ]

        scores = {
            "Electrical": sum(word in text for word in electrical),
            "Plumbing": sum(word in text for word in plumbing),
            "HVAC": sum(word in text for word in hvac),
            "Cleaning/Custodial": sum(word in text for word in cleaning),
            "Security": sum(word in text for word in security),
        }

        category = max(scores, key=scores.get)
        score = scores[category]

        # ----------------------------------------------------
        # Ambiguous request
        # ----------------------------------------------------

        if score == 0:
            return {
                "category": "HVAC",
                "confidence": 0.55,
                "needs_context": True,
                "rationale": "The request is too vague to classify reliably.",
            }

        # ----------------------------------------------------
        # Confidence
        # ----------------------------------------------------

        confidence = min(0.96, 0.70 + (score * 0.08))

        if score >= 3:
            confidence = 0.94

        if category == "Security":
            confidence = 0.96

        rationale = {
            "Electrical": "Detected electrical-equipment terms such as power, socket, light or wiring.",
            "Plumbing": "Detected water-system terms such as leak, sink, tap, pipe or washroom.",
            "HVAC": "Detected temperature, AC, cooling or ventilation indicators.",
            "Cleaning/Custodial": "Detected cleaning, waste, garbage or cleanliness indicators.",
            "Security": "Detected access-control or security-related indicators.",
        }[category]

        return {
            "category": category,
            "confidence": confidence,
            "needs_context": confidence < st.session_state.confidence_threshold,
            "rationale": rationale,
        }


# ============================================================
# AGENT TOOLS
# ============================================================

def log_event(request_id, tool, summary, output=None):

    if request_id not in st.session_state.events:
        st.session_state.events[request_id] = []

    st.session_state.events[request_id].append({
        "time": now(),
        "tool": tool,
        "summary": summary,
        "output": output or "",
    })


def find_related_history(request, all_requests):

    description = request["description"].lower()

    related = []

    for item in all_requests:

        if item["request_id"] == request["request_id"]:
            continue

        similarity = SequenceMatcher(
            None,
            description,
            item["description"].lower()
        ).ratio()

        same_location = (
            request["location"].lower()
            == item["location"].lower()
        )

        if similarity >= 0.42 or (same_location and similarity >= 0.25):
            related.append({
                "request_id": item["request_id"],
                "description": item["description"],
                "similarity": round(similarity, 2),
            })

    related.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return related[:3]


def get_additional_context(request, related):

    return {
        "location": request["location"],
        "employee": request["employee"],
        "related_count": len(related),
        "historical_signal": (
            "Similar requests exist"
            if related
            else "No strong historical signal"
        ),
    }


def route_request(request_id, category):

    team = TEAM_MAP[category]

    log_event(
        request_id,
        "route_request",
        f"Request routed to {team}",
        team
    )

    return team


def acknowledge(request_id):

    message = "Automated acknowledgement sent to employee."

    log_event(
        request_id,
        "acknowledge",
        message,
        "Acknowledged"
    )

    return True


def close_duplicate(request_id, related_request):

    summary = (
        f"Request closed as duplicate of "
        f"{related_request['request_id']}"
    )

    log_event(
        request_id,
        "close_duplicate",
        summary,
        related_request["request_id"]
    )

    return True


def check_vendor_coverage(request_id, category):

    matches = [
        x for x in DEMO_CONTRACTS
        if x["category"] == category
    ]

    if not matches:
        result = {
            "covered": False,
            "reason": "No matching contract found."
        }

    else:

        contract = matches[0]

        result = {
            "covered": contract["covered"],
            "vendor": contract["vendor"],
            "estimated_cost": contract["estimated_cost"],
            "contract_id": contract["contract_id"],
        }

    log_event(
        request_id,
        "check_vendor_coverage",
        f"Checked vendor contract for {category}",
        str(result)
    )

    return result


def dispatch_vendor_work_order(request_id, category, contract):

    work_order = {
        "work_order_id": generate_work_order(),
        "request_id": request_id,
        "category": category,
        "vendor": contract["vendor"],
        "estimated_cost": contract["estimated_cost"],
        "contract_id": contract["contract_id"],
        "status": "DISPATCHED",
        "created_at": now(),
    }

    st.session_state.vendor_orders.append(work_order)

    log_event(
        request_id,
        "dispatch_vendor_work_order",
        f"Vendor work order dispatched to {contract['vendor']}",
        work_order["work_order_id"]
    )

    return work_order


# ============================================================
# URGENCY DETECTION
# ============================================================

def detect_urgency(description):

    text = description.lower()

    urgent_words = [
        "spark",
        "sparks",
        "fire",
        "smoke",
        "shock",
        "electric shock",
        "flood",
        "burst pipe",
        "intruder",
        "unauthorized person",
        "security threat",
        "danger",
    ]

    matched = [
        word for word in urgent_words
        if word in text
    ]

    return len(matched) > 0, matched


# ============================================================
# AGENT
# ============================================================

def run_agent(request, all_requests):

    llm = FakeLLM()

    request_id = request["request_id"]

    # --------------------------------------------------------
    # STEP 1 - CLASSIFY
    # --------------------------------------------------------

    classification = llm.classify(
        request["description"]
    )

    log_event(
        request_id,
        "fake_llm",
        f"Classified as {classification['category']} "
        f"with confidence {classification['confidence']:.2f}",
        classification["rationale"]
    )

    # --------------------------------------------------------
    # STEP 2 - HISTORY
    # --------------------------------------------------------

    related = find_related_history(
        request,
        all_requests
    )

    log_event(
        request_id,
        "find_related_history",
        f"Found {len(related)} related historical request(s)",
        str(related)
    )

    # --------------------------------------------------------
    # STEP 3 - CONTEXT IF UNCERTAIN
    # --------------------------------------------------------

    if (
        classification["confidence"]
        < st.session_state.confidence_threshold
        or classification["needs_context"]
    ):

        context = get_additional_context(
            request,
            related
        )

        log_event(
            request_id,
            "get_additional_context",
            "Additional context requested because confidence was low.",
            str(context)
        )

        context_text = (
            f"Location: {context['location']}. "
            f"Historical signal: {context['historical_signal']}."
        )

        classification = llm.classify(
            request["description"],
            context_text
        )

        log_event(
            request_id,
            "fake_llm_recheck",
            f"Reclassified as {classification['category']} "
            f"with confidence {classification['confidence']:.2f}",
            classification["rationale"]
        )

    # --------------------------------------------------------
    # STEP 4 - URGENCY
    # --------------------------------------------------------

    urgent, safety_signals = detect_urgency(
        request["description"]
    )

    if urgent:

        log_event(
            request_id,
            "urgency_check",
            "Immediate human attention required.",
            ", ".join(safety_signals)
        )

        team = route_request(
            request_id,
            classification["category"]
        )

        acknowledge(request_id)

        return {
            "category": classification["category"],
            "confidence": classification["confidence"],
            "team": team,
            "action": "HUMAN REVIEW",
            "status": "HUMAN ATTENTION",
            "urgent": True,
            "duplicate": False,
            "vendor_order": None,
            "rationale": (
                classification["rationale"]
                + " Safety signal detected, so the agent escalated "
                  "the request for immediate human attention."
            ),
            "related": related,
        }

    # --------------------------------------------------------
    # STEP 5 - LOW CONFIDENCE
    # --------------------------------------------------------

    if classification["confidence"] < 0.72:

        team = route_request(
            request_id,
            classification["category"]
        )

        acknowledge(request_id)

        return {
            "category": classification["category"],
            "confidence": classification["confidence"],
            "team": team,
            "action": "HUMAN REVIEW",
            "status": "REVIEW",
            "urgent": False,
            "duplicate": False,
            "vendor_order": None,
            "rationale": (
                classification["rationale"]
                + " Confidence remains below the review threshold."
            ),
            "related": related,
        }

    # --------------------------------------------------------
    # STEP 6 - DUPLICATE
    # --------------------------------------------------------

    if related:

        strongest = related[0]

        if strongest["similarity"] >= 0.60:

            close_duplicate(
                request_id,
                strongest
            )

            return {
                "category": classification["category"],
                "confidence": classification["confidence"],
                "team": TEAM_MAP[classification["category"]],
                "action": "CLOSE DUPLICATE",
                "status": "CLOSED DUPLICATE",
                "urgent": False,
                "duplicate": True,
                "vendor_order": None,
                "rationale": (
                    classification["rationale"]
                    + f" A closely related request "
                      f"({strongest['request_id']}) was found."
                ),
                "related": related,
            }

    # --------------------------------------------------------
    # STEP 7 - ROUTE
    # --------------------------------------------------------

    team = route_request(
        request_id,
        classification["category"]
    )

    acknowledge(request_id)

    # --------------------------------------------------------
    # STEP 8 - VENDOR CONTRACT
    # --------------------------------------------------------

    vendor_order = None

    if classification["category"] in [
        "Electrical",
        "Plumbing",
        "HVAC",
    ]:

        contract = check_vendor_coverage(
            request_id,
            classification["category"]
        )

        if (
            contract.get("covered")
            and contract.get("estimated_cost") is not None
            and contract["estimated_cost"]
            <= st.session_state.low_cost_threshold
        ):

            vendor_order = dispatch_vendor_work_order(
                request_id,
                classification["category"],
                contract
            )

            action = "AUTO ROUTED + VENDOR DISPATCHED"
            status = "VENDOR DISPATCHED"

        else:

            action = "AUTO ROUTED"
            status = "AUTO ROUTED"

    else:

        action = "AUTO ROUTED"
        status = "AUTO ROUTED"

    # --------------------------------------------------------
    # FINAL DECISION
    # --------------------------------------------------------

    return {
        "category": classification["category"],
        "confidence": classification["confidence"],
        "team": team,
        "action": action,
        "status": status,
        "urgent": False,
        "duplicate": False,
        "vendor_order": vendor_order,
        "rationale": classification["rationale"],
        "related": related,
    }


# ============================================================
# PROCESS ALL DEMO REQUESTS
# ============================================================

def process_all_requests():

    st.session_state.requests = {}
    st.session_state.events = {}
    st.session_state.vendor_orders = []

    for request in DEMO_REQUESTS:

        result = run_agent(
            request,
            DEMO_REQUESTS
        )

        st.session_state.requests[
            request["request_id"]
        ] = {
            **request,
            **result,
            "processed_at": now(),
            "human_override": None,
        }

    st.session_state.processed = True


# ============================================================
# PROCESS SINGLE REQUEST
# ============================================================

def process_single_request(description, location, employee):

    request = {
        "request_id": generate_request_id(),
        "description": description,
        "location": location,
        "employee": employee,
    }

    existing = list(
        st.session_state.requests.values()
    )

    result = run_agent(
        request,
        existing
    )

    st.session_state.requests[
        request["request_id"]
    ] = {
        **request,
        **result,
        "processed_at": now(),
        "human_override": None,
    }

    st.session_state.selected_request = request["request_id"]

    return request["request_id"]


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="brand">🏢 FacilitiesAgent</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="brand-sub">AI Facilities Operations Center</div>',
        unsafe_allow_html=True
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
        ]
    )

    st.divider()

    st.markdown("### Agent Settings")

    st.selectbox(
        "LLM Mode",
        ["DEMO / FAKE LLM"],
        index=0,
        disabled=True
    )

    st.session_state.confidence_threshold = st.slider(
        "Confidence threshold",
        0.50,
        0.95,
        st.session_state.confidence_threshold,
        0.01
    )

    st.session_state.low_cost_threshold = st.number_input(
        "Low-cost threshold ₹",
        min_value=50,
        max_value=5000,
        value=st.session_state.low_cost_threshold,
        step=50
    )

    st.divider()

    st.markdown("### Demo Controls")

    if st.button(
        "▶ Run Agent on Demo Data",
        use_container_width=True
    ):
        process_all_requests()
        st.success("Agent run completed.")

    if st.button(
        "↻ Reset Demo",
        use_container_width=True
    ):
        st.session_state.requests = {}
        st.session_state.events = {}
        st.session_state.vendor_orders = []
        st.session_state.processed = False
        st.session_state.selected_request = None
        st.rerun()

    st.divider()

    st.markdown(
        """
        <div class="small">
        Environment<br>
        <b>DEMO</b><br><br>
        LLM<br>
        <b>Fake / Deterministic</b><br><br>
        Tools<br>
        <b>7 simulated tools</b><br><br>
        Database<br>
        <b>Session State</b>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# HEADER
# ============================================================

def page_header(title, subtitle):

    st.markdown(
        f"""
        <div class="topbar">
            <div>
                <div class="page-title">{title}</div>
                <div class="page-subtitle">{subtitle}</div>
            </div>
            <div class="online">● AGENT ONLINE</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# COMMAND CENTER
# ============================================================

if page == "Command Center":

    page_header(
        "Facilities AI Agent",
        "Autonomous intake, classification, routing and vendor operations"
    )

    requests = list(
        st.session_state.requests.values()
    )

    total = len(requests)

    human = len([
        x for x in requests
        if x.get("status") in [
            "HUMAN ATTENTION",
            "REVIEW"
        ]
    ])

    duplicates = len([
        x for x in requests
        if x.get("duplicate")
    ])

    vendor_count = len(
        st.session_state.vendor_orders
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="metric">
                <div class="metric-label">TOTAL REQUESTS</div>
                <div class="metric-value">{total}</div>
                <div class="metric-note">Demo stream</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric">
                <div class="metric-label">HUMAN ATTENTION</div>
                <div class="metric-value">{human}</div>
                <div class="metric-note">Requires review</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric">
                <div class="metric-label">DUPLICATES CLOSED</div>
                <div class="metric-value">{duplicates}</div>
                <div class="metric-note">Auto-closed</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"""
            <div class="metric">
                <div class="metric-label">VENDOR ORDERS</div>
                <div class="metric-value">{vendor_count}</div>
                <div class="metric-note">Auto-dispatched</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("")

    # --------------------------------------------------------
    # RUN FIRST
    # --------------------------------------------------------

    if not st.session_state.processed:

        st.markdown(
            """
            <div class="card">
                <div class="card-title">
                    🚀 Start the AI Facilities Agent
                </div>
                <div class="small">
                    This mobile demo contains built-in sample requests.
                    No CSV, database or external LLM is required.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "▶ START DEMO AGENT",
            type="primary",
            use_container_width=True
        ):
            process_all_requests()
            st.rerun()

    else:

        left, right = st.columns([1.25, 0.75])

        # ----------------------------------------------------
        # RECENT ACTIVITY
        # ----------------------------------------------------

        with left:

            st.markdown(
                """
                <div class="card-title">
                    Live Agent Activity
                </div>
                """,
                unsafe_allow_html=True
            )

            for request in requests[-6:][::-1]:

                status = request["status"]

                if status == "HUMAN ATTENTION":
                    badge = '<span class="badge badge-urgent">HUMAN ATTENTION</span>'
                elif status == "CLOSED DUPLICATE":
                    badge = '<span class="badge badge-duplicate">DUPLICATE CLOSED</span>'
                elif status == "VENDOR DISPATCHED":
                    badge = '<span class="badge badge-vendor">VENDOR DISPATCHED</span>'
                elif status == "REVIEW":
                    badge = '<span class="badge badge-review">REVIEW</span>'
                else:
                    badge = '<span class="badge badge-auto">AUTO ROUTED</span>'

                st.markdown(
                    f"""
                    <div class="card">
                        <div class="request-id">
                            {request['request_id']}
                        </div>

                        <div class="request-text">
                            {request['description']}
                        </div>

                        <div style="margin-top:10px">
                            {badge}
                            <span class="badge badge-auto">
                                {request['category']}
                            </span>
                        </div>

                        <div class="small" style="margin-top:8px">
                            {request['team']}
                            &nbsp; • &nbsp;
                            confidence {request['confidence']:.2f}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # ----------------------------------------------------
        # ATTENTION
        # ----------------------------------------------------

        with right:

            st.markdown(
                """
                <div class="card-title">
                    ⚠ Human Attention
                </div>
                """,
                unsafe_allow_html=True
            )

            attention = [
                x for x in requests
                if x["status"] in [
                    "HUMAN ATTENTION",
                    "REVIEW"
                ]
            ]

            if not attention:

                st.markdown(
                    '<div class="success-box">No pending reviews.</div>',
                    unsafe_allow_html=True
                )

            for request in attention:

                st.markdown(
                    f"""
                    <div class="warning-box">
                        <b>{request['request_id']}</b><br>
                        {request['description']}<br><br>
                        Category: <b>{request['category']}</b><br>
                        Confidence: <b>{request['confidence']:.2f}</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # --------------------------------------------------------
    # SIMULATE NEW REQUEST
    # --------------------------------------------------------

    st.markdown("### 🧪 Simulate New Request")

    with st.form("new_request_form"):

        description = st.text_area(
            "Employee issue",
            placeholder=(
                "Example: There is smoke coming from the electrical panel..."
            )
        )

        col1, col2 = st.columns(2)

        with col1:
            location = st.text_input(
                "Location",
                "Mumbai - Floor 4"
            )

        with col2:
            employee = st.text_input(
                "Employee",
                "Demo Employee"
            )

        submitted = st.form_submit_button(
            "Send to AI Agent",
            use_container_width=True
        )

        if submitted:

            if description.strip():

                rid = process_single_request(
                    description,
                    location,
                    employee
                )

                st.success(
                    f"{rid} processed by the agent."
                )

                st.rerun()

            else:
                st.warning(
                    "Please enter an employee issue."
                )


# ============================================================
# REQUEST QUEUE
# ============================================================

elif page == "Request Queue":

    page_header(
        "Request Queue",
        "All employee facilities requests processed by the agent"
    )

    requests = list(
        st.session_state.requests.values()
    )

    if not requests:

        st.info(
            "Run the demo agent first from the sidebar."
        )

    else:

        status_filter = st.multiselect(
            "Filter status",
            sorted(
                list(
                    set(
                        x["status"]
                        for x in requests
                    )
                )
            ),
        )

        category_filter = st.multiselect(
            "Filter category",
            CATEGORIES,
        )

        filtered = requests

        if status_filter:
            filtered = [
                x for x in filtered
                if x["status"] in status_filter
            ]

        if category_filter:
            filtered = [
                x for x in filtered
                if x["category"] in category_filter
            ]

        for request in filtered:

            with st.expander(
                f"{request['request_id']}  |  "
                f"{request['category']}  |  "
                f"{request['status']}"
            ):

                c1, c2, c3 = st.columns(3)

                with c1:
                    st.write(
                        f"**Employee:** {request['employee']}"
                    )
                    st.write(
                        f"**Location:** {request['location']}"
                    )

                with c2:
                    st.write(
                        f"**Category:** {request['category']}"
                    )
                    st.write(
                        f"**Team:** {request['team']}"
                    )

                with c3:
                    st.write(
                        f"**Confidence:** {request['confidence']:.2f}"
                    )
                    st.write(
                        f"**Action:** {request['action']}"
                    )

                st.markdown(
                    f"**Issue:** {request['description']}"
                )

                st.markdown(
                    f"""
                    <div class="decision-rationale">
                    <b>Agent rationale:</b>
                    {request['rationale']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ============================================================
# AGENT EXECUTION
# ============================================================

elif page == "Agent Execution":

    page_header(
        "Agent Execution",
        "See how the AI agent reached a decision using tools"
    )

    requests = list(
        st.session_state.requests.values()
    )

    if not requests:

        st.info(
            "Run the demo agent first."
        )

    else:

        ids = [
            x["request_id"]
            for x in requests
        ]

        selected = st.selectbox(
            "Select request",
            ids
        )

        request = next(
            x for x in requests
            if x["request_id"] == selected
        )

        # ----------------------------------------------------
        # REQUEST
        # ----------------------------------------------------

        st.markdown(
            f"""
            <div class="card">
                <div class="request-id">
                    {request['request_id']}
                </div>

                <div class="request-text">
                    {request['description']}
                </div>

                <div class="small" style="margin-top:8px">
                    📍 {request['location']}
                    &nbsp;&nbsp; | &nbsp;&nbsp;
                    👤 {request['employee']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # DECISION
        # ----------------------------------------------------

        st.markdown("### Agent Decision")

        st.markdown(
            f"""
            <div class="decision">

                <div class="decision-main">
                    {request['category']}
                </div>

                <div style="margin-top:8px">
                    <b>Confidence:</b>
                    {request['confidence']:.2f}
                    &nbsp;&nbsp; • &nbsp;&nbsp;
                    <b>Team:</b>
                    {request['team']}
                </div>

                <div style="margin-top:10px">
                    <b>Action:</b>
                    {request['action']}
                </div>

                <div class="decision-rationale">
                    <b>Why did the agent do this?</b><br>
                    {request['rationale']}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(
            min(
                max(request["confidence"], 0),
                1
            )
        )

        # ----------------------------------------------------
        # TOOL TRACE
        # ----------------------------------------------------

        st.markdown("### 🔎 Agent Tool Trace")

        events = st.session_state.events.get(
            request["request_id"],
            []
        )

        st.markdown(
            '<div class="trace">',
            unsafe_allow_html=True
        )

        for index, event in enumerate(events, 1):

            st.markdown(
                f"""
                <div class="trace-step">

                    <div class="trace-tool">
                        STEP {index}
                        &nbsp; • &nbsp;
                        {event['tool']}
                    </div>

                    <div class="trace-output">
                        {event['summary']}
                    </div>

                    <div class="small">
                        {event['time']}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # RELATED HISTORY
        # ----------------------------------------------------

        if request["related"]:

            st.markdown("### Related History")

            for item in request["related"]:

                st.markdown(
                    f"""
                    <div class="card">
                        <b>{item['request_id']}</b>
                        &nbsp; • &nbsp;
                        similarity {item['similarity']}<br>
                        <span class="small">
                        {item['description']}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # ----------------------------------------------------
        # VENDOR ORDER
        # ----------------------------------------------------

        if request["vendor_order"]:

            order = request["vendor_order"]

            st.markdown("### 🛠 Vendor Work Order")

            st.markdown(
                f"""
                <div class="success-box">

                    <b>{order['work_order_id']}</b><br><br>

                    Vendor:
                    <b>{order['vendor']}</b><br>

                    Category:
                    <b>{order['category']}</b><br>

                    Estimated Cost:
                    <b>₹{order['estimated_cost']}</b><br>

                    Contract:
                    <b>{order['contract_id']}</b><br>

                    Status:
                    <b>{order['status']}</b>

                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# VENDOR OPERATIONS
# ============================================================

elif page == "Vendor Operations":

    page_header(
        "Vendor Operations",
        "Autonomous vendor coverage checks and work-order dispatch"
    )

    orders = st.session_state.vendor_orders

    if not orders:

        st.info(
            "No vendor work orders yet. Run the demo agent."
        )

    else:

        total_cost = sum(
            x["estimated_cost"]
            for x in orders
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Work Orders",
                len(orders)
            )

        with c2:
            st.metric(
                "Estimated Spend",
                f"₹{total_cost}"
            )

        with c3:
            st.metric(
                "Auto Dispatch",
                "100%"
            )

        st.markdown("### Dispatched Work Orders")

        for order in orders:

            st.markdown(
                f"""
                <div class="card">

                    <div class="request-id">
                        {order['work_order_id']}
                    </div>

                    <div class="card-title">
                        {order['category']} — {order['vendor']}
                    </div>

                    <div class="small">
                        Request: {order['request_id']}
                        &nbsp; • &nbsp;
                        Contract: {order['contract_id']}
                    </div>

                    <div style="margin-top:10px">
                        Estimated cost:
                        <b>₹{order['estimated_cost']}</b>
                        &nbsp;&nbsp;
                        <span class="badge badge-vendor">
                            {order['status']}
                        </span>
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("### Vendor Contract Coverage")

    df = pd.DataFrame(DEMO_CONTRACTS)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# HUMAN REVIEW & AUDIT
# ============================================================

elif page == "Human Review & Audit":

    page_header(
        "Human Review & Audit",
        "Human-in-the-loop decisions and complete agent activity trail"
    )

    requests = list(
        st.session_state.requests.values()
    )

    if not requests:

        st.info(
            "Run the demo agent first."
        )

    else:

        pending = [
            x for x in requests
            if x["status"] in [
                "HUMAN ATTENTION",
                "REVIEW"
            ]
        ]

        st.markdown(
            f"""
            <div class="warning-box">
                <b>{len(pending)}</b>
                request(s) require human attention.
            </div>
            """,
            unsafe_allow_html=True
        )

        if pending:

            selected = st.selectbox(
                "Select request for review",
                [
                    x["request_id"]
                    for x in pending
                ]
            )

            request = next(
                x for x in pending
                if x["request_id"] == selected
            )

            st.markdown("### Review Request")

            st.markdown(
                f"""
                <div class="card">

                    <b>{request['request_id']}</b><br><br>

                    {request['description']}<br><br>

                    <span class="small">
                    Current category:
                    {request['category']}
                    &nbsp; • &nbsp;
                    Confidence:
                    {request['confidence']:.2f}
                    </span>

                </div>
                """,
                unsafe_allow_html=True
            )

            new_category = st.selectbox(
                "Human-approved category",
                CATEGORIES,
                index=CATEGORIES.index(
                    request["category"]
                )
            )

            reviewer_reason = st.text_area(
                "Reviewer's reason",
                placeholder="Explain why you are overriding or confirming the agent."
            )

            if st.button(
                "✓ Apply Human Decision",
                type="primary"
            ):

                old_category = request["category"]

                request["category"] = new_category
                request["team"] = TEAM_MAP[new_category]
                request["human_override"] = {
                    "from": old_category,
                    "to": new_category,
                    "reason": reviewer_reason,
                    "time": now(),
                }
                request["status"] = "HUMAN APPROVED"
                request["action"] = "HUMAN OVERRIDE"

                log_event(
                    request["request_id"],
                    "human_override",
                    f"Human changed category from {old_category} "
                    f"to {new_category}",
                    reviewer_reason
                )

                st.success(
                    "Human decision recorded."
                )

                st.rerun()

        # ----------------------------------------------------
        # AUDIT TRAIL
        # ----------------------------------------------------

        st.markdown("### Audit Trail")

        for request in requests:

            events = st.session_state.events.get(
                request["request_id"],
                []
            )

            with st.expander(
                f"{request['request_id']} — "
                f"{len(events)} events"
            ):

                for event in events:

                    st.markdown(
                        f"""
                        **{event['time']}**  
                        `{event['tool']}`  
                        {event['summary']}
                        """
                    )

                    if event["output"]:
                        st.caption(
                            event["output"]
                        )


# ============================================================
# ARCHITECTURE
# ============================================================

elif page == "Architecture":

    page_header(
        "Agent Architecture",
        "How the autonomous facilities workflow operates"
    )

    st.markdown("### Agent Flow")

    flow_cols = st.columns(7)

    flow_items = [
        "Employee\nRequest",
        "Fake LLM\nClassification",
        "History\nTool",
        "Context\nTool",
        "Decision\nEngine",
        "Route /\nDuplicate",
        "Vendor\nDispatch",
    ]

    for col, item in zip(
        flow_cols,
        flow_items
    ):

        with col:

            st.markdown(
                f"""
                <div class="flow">
                    {item.replace(chr(10), '<br>')}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("")

    st.markdown(
        """
        <div class="architecture">

        Employee Request
                │
                ▼
        ┌──────────────────────┐
        │      Fake LLM        │
        │  Classify + Confidence│
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  History Tool        │
        │  Find related issues │
        └──────────┬───────────┘
                   │
             Low confidence?
                   │
              ┌────┴────┐
             YES        NO
              │          │
              ▼          │
        Context Tool     │
              │          │
              ▼          │
        Re-classification │
              │          │
              └────┬─────┘
                   ▼
        ┌──────────────────────┐
        │   Decision Engine    │
        └──────────┬───────────┘
                   │
          ┌────────┼─────────┐
          │        │         │
          ▼        ▼         ▼
        Urgent   Duplicate  Normal
          │        │         │
          ▼        ▼         ▼
        Human    Auto Close Route
        Review             │
                           ▼
                    Contract Check
                           │
                     Covered + Low
                           │
                           ▼
                    Vendor Dispatch

        All actions
              │
              ▼
          Audit Trail

        Human can override
              │
              ▼
        Final decision
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Agent Principles")

    principles = [
        (
            "1. LLM is not the entire agent",
            "The LLM classifies the request. Tools perform history, routing, contract and dispatch operations."
        ),
        (
            "2. Confidence matters",
            "Low-confidence classifications trigger additional context and may require human review."
        ),
        (
            "3. Safety comes first",
            "Signals such as sparks, smoke, fire or unauthorized access trigger human attention."
        ),
        (
            "4. Duplicate detection",
            "Related historical requests are checked before creating another operational action."
        ),
        (
            "5. Controlled autonomy",
            "Vendor dispatch occurs only when contract coverage exists and estimated cost is below the configured threshold."
        ),
        (
            "6. Human-in-the-loop",
            "A human can override the agent's category and routing decision."
        ),
        (
            "7. Explainability",
            "The UI shows concise decision rationale and tool execution history rather than hidden chain-of-thought."
        ),
    ]

    for title, description in principles:

        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">{title}</div>
                <div class="small">{description}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#58657d;
        font-size:11px;
        padding:25px 0 10px 0;
    ">
        Facilities AI Agent • DEMO / FAKE LLM • xdata
    </div>
    """,
    unsafe_allow_html=True
)
