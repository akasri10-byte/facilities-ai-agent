# config.py

import os

from pathlib import Path

BASE_DIR = Path(_file__).parent

DATA DIR = BASE_DIR / "data"

# Switch between real LLM and mock LLM (set env var before running)

USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "1") == "1"

# Business thresholds

LOW_COST_THRESHOLD = 100.0

# USD

below this we auto-dispatch a vendor

IMMEDIATE_KEYWORDS = {

"fire", "electrical", "smoke", "burst",

"explosion",

"urgent", "danger", "dangerous", "hazard"

}
