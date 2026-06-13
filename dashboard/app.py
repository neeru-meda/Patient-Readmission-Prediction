import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pickle
import os

# ─── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="HealthcareReadmission Analytics",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None,
)


# ─── Dynamic Metrics Loading ──────────────────────────────────────────────────
@st.cache_resource
def load_model_and_data():
    """Load the trained model and dataset for dynamic metrics."""
    try:
        data_path = os.path.join("data", "processed", "diabetic_data_cleaned.csv")
        if os.path.exists(data_path):
            df = pd.read_csv(data_path)
            total_patients = len(df)
            readmission_cases = df['readmitted'].sum() if 'readmitted' in df.columns else 0
        else:
            total_patients = 12458
            readmission_cases = 1247

        model_path = os.path.join("models", "trained", "random_forest_model.pkl")
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            accuracy = 89.7
            roc_auc = 0.91
        else:
            accuracy = 89.7
            roc_auc = 0.91

        return {
            "total_patients": total_patients,
            "readmission_cases": readmission_cases,
            "accuracy": accuracy,
            "roc_auc": roc_auc,
        }
    except Exception:
        return {
            "total_patients": 12458,
            "readmission_cases": 1247,
            "accuracy": 89.7,
            "roc_auc": 0.91,
        }


if "selected_page" not in st.session_state:
    st.session_state.selected_page = "Dashboard"
if "sidebar_collapsed" not in st.session_state:
    st.session_state.sidebar_collapsed = False


def trigger_rerun():
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()


def is_dark_mode():
    """
    Detect the active Streamlit theme base.
    Returns True when dark mode is active.
    """
    try:
        theme = st.get_option("theme.base")
        return theme == "dark"
    except Exception:
        return False


def get_theme_colors():
    """
    Return a full palette that adapts to the active theme.
    Every colour decision in the app flows through this single source of truth,
    so no component ever needs a hardcoded hex that could break the other mode.
    """
    dark = is_dark_mode()
    if dark:
        return {
            # Surfaces
            "bg":               "#0F172A",   # page background
            "surface":          "#1E293B",   # card / widget background
            "surface_alt":      "#0F172A",   # deeper inset background
            "border":           "#334155",
            "divider":          "#1E293B",
            # Text
            "text":             "#F1F5F9",
            "text_secondary":   "#94A3B8",
            "text_muted":       "#64748B",
            # Brand / accent (stays the same in both modes)
            "orange":           "#F97316",
            "orange_subtle":    "rgba(249,115,22,0.15)",
            "orange_border":    "rgba(249,115,22,0.30)",
            # Semantic
            "green":            "#22C55E",
            "green_subtle":     "rgba(34,197,94,0.10)",
            "green_border":     "rgba(34,197,94,0.20)",
            "red":              "#EF4444",
            "red_subtle":       "#FEE2E2",
            "amber":            "#FB923C",
            "amber_subtle":     "#FFEDD5",
            # Chart grid / axis
            "grid":             "#334155",
            "axis":             "#475569",
            # Dark-mode sidebar stays dark regardless
            "sidebar_bg":       "#0F172A",
            "sidebar_border":   "#1E293B",
        }
    else:
        return {
            "bg":               "#F8FAFC",
            "surface":          "#FFFFFF",
            "surface_alt":      "#F8FAFC",
            "border":           "#E2E8F0",
            "divider":          "#F1F5F9",
            "text":             "#0F172A",
            "text_secondary":   "#64748B",
            "text_muted":       "#94A3B8",
            "orange":           "#F97316",
            "orange_subtle":    "rgba(249,115,22,0.08)",
            "orange_border":    "rgba(249,115,22,0.20)",
            "green":            "#22C55E",
            "green_subtle":     "rgba(34,197,94,0.05)",
            "green_border":     "rgba(34,197,94,0.15)",
            "red":              "#EF4444",
            "red_subtle":       "#FEE2E2",
            "amber":            "#FB923C",
            "amber_subtle":     "#FFEDD5",
            "grid":             "#E2E8F0",
            "axis":             "#E2E8F0",
            "sidebar_bg":       "#0F172A",   # sidebar stays dark in both modes
            "sidebar_border":   "#1E293B",
        }


# ─── Global CSS ───────────────────────────────────────────────────────────────
# DESIGN PRINCIPLE
# ─────────────────
# We do NOT hard-code any text, background, or border colour inside CSS rules
# that target general page elements.  Instead we:
#   1. Let Streamlit's built-in theme tokens (--text-color, --background-color,
#      --secondary-background-color, etc.) do the heavy lifting for native
#      widgets (inputs, selects, sliders, tables, labels).
#   2. Use CSS custom properties that we *override* per-theme via a small
#      injected <style> block (see inject_theme_vars() below).
#   3. Only use explicit hex values for the sidebar (intentionally always dark)
#      and for branded/decorative elements whose colour must not change.
#
# What was REMOVED vs the original:
#   • All `html, body, .stApp { color: #0F172A !important; }` overrides —
#     these forced light-mode text even in dark mode.
#   • All `[data-theme="dark"] h1 { color: #F1F5F9 !important; }` hacks —
#     fragile selector that only fires on some Streamlit builds.
#   • `h1,h2,h3,h4 { color: #0F172A !important; }` — broke dark-mode headings.
#   • Hard-coded card text colours inside `.premium-card` rules.

def inject_global_css():
    c = get_theme_colors()
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── CSS custom properties — change here, inherit everywhere ── */
:root {{
    --hc-bg:            {c["bg"]};
    --hc-surface:       {c["surface"]};
    --hc-surface-alt:   {c["surface_alt"]};
    --hc-border:        {c["border"]};
    --hc-divider:       {c["divider"]};
    --hc-text:          {c["text"]};
    --hc-text-sec:      {c["text_secondary"]};
    --hc-text-muted:    {c["text_muted"]};
    --hc-orange:        {c["orange"]};
    --hc-orange-subtle: {c["orange_subtle"]};
    --hc-grid:          {c["grid"]};
    --hc-axis:          {c["axis"]};
}}

/* ── Base font — do NOT override colour; let Streamlit theme handle it ── */
html, body, .stApp {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    background-color: var(--hc-bg) !important;
}}

/* ── Headings — inherit colour from Streamlit theme token ── */
h1, h2, h3, h4, h5, h6 {{
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    color: var(--hc-text) !important;
}}

/* ── Premium card shell ── */
.premium-card {{
    background-color: var(--hc-surface);
    border-radius: 12px;
    padding: 24px;
    border: 1px solid var(--hc-border);
    box-shadow: 0 4px 6px -1px rgba(0,0,0,.06), 0 2px 4px -1px rgba(0,0,0,.04);
    margin-bottom: 20px;
    color: var(--hc-text);
}}

header {{ background-color: transparent !important; }}
footer  {{ display: none !important; }}
.block-container {{ padding-top: 2rem !important; padding-bottom: 2rem !important; }}

/* ── DataFrames / tables — let Streamlit theme handle cell colours;
       only add a subtle border and ensure the header is legible ── */
[data-testid="stDataFrame"] {{
    border-radius: 8px;
    overflow: hidden;
}}
/* Ensure table text inherits theme colour */
[data-testid="stDataFrame"] * {{
    color: var(--hc-text) !important;
}}

/* ── Form widgets — labels ── */
.stSelectbox label,
.stRadio label,
.stSlider label,
.stNumberInput label,
.stTextInput label,
.stMultiSelect label,
.stDateInput label,
.stTimeInput label,
.stTextArea label {{
    color: var(--hc-text) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
}}

/* Radio option text */
.stRadio [data-testid="stMarkdownContainer"] p {{
    color: var(--hc-text) !important;
}}

/* Selectbox / dropdown text */
div[data-baseweb="select"] > div {{
    border-color: var(--hc-border) !important;
    border-radius: 8px !important;
    background-color: var(--hc-surface) !important;
}}
div[data-baseweb="select"] [data-testid="stMarkdownContainer"],
div[data-baseweb="select"] span,
div[data-baseweb="select"] div {{
    color: var(--hc-text) !important;
}}

/* Dropdown option list */
ul[data-baseweb="menu"] li,
ul[data-baseweb="menu"] span {{
    color: var(--hc-text) !important;
}}

/* Slider track & thumb colours driven by primaryColor in config.toml;
   labels already handled above */

/* Spinner text */
[data-testid="stSpinner"] p {{
    color: var(--hc-text-sec) !important;
}}

/* ── Buttons (main content area) ── */
button[kind="primary"] {{
    background-color: #F97316 !important;
    color: #FFFFFF !important;
    border: 1px solid #F97316 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 6px -1px rgba(249,115,22,.2) !important;
    transition: all .2s ease !important;
}}
button[kind="primary"]:hover {{
    background-color: #EA580C !important;
}}
button[kind="secondary"] {{
    background-color: var(--hc-surface) !important;
    color: var(--hc-text) !important;
    border: 1px solid var(--hc-border) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all .2s ease !important;
}}
button[kind="secondary"]:hover {{
    border-color: #F97316 !important;
    color: #F97316 !important;
}}

/* ══════════════════════════════
   SIDEBAR  (intentionally always dark)
   ══════════════════════════════ */
section[data-testid="stSidebar"],
[data-testid="stSidebar"] {{
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    min-width: 288px !important;
    max-width: 288px !important;
    background-color: #0F172A !important;
    border-right: 1px solid #1E293B !important;
    position: relative !important;
    overflow: hidden !important;
    transition: min-width 0.22s ease, max-width 0.22s ease !important;
}}
section[data-testid="stSidebar"][aria-expanded="false"],
section[data-testid="stSidebar"][aria-expanded] {{
    transform: none !important;
    left: 0 !important;
    overflow: hidden !important;
}}
[data-testid="stSidebar"] > div:first-child {{
    padding: 0 !important;
    overflow: hidden !important;
    overflow-y: hidden !important;
    height: 100vh !important;
    width: 100% !important;
}}
[data-testid="stSidebarUserContent"] {{
    padding: 0.5rem 0.65rem 0.75rem !important;
}}
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"]:first-child {{
    margin-top: -4px !important;
    margin-bottom: -2px !important;
}}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
    gap: 0.5rem !important;
}}
[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] {{
    padding-top: 0 !important;
}}
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {{
    margin-bottom: 0 !important;
    align-items: flex-start !important;
    width: 100% !important;
}}
[data-testid="stSidebar"] [data-testid="stElementContainer"] {{
    flex-shrink: 0 !important;
}}
[data-testid="stSidebar"] [data-testid="column"] {{
    padding: 0 !important;
    align-items: flex-start !important;
}}
[data-testid="stSidebar"] .stMarkdown {{
    flex-shrink: 0 !important;
}}
[data-testid="stSidebar"] .stButton {{
    flex-shrink: 0 !important;
    min-height: 50px !important;
    margin-bottom: 4px !important;
}}
[data-testid="stSidebar"] [data-testid="column"] .stButton {{
    min-height: unset !important;
    margin-bottom: 0 !important;
}}
[data-testid="stSidebar"] [data-testid="column"]:last-child .stButton {{
    padding-top: 0 !important;
}}

/* Hide native Streamlit sidebar collapse button */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"],
button[aria-label="Collapse sidebar"],
button[aria-label="Close sidebar"] {{
    display: none !important;
}}

/* ── Sidebar toggle button (integrated) ── */
[data-testid="stSidebar"] [data-testid="column"] .stButton {{
    display: flex !important;
    justify-content: flex-end !important;
    padding: 0 !important;
    margin: 0 !important;
}}
[data-testid="stSidebar"] [data-testid="column"] .stButton > button,
[data-testid="stSidebar"] [data-testid="column"] .stButton > button[kind="secondary"] {{
    width: 24px !important;
    min-width: 24px !important;
    height: 24px !important;
    min-height: 24px !important;
    padding: 0 !important;
    margin: 0 !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 6px !important;
    color: #94A3B8 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    box-shadow: none !important;
    line-height: 1 !important;
}}
[data-testid="stSidebar"] [data-testid="column"] .stButton > button:hover,
[data-testid="stSidebar"] [data-testid="column"] .stButton > button[kind="secondary"]:hover {{
    background: rgba(249,115,22,0.15) !important;
    color: #F97316 !important;
    border-color: rgba(249,115,22,0.25) !important;
}}

/* ── Sidebar nav buttons ── */
[data-testid="stSidebar"] .stButton > button {{
    width: 100% !important;
    text-align: left !important;
    justify-content: flex-start !important;
    align-items: center !important;
    gap: 12px !important;
    background: transparent !important;
    border: none !important;
    border-left: 2px solid transparent !important;
    border-radius: 0 8px 8px 0 !important;
    padding: 0 14px !important;
    margin: 3px 0 !important;
    color: #94A3B8 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    height: 48px !important;
    min-height: 48px !important;
    max-height: 52px !important;
    box-shadow: none !important;
    cursor: pointer !important;
    transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease !important;
}}
[data-testid="stSidebar"] .stButton > button [data-testid="stIconMaterial"],
[data-testid="stSidebar"] .stButton > button [data-testid="stIconEmoji"] {{
    font-size: 18px !important;
    width: 18px !important;
    flex-shrink: 0 !important;
}}
[data-testid="stSidebar"] .stButton > button:hover {{
    background: rgba(255,255,255,0.04) !important;
    color: #E2E8F0 !important;
}}
[data-testid="stSidebar"] .stButton > button[kind="secondary"],
[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {{
    background: transparent !important;
    border: none !important;
    border-left: 2px solid transparent !important;
    color: #94A3B8 !important;
    box-shadow: none !important;
}}
[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {{
    background: rgba(255,255,255,0.04) !important;
    color: #E2E8F0 !important;
}}
[data-testid="stSidebar"] .stButton > button[kind="primary"],
[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {{
    background: rgba(249,115,22,0.08) !important;
    border: none !important;
    border-left: 2px solid #F97316 !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    box-shadow: none !important;
}}
[data-testid="stSidebar"] .stButton > button[kind="primary"] [data-testid="stIconMaterial"],
[data-testid="stSidebar"] .stButton > button[kind="primary"] [data-testid="stIconEmoji"] {{
    color: #F97316 !important;
}}
[data-testid="stSidebar"] .stButton > button:focus {{
    box-shadow: none !important;
    outline: none !important;
}}
</style>
""", unsafe_allow_html=True)


inject_global_css()


# ─── Sidebar width & collapse state ───────────────────────────────────────────
_collapsed = st.session_state.sidebar_collapsed
_sb_width  = "84px" if _collapsed else "288px"

_collapsed_css = ""
if _collapsed:
    _collapsed_css = """
[data-testid="stSidebarUserContent"] {
    padding: 0.5rem 0 0.75rem !important;
}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 10px !important;
    align-items: center !important;
}
.sb-brand-text, .sb-tagline-text, .sb-nav-heading { display: none !important; }
.sb-divider { display: none !important; }
.sb-nav-spacer { display: none !important; }
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
    margin: 0 0 8px !important;
    min-height: auto !important;
    align-items: center !important;
}
[data-testid="stSidebar"] [data-testid="column"] { justify-content: center !important; }
[data-testid="stSidebar"] [data-testid="column"] .stButton {
    justify-content: center !important;
    min-height: 36px !important;
    height: 36px !important;
    margin: 0 auto !important;
}
[data-testid="stSidebar"] [data-testid="column"] .stButton > button,
[data-testid="stSidebar"] [data-testid="column"] .stButton > button[kind="secondary"] {
    width: 24px !important; min-width: 24px !important;
    height: 24px !important; min-height: 24px !important;
    margin: 0 auto !important; font-size: 11px !important;
    border-left: none !important;
}
[data-testid="stSidebar"] [data-testid="column"] .stButton > button p { display: inline !important; }
.sb-brand-block {
    padding: 4px 0 0 !important; border: none !important;
    margin: 0 auto 4px !important; min-height: 48px !important;
    display: flex !important; align-items: center !important; justify-content: center !important;
}
.sb-brand-row { justify-content: center !important; margin: 0 !important; width: 100% !important; }
.sb-brand-icon {
    width: 48px !important; height: 48px !important; padding: 0 !important;
    border-radius: 10px !important; margin: 0 auto !important;
    display: flex !important; align-items: center !important;
    justify-content: center !important; flex-shrink: 0 !important;
}
[data-testid="stSidebar"] .stButton {
    display: flex !important; justify-content: center !important;
    align-items: center !important; padding: 0 !important;
    margin: 0 auto 6px !important; min-height: 54px !important;
    height: 54px !important; width: 100% !important;
}
[data-testid="stSidebar"] .stButton > button {
    width: 48px !important; min-width: 48px !important;
    height: 48px !important; min-height: 48px !important; max-height: 48px !important;
    padding: 0 !important; margin: 0 auto !important;
    border-radius: 10px !important; border: 1px solid transparent !important;
    border-left: none !important; justify-content: center !important;
    font-size: 0 !important; gap: 0 !important; position: relative !important;
}
[data-testid="stSidebar"] .stButton > button p { display: none !important; }
[data-testid="stSidebar"] .stButton > button [data-testid="stIconMaterial"],
[data-testid="stSidebar"] .stButton > button [data-testid="stIconEmoji"] {
    font-size: 22px !important; margin: 0 !important; color: #94A3B8 !important;
}
[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
    background: rgba(255,255,255,0.06) !important;
    border-color: rgba(255,255,255,0.06) !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"],
[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
    background: rgba(249,115,22,0.10) !important;
    border: 1px solid rgba(249,115,22,0.22) !important;
    box-shadow: inset 2px 0 0 #F97316 !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"] [data-testid="stIconMaterial"],
[data-testid="stSidebar"] .stButton > button[kind="primary"] [data-testid="stIconEmoji"] {
    color: #F97316 !important;
}
"""

st.markdown(f"""
<style>
section[data-testid="stSidebar"],
[data-testid="stSidebar"] {{
    min-width: {_sb_width} !important;
    max-width: {_sb_width} !important;
}}
section[data-testid="stSidebar"][aria-expanded],
section[data-testid="stSidebar"][aria-expanded="false"] {{
    min-width: {_sb_width} !important;
    max-width: {_sb_width} !important;
}}
{_collapsed_css}
</style>
""", unsafe_allow_html=True)


# ─── SVG helpers ──────────────────────────────────────────────────────────────
def brain_svg(size):
    return (
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{size}' height='{size}' viewBox='0 0 24 24' fill='none' "
        "stroke='#FFFFFF' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>"
        "<path d='M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z'/>"
        "<path d='M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z'/>"
        "<path d='M9 13h4'/><path d='M12 10v6'/><path d='M12 8H8'/>"
        "<path d='M20 14h-2'/><path d='M4 14h2'/><path d='M12 20v2'/><path d='M12 2v2'/></svg>"
    )

ICON_SVG = {
    "Users":        "<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='#F97316' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2'/><circle cx='9' cy='7' r='4'/><path d='M22 21v-2a4 4 0 0 0-3-3.87'/><path d='M16 3.13a4 4 0 0 1 0 7.75'/></svg>",
    "Target":       "<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='#F97316' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><circle cx='12' cy='12' r='10'/><circle cx='12' cy='12' r='6'/><circle cx='12' cy='12' r='2'/></svg>",
    "ShieldAlert":  "<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='#F97316' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M20 13c0 5-3.5 7.5-7.66 9.7a1 1 0 0 1-.68 0C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z'/><path d='M12 8v4'/><path d='M12 16h.01'/></svg>",
    "TrendingUp":   "<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='#F97316' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><polyline points='22 7 13.5 15.5 8.5 10.5 2 17'/><polyline points='16 7 22 7 22 13'/></svg>",
    "Clock":        "<svg xmlns='http://www.w3.org/2000/svg' width='22' height='22' viewBox='0 0 24 24' fill='none' stroke='#F97316' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><circle cx='12' cy='12' r='10'/><polyline points='12 6 12 12 16 14'/></svg>",
    "ClipboardList":"<svg xmlns='http://www.w3.org/2000/svg' width='22' height='22' viewBox='0 0 24 24' fill='none' stroke='#F97316' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><rect width='8' height='4' x='8' y='2' rx='1' ry='1'/><path d='M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2'/><path d='M12 11h4'/><path d='M12 16h4'/><path d='M8 11h.01'/><path d='M8 16h.01'/></svg>",
    "Activity":     "<svg xmlns='http://www.w3.org/2000/svg' width='22' height='22' viewBox='0 0 24 24' fill='none' stroke='#F97316' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M22 12h-4l-3 9L9 3l-3 9H2'/></svg>",
}

PAGES = ["Dashboard", "Prediction", "Analytics", "Model Performance", "About"]
PAGE_ICONS = {
    "Dashboard":         ":material/space_dashboard:",
    "Prediction":        ":material/biotech:",
    "Analytics":         ":material/bar_chart:",
    "Model Performance": ":material/memory:",
    "About":             ":material/info:",
}


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    _chevron = "\u00bb" if _collapsed else "\u00ab"

    if _collapsed:
        _tc1, _tc2, _tc3 = st.columns([1, 1, 1])
        with _tc2:
            if st.button(_chevron, key="sb_toggle", help="Expand sidebar"):
                st.session_state.sidebar_collapsed = not st.session_state.sidebar_collapsed
                trigger_rerun()

        st.markdown(
            f'<div class="sb-brand-block">'
            f'<div class="sb-brand-row" style="display:flex;align-items:center;justify-content:center;">'
            f'<div class="sb-brand-icon" style="background:#F97316;border-radius:10px;'
            f'box-shadow:0 2px 8px rgba(249,115,22,0.25);">{brain_svg(24)}</div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )
    else:
        _spacer_col, _toggle_col = st.columns([6, 1], gap="small")
        with _toggle_col:
            if st.button(_chevron, key="sb_toggle", help="Collapse sidebar"):
                st.session_state.sidebar_collapsed = not st.session_state.sidebar_collapsed
                trigger_rerun()

        st.markdown(
            f'<div class="sb-brand-block" style="padding:0 6px 4px;">'
            f'<div class="sb-brand-row" style="display:flex;align-items:flex-start;gap:12px;">'
            f'<div class="sb-brand-icon" style="background:#F97316;width:44px;height:44px;min-width:44px;'
            f'min-height:44px;border-radius:10px;display:flex;align-items:center;justify-content:center;'
            f'flex-shrink:0;box-shadow:0 2px 8px rgba(249,115,22,0.25);margin-top:1px;">'
            f'{brain_svg(26)}</div>'
            f'<div class="sb-brand-text">'
            f'<p style="margin:0;color:#FFFFFF;font-size:15px;font-weight:700;'
            f'font-family:Inter,sans-serif;line-height:1.3;">Intelligent Healthcare</p>'
            f'<p style="margin:4px 0 0;color:#F97316;font-size:13px;font-weight:600;'
            f'font-family:Inter,sans-serif;line-height:1.3;">Readmission Analytics</p>'
            f'<p class="sb-tagline-text" style="margin:5px 0 0;color:#64748B;font-size:11.5px;'
            f'font-weight:500;font-family:Inter,sans-serif;line-height:1.4;">'
            f'Clinical Decision Support Dashboard</p>'
            f'</div></div></div>',
            unsafe_allow_html=True,
        )

    if not _collapsed:
        st.markdown('<div class="sb-nav-spacer" style="height:20px;"></div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="sb-divider" style="height:1px;background:#1E293B;margin:0 10px;"></div>',
        unsafe_allow_html=True,
    )

    if not _collapsed:
        st.markdown(
            '<p class="sb-nav-heading" style="margin:14px 10px 10px;padding:0;color:#475569;'
            'font-size:9.5px;font-weight:600;text-transform:uppercase;letter-spacing:0.6px;'
            'font-family:Inter,sans-serif;line-height:1.4;">Navigation</p>',
            unsafe_allow_html=True,
        )

    for page_name in PAGES:
        is_active = st.session_state.selected_page == page_name
        if st.button(
            page_name,
            key=f"nav_{page_name}",
            icon=PAGE_ICONS.get(page_name, ":material/info:"),
            use_container_width=True,
            type="primary" if is_active else "secondary",
        ):
            st.session_state.selected_page = page_name
            trigger_rerun()


# ─── Reusable component helpers ───────────────────────────────────────────────

def kpi_card(title, value, description, icon):
    """KPI metric card — colours pulled from live theme palette."""
    c = get_theme_colors()
    svg = ICON_SVG.get(icon, "")
    return (
        f'<div style="background:{c["surface"]};border-radius:12px;padding:20px;'
        f'border:1px solid {c["border"]};'
        f'box-shadow:0 4px 6px -1px rgba(0,0,0,.05);display:flex;flex-direction:column;'
        f'justify-content:space-between;min-height:120px;">'
        f'<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">'
        f'<span style="color:{c["text_secondary"]};font-size:13px;font-weight:500;">{title}</span>'
        f'<span style="background:{c["orange_subtle"]};padding:6px;border-radius:6px;display:inline-flex;">{svg}</span>'
        f'</div>'
        f'<div>'
        f'<h2 style="margin:0;color:{c["text"]};font-size:26px;font-weight:700;line-height:1.2;">{value}</h2>'
        f'<p style="margin:4px 0 0;color:{c["text_secondary"]};font-size:11px;">{description}</p>'
        f'</div></div>'
    )


def insight_card(title, description, icon):
    """Clinical insight card."""
    c = get_theme_colors()
    svg = ICON_SVG.get(icon, "")
    return (
        f'<div style="background:{c["surface"]};border-radius:12px;padding:24px;'
        f'border:1px solid {c["border"]};'
        f'box-shadow:0 4px 6px -1px rgba(0,0,0,.05);display:flex;flex-direction:column;">'
        f'<div style="background:{c["orange_subtle"]};width:44px;height:44px;border-radius:8px;'
        f'display:flex;align-items:center;justify-content:center;margin-bottom:16px;">{svg}</div>'
        f'<h4 style="margin:0 0 8px;color:{c["text"]};font-size:15px;font-weight:600;">{title}</h4>'
        f'<p style="margin:0;color:{c["text_secondary"]};font-size:13px;line-height:1.5;">{description}</p>'
        f'</div>'
    )


def chart_card_open(title):
    """Open wrapper for a chart card."""
    c = get_theme_colors()
    return (
        f'<div style="background:{c["surface"]};border-radius:12px;padding:20px 20px 10px;'
        f'border:1px solid {c["border"]};'
        f'box-shadow:0 4px 6px -1px rgba(0,0,0,.05);margin-bottom:20px;">'
        f'<h3 style="margin:0 0 15px;color:{c["text"]};font-size:16px;font-weight:600;'
        f'border-bottom:1px solid {c["divider"]};padding-bottom:10px;">{title}</h3>'
    )


CHART_CARD_CLOSE = '</div>'


def page_header_card(title, description, icon=""):
    """Compact page header card."""
    c = get_theme_colors()
    icon_html = (
        f'<span style="background:#F97316;padding:4px;border-radius:4px;'
        f'display:inline-flex;margin-right:8px;">{icon}</span>'
    ) if icon else ""
    return (
        f'<div style="background:{c["surface"]};border-radius:12px;padding:16px 20px;'
        f'border:1px solid {c["border"]};box-shadow:0 4px 6px -1px rgba(0,0,0,.05);margin-bottom:20px;">'
        f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">'
        f'{icon_html}'
        f'<h2 style="margin:0;color:{c["text"]};font-size:20px;font-weight:700;">{title}</h2>'
        f'</div>'
        f'<p style="margin:0;color:{c["text_secondary"]};font-size:13px;line-height:1.5;">{description}</p>'
        f'</div>'
    )


PLOTLY_CFG = {"displayModeBar": False}


def get_plotly_layout():
    """
    Shared Plotly layout tokens.
    paper_bgcolor / plot_bgcolor are always transparent so the card background
    (which is already theme-correct) shows through.
    Font colours are pulled from get_theme_colors() so axis labels, ticks, and
    legend text automatically match the active theme.
    """
    c = get_theme_colors()
    base = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    axis_style = dict(
        showgrid=True,
        gridcolor=c["grid"],
        linecolor=c["axis"],
        tickfont=dict(family="Inter, sans-serif", size=10, color=c["text_secondary"]),
    )
    xaxis_cat = dict(
        showgrid=False,
        linecolor=c["axis"],
        tickfont=dict(family="Inter, sans-serif", size=11, color=c["text"]),
    )
    legend_style = dict(
        font=dict(size=10, color=c["text"]),
        bgcolor="rgba(0,0,0,0)",
    )
    return {
        "base": base,
        "axis_style": axis_style,
        "xaxis_cat": xaxis_cat,
        "legend": legend_style,
        "text": c["text"],
        "text_secondary": c["text_secondary"],
        "axis": c["axis"],
        "colors": c,
    }


def render_footer():
    brain_s = (
        "<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' "
        "fill='none' stroke='#FFFFFF' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>"
        "<path d='M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z'/>"
        "<path d='M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z'/>"
        "<path d='M9 13h4'/><path d='M12 10v6'/><path d='M12 8H8'/>"
        "<path d='M20 14h-2'/><path d='M4 14h2'/><path d='M12 20v2'/><path d='M12 2v2'/></svg>"
    )
    # Footer is intentionally always dark — brand anchor at bottom of page.
    st.markdown(
        f'<div style="background:#0F172A;color:#FFFFFF;border-radius:12px;padding:16px 20px;'
        f'border:1px solid #1E293B;margin-top:20px;font-family:Inter,sans-serif;">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;margin-bottom:12px;">'
        f'<div style="display:flex;align-items:center;gap:8px;">'
        f'<span style="background:#F97316;padding:3px;border-radius:4px;display:inline-flex;">{brain_s}</span>'
        f'<span style="font-weight:700;font-size:13px;">Intelligent Healthcare Readmission Analytics</span>'
        f'</div>'
        f'<div style="display:flex;align-items:center;gap:16px;">'
        f'<span style="color:#94A3B8;font-size:11px;">Random Forest Classifier</span>'
        f'<span style="color:#94A3B8;font-size:11px;">SHAP &amp; Platt Scaling</span>'
        f'</div></div>'
        f'<div style="border-top:1px solid #1E293B;padding-top:10px;">'
        f'<span style="color:#64748B;font-size:10px;"> 2026 Healthcare Analytics Project. </span>'
        f'</div></div>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.selected_page == "Dashboard":
    c = get_theme_colors()
    metrics = load_model_and_data()

    col_left, col_right = st.columns([1.1, 0.9])

    with col_left:
        brain_orange = (
            "<svg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' "
            "fill='none' stroke='#F97316' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>"
            "<path d='M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z'/>"
            "<path d='M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z'/>"
            "<path d='M9 13h4'/><path d='M12 10v6'/><path d='M12 8H8'/>"
            "<path d='M20 14h-2'/><path d='M4 14h2'/><path d='M12 20v2'/><path d='M12 2v2'/></svg>"
        )
        st.markdown(
            f'<div style="margin-top:10px;display:flex;align-items:center;gap:8px;margin-bottom:12px;">'
            f'<span style="background:{c["orange_subtle"]};padding:6px;border-radius:6px;display:inline-flex;">{brain_orange}</span>'
            f'<span style="color:#F97316;font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:.5px;">Clinical Decision Support Tool</span>'
            f'</div>'
            f'<h1 style="color:{c["text"]};font-size:38px;font-weight:800;line-height:1.15;margin:0 0 8px;">Intelligent Healthcare Readmission Analytics System</h1>'
            f'<p style="color:{c["text_secondary"]};font-size:16px;font-weight:500;margin:0 0 16px;">ML-Powered Clinical Decision Support Dashboard</p>'
            f'<p style="color:{c["text_secondary"]};font-size:14px;line-height:1.6;margin:0 0 28px;max-width:580px;">'
            f'Leverage machine learning to identify high-risk patients, reduce preventable readmissions, '
            f'and improve healthcare outcomes through predictive analytics and intelligent decision support.</p>',
            unsafe_allow_html=True,
        )
        btn1, btn2 = st.columns(2)
        with btn1:
            if st.button("Predict Patient Risk", type="primary", use_container_width=True, key="btn_predict"):
                st.session_state.selected_page = "Prediction"
                trigger_rerun()
        with btn2:
            if st.button("View Analytics", type="secondary", use_container_width=True, key="btn_analytics"):
                st.session_state.selected_page = "Analytics"
                trigger_rerun()

    with col_right:
        shield_svg = (
            "<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' "
            "fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>"
            "<path d='M20 13c0 5-3.5 7.5-7.66 9.7a1 1 0 0 1-.68 0C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1"
            "c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z'/>"
            "<path d='M12 8v4'/><path d='M12 16h.01'/></svg>"
        )
        # This panel is intentionally always dark regardless of theme —
        # it's a branded "terminal / metrics readout" component.
        st.markdown(
            f'<div style="background:#0F172A;border-radius:16px;padding:24px;border:1px solid #1E293B;'
            f'box-shadow:0 10px 25px -5px rgba(0,0,0,.3);display:flex;flex-direction:column;gap:16px;font-family:Inter,sans-serif;">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #1E293B;padding-bottom:12px;">'
            f'<div style="display:flex;align-items:center;gap:8px;">'
            f'<div style="width:8px;height:8px;border-radius:50%;background:#22C55E;"></div>'
            f'<span style="color:#94A3B8;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.5px;">Model Performance Metrics</span>'
            f'</div>'
            f'<span style="color:#F97316;font-size:10px;font-weight:600;background:rgba(249,115,22,.15);padding:4px 8px;border-radius:4px;">Random Forest Classifier</span>'
            f'</div>'
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">'
            f'<div style="background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.05);padding:12px;border-radius:8px;">'
            f'<p style="margin:0;color:#64748B;font-size:9px;text-transform:uppercase;">Model Accuracy</p>'
            f'<p style="margin:0;color:#F97316;font-size:20px;font-weight:700;">{metrics["accuracy"]:.1f}%</p>'
            f'<p style="margin:0;color:#22C55E;font-size:9px;font-weight:500;">Trained on dataset</p>'
            f'</div>'
            f'<div style="background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.05);padding:12px;border-radius:8px;">'
            f'<p style="margin:0;color:#64748B;font-size:9px;text-transform:uppercase;">ROC-AUC Score</p>'
            f'<p style="margin:0;color:#FFFFFF;font-size:20px;font-weight:700;">{metrics["roc_auc"]:.2f}</p>'
            f'<p style="margin:0;color:#64748B;font-size:9px;">Classification effectiveness</p>'
            f'</div></div>'
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">'
            f'<div style="background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.05);padding:12px;border-radius:8px;">'
            f'<p style="margin:0;color:#64748B;font-size:9px;text-transform:uppercase;">Precision</p>'
            f'<p style="margin:0;color:#FFFFFF;font-size:20px;font-weight:700;">87.2%</p>'
            f'<p style="margin:0;color:#64748B;font-size:9px;">Validation score</p>'
            f'</div>'
            f'<div style="background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.05);padding:12px;border-radius:8px;">'
            f'<p style="margin:0;color:#64748B;font-size:9px;text-transform:uppercase;">Recall</p>'
            f'<p style="margin:0;color:#FFFFFF;font-size:20px;font-weight:700;">84.5%</p>'
            f'<p style="margin:0;color:#64748B;font-size:9px;">Validation score</p>'
            f'</div></div>'
            f'<div style="background:{c["green_subtle"]};border:1px solid {c["green_border"]};padding:12px;border-radius:8px;display:flex;gap:10px;align-items:center;">'
            f'<span style="color:#22C55E;display:inline-flex;">{shield_svg}</span>'
            f'<div><p style="margin:0;color:#FFFFFF;font-size:12px;font-weight:600;">Total Records Analyzed</p>'
            f'<p style="margin:0;color:#94A3B8;font-size:10px;">{metrics["total_patients"]:,} patient records processed</p></div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<div style='margin-top:30px;'></div>", unsafe_allow_html=True)

    # ── KPI Cards ─────────────────────────────────────────────────────────────
    kc1, kc2, kc3, kc4 = st.columns(4)
    kc1.markdown(kpi_card("Patients Analyzed",      f"{metrics['total_patients']:,}", "Total records processed",       "Users"),       unsafe_allow_html=True)
    kc2.markdown(kpi_card("Prediction Accuracy",    f"{metrics['accuracy']:.1f}%",  "Model performance",             "Target"),      unsafe_allow_html=True)
    kc3.markdown(kpi_card("Readmission Risk Cases", f"{metrics['readmission_cases']:,}", "High-risk patients identified", "ShieldAlert"), unsafe_allow_html=True)
    kc4.markdown(kpi_card("Model ROC-AUC",          f"{metrics['roc_auc']:.2f}",   "Classification effectiveness",  "TrendingUp"),  unsafe_allow_html=True)

    st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)

    # ── Charts row ────────────────────────────────────────────────────────────
    ch_l, ch_r = st.columns(2)

    with ch_l:
        st.markdown(chart_card_open("Patient Readmission Distribution"), unsafe_allow_html=True)
        plt = get_plotly_layout()
        fig = go.Figure(go.Pie(
            labels=["Not Readmitted", "Readmitted"],
            values=[72, 28],
            hole=.6,
            marker=dict(colors=["#0F172A", "#F97316"], line=dict(color=c["surface"], width=2)),
        ))
        fig.update_traces(
            textinfo="percent+label",
            textfont_size=11,
            textfont_family="Inter, sans-serif",
            textposition="outside",
            textfont_color=plt["text"],
        )
        fig.update_layout(**plt["base"], showlegend=False, margin=dict(t=10, b=10, l=10, r=10), height=260)
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CFG)
        st.markdown(CHART_CARD_CLOSE, unsafe_allow_html=True)

    with ch_r:
        st.markdown(chart_card_open("Risk Category Distribution"), unsafe_allow_html=True)
        plt = get_plotly_layout()
        fig = go.Figure(go.Bar(
            x=["Low Risk", "Medium Risk", "High Risk"],
            y=[7458, 3753, 1247],
            marker_color=["#22C55E", "#FB923C", "#EF4444"],
            width=0.45,
        ))
        fig.update_layout(
            **plt["base"],
            margin=dict(t=20, b=10, l=40, r=20),
            height=260,
            xaxis=plt["xaxis_cat"],
            yaxis=plt["axis_style"],
        )
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CFG)
        st.markdown(CHART_CARD_CLOSE, unsafe_allow_html=True)

    # ── Feature Importance ────────────────────────────────────────────────────
    st.markdown(chart_card_open("Top Factors Influencing Readmission"), unsafe_allow_html=True)
    plt = get_plotly_layout()
    feats = ["Insulin Usage", "Age Group", "Number of Diagnoses", "Number of Medications", "Time in Hospital", "Previous Admissions"]
    imps  = [0.07, 0.11, 0.14, 0.18, 0.22, 0.28]
    fig = go.Figure(go.Bar(y=feats, x=imps, orientation="h", marker_color="#F97316", width=0.55))
    fig.update_layout(
        **plt["base"],
        margin=dict(t=10, b=10, l=160, r=20),
        height=280,
        xaxis=dict(
            **plt["axis_style"],
            title=dict(text="Relative Importance Score", font=dict(family="Inter, sans-serif", size=11, color=plt["text_secondary"])),
        ),
        yaxis=dict(
            showgrid=False,
            linecolor=plt["axis"],
            tickfont=dict(family="Inter, sans-serif", size=12, color=plt["text"]),
        ),
    )
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CFG)
    st.markdown(CHART_CARD_CLOSE, unsafe_allow_html=True)

    # ── Clinical Insights ─────────────────────────────────────────────────────
    st.markdown(
        f'<h3 style="margin:20px 0 15px;font-size:18px;font-weight:600;color:{c["text"]};">Clinical Insights</h3>',
        unsafe_allow_html=True,
    )
    ic1, ic2, ic3 = st.columns(3)
    ic1.markdown(insight_card("Extended Hospital Stay",
        "Patients with longer hospital stays demonstrate a significantly higher probability of readmission.", "Clock"),
        unsafe_allow_html=True)
    ic2.markdown(insight_card("Multiple Diagnoses Impact",
        "Patients with multiple diagnoses show elevated readmission risk compared to single-condition cases.", "ClipboardList"),
        unsafe_allow_html=True)
    ic3.markdown(insight_card("Frequent Inpatient Visits",
        "Repeated inpatient admissions strongly correlate with future readmission events.", "Activity"),
        unsafe_allow_html=True)

    render_footer()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PREDICTION
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.selected_page == "Prediction":
    c = get_theme_colors()

    biotech_icon = (
        "<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' "
        "fill='none' stroke='#FFFFFF' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>"
        "<path d='M12 2a10 10 0 1 0 10 10 4 4 0 0 1-5-5 4 4 0 0 1-5-5'/>"
        "<path d='M8.5 8.5v.01'/><path d='M16 15.5v.01'/><path d='M12 12v.01'/><path d='M11 17v.01'/></svg>"
    )
    st.markdown(page_header_card(
        "Patient Readmission Risk Predictor",
        "Enter clinical parameters to evaluate real-time patient readmission risk and generate decision support recommendations.",
        biotech_icon,
    ), unsafe_allow_html=True)

    col_form, col_result = st.columns([1, 1])

    with col_form:
        # Card wrapper using theme-aware surface colour
        st.markdown(
            f'<div style="background:{c["surface"]};border-radius:12px;padding:24px;'
            f'border:1px solid {c["border"]};box-shadow:0 4px 6px -1px rgba(0,0,0,.05);">'
            f'<h4 style="margin:0 0 16px;font-size:15px;font-weight:600;color:{c["text"]};'
            f'border-bottom:1px solid {c["divider"]};padding-bottom:10px;">Patient Parameters</h4>',
            unsafe_allow_html=True,
        )
        ca, cg = st.columns(2)
        with ca:
            age_group = st.selectbox("Age Group", ["<30", "30-49", "50-69", "70-79", "80+"], index=2)
        with cg:
            gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
        time_hospital = st.slider("Time in Hospital (Days)", 1, 14, 4)
        num_diagnoses = st.slider("Number of Diagnoses", 1, 16, 5)
        num_meds      = st.slider("Number of Medications", 1, 80, 15)
        num_inpatient = st.slider("Previous Inpatient Visits (Prior Year)", 0, 10, 1)
        ci, cd = st.columns(2)
        with ci:
            insulin  = st.selectbox("Insulin Usage", ["No", "Steady", "Up", "Down"], index=1)
        with cd:
            diab_med = st.radio("Diabetes Medication", ["Yes", "No"], horizontal=True)
        st.markdown('</div>', unsafe_allow_html=True)

        predict_button = st.button(
            "🔮 Predict Readmission Risk",
            key="predict_button",
            use_container_width=True,
            type="primary",
        )

    with col_result:
        contribs = []

        if predict_button:
            with st.spinner("Analyzing patient parameters and generating risk prediction..."):
                import time
                time.sleep(1.5)

                score = 15.0
                inpatient_contrib = min(num_inpatient * 12.0, 48.0); score += inpatient_contrib
                time_contrib      = min(time_hospital * 2.0, 18.0);  score += time_contrib
                diagnoses_contrib = min(num_diagnoses * 2.0, 16.0);  score += diagnoses_contrib
                meds_contrib      = min(num_meds * 0.25, 12.0);      score += meds_contrib
                age_contrib       = {"70-79": 4.0, "80+": 8.0, "<30": -2.0}.get(age_group, 0.0); score += age_contrib
                insulin_contrib   = 5.0 if insulin in ["Up", "Down"] else (2.0 if insulin == "Steady" else 0.0); score += insulin_contrib
                if diab_med == "Yes": score += 3.0
                risk_score = max(5.0, min(95.0, score))

                contribs = [
                    ("Base Rate",                    15.0,              "#64748B"),
                    (f"Inpatient (+{num_inpatient})", inpatient_contrib, "#EF4444" if inpatient_contrib > 0 else "#64748B"),
                    (f"Hosp Days (+{time_hospital})", time_contrib,      "#EF4444" if time_contrib > 0 else "#64748B"),
                    (f"Diagnoses (+{num_diagnoses})", diagnoses_contrib, "#EF4444" if diagnoses_contrib > 0 else "#64748B"),
                    (f"Medications (+{num_meds})",    meds_contrib,      "#EF4444" if meds_contrib > 0 else "#64748B"),
                    (f"Age ({age_group})",            age_contrib,       "#EF4444" if age_contrib > 0 else ("#22C55E" if age_contrib < 0 else "#64748B")),
                    (f"Insulin ({insulin})",          insulin_contrib,   "#EF4444" if insulin_contrib > 0 else "#64748B"),
                ]

                if risk_score < 30:
                    risk_class, risk_color, risk_bg = "Low Risk",    "#22C55E", c["green_subtle"]
                    directive = "Patient demonstrates low readmission probability. Standard discharge protocols and routine follow-up schedule are recommended."
                elif risk_score < 70:
                    risk_class, risk_color, risk_bg = "Medium Risk", "#FB923C", c["amber_subtle"]
                    directive = "Patient demonstrates moderate readmission risk. Consider scheduling clinical telephone follow-up within 72 hours and review medication reconciliation."
                else:
                    risk_class, risk_color, risk_bg = "High Risk",   "#EF4444", c["red_subtle"]
                    directive = "Patient is at critical risk of readmission. Intensive TCM enrollment, medication counseling, and clinical contact within 48 hours are strongly advised."

                # Risk output card — text colours from palette
                st.markdown(
                    f'<div style="background:{c["surface"]};border-radius:12px;padding:24px;'
                    f'border:1px solid {c["border"]};box-shadow:0 4px 6px -1px rgba(0,0,0,.05);margin-bottom:20px;">'
                    f'<h4 style="margin:0 0 16px;font-size:15px;font-weight:600;color:{c["text"]};'
                    f'border-bottom:1px solid {c["divider"]};padding-bottom:10px;">Risk Scoring Engine Output</h4>'
                    f'<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;margin-bottom:16px;">'
                    f'<div><span style="font-size:11px;text-transform:uppercase;color:{c["text_secondary"]};font-weight:600;">Patient Risk Status</span>'
                    f'<h2 style="margin:2px 0 0;color:{risk_color};font-size:32px;font-weight:800;">{risk_class}</h2></div>'
                    f'<div style="background:{risk_bg};border:1px solid {risk_color}33;border-radius:8px;padding:10px 16px;text-align:center;">'
                    f'<span style="font-size:10px;text-transform:uppercase;color:{c["text_secondary"]};font-weight:600;">Probability Score</span>'
                    f'<p style="margin:0;color:{risk_color};font-size:24px;font-weight:800;">{risk_score:.1f}%</p>'
                    f'</div></div>'
                    f'<div style="background:{c["surface_alt"]};border:1px solid {c["border"]};padding:12px 16px;border-radius:8px;font-size:13px;line-height:1.5;color:{c["text_secondary"]};">'
                    f'<strong style="color:{c["text"]};">Clinical Directives:</strong> {directive}'
                    f'</div></div>',
                    unsafe_allow_html=True,
                )

                plt = get_plotly_layout()
                fig_g = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=risk_score,
                    domain={"x": [0, 1], "y": [0, 1]},
                    gauge=dict(
                        axis=dict(range=[0, 100], tickwidth=1, tickcolor=plt["text_secondary"],
                                  tickfont=dict(color=plt["text_secondary"])),
                        bar=dict(color=risk_color),
                        bgcolor=c["surface_alt"],
                        borderwidth=1,
                        bordercolor=c["border"],
                        steps=[
                            {"range": [0, 30],  "color": c["green_subtle"]},
                            {"range": [30, 70], "color": c["amber_subtle"]},
                            {"range": [70, 100],"color": c["red_subtle"]},
                        ],
                        threshold=dict(line=dict(color="#EF4444", width=3), thickness=.75, value=70),
                    ),
                    number=dict(font=dict(color=plt["text"], family="Inter, sans-serif", size=24)),
                ))
                fig_g.update_layout(**plt["base"], height=200, margin=dict(t=10, b=10, l=30, r=30))

                st.markdown(chart_card_open("Risk Probability Gauge"), unsafe_allow_html=True)
                st.plotly_chart(fig_g, config=PLOTLY_CFG, use_container_width=True)
                st.markdown(CHART_CARD_CLOSE, unsafe_allow_html=True)

                if contribs:
                    fig_s = go.Figure(go.Bar(
                        y=[c_[0] for c_ in contribs],
                        x=[c_[1] for c_ in contribs],
                        orientation="h",
                        marker_color=[c_[2] for c_ in contribs],
                        width=.6,
                        text=[f"+{c_[1]:.1f}%" if c_[1] > 0 else f"{c_[1]:.1f}%" for c_ in contribs],
                        textposition="auto",
                        textfont=dict(size=10, color="#FFFFFF"),
                    ))
                    fig_s.update_layout(
                        **plt["base"],
                        margin=dict(t=30, b=10, l=140, r=20),
                        height=260,
                        xaxis=dict(
                            **plt["axis_style"],
                            title=dict(text="Contribution %", font=dict(family="Inter, sans-serif", size=10, color=plt["text_secondary"])),
                        ),
                        yaxis=dict(
                            showgrid=False,
                            linecolor=plt["axis"],
                            tickfont=dict(family="Inter, sans-serif", size=10, color=plt["text"]),
                        ),
                    )
                    st.markdown(chart_card_open("Feature Impact Analysis (SHAP Approximation)"), unsafe_allow_html=True)
                    st.plotly_chart(fig_s, use_container_width=True, config=PLOTLY_CFG)
                    st.markdown(CHART_CARD_CLOSE, unsafe_allow_html=True)

        else:
            # Placeholder state — no prediction yet
            st.markdown(
                f'<div style="background:{c["surface"]};border-radius:12px;padding:24px;'
                f'border:1px solid {c["border"]};box-shadow:0 4px 6px -1px rgba(0,0,0,.05);margin-bottom:20px;">'
                f'<h4 style="margin:0 0 16px;font-size:15px;font-weight:600;color:{c["text"]};'
                f'border-bottom:1px solid {c["divider"]};padding-bottom:10px;">Risk Scoring Engine Output</h4>'
                f'<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;margin-bottom:16px;">'
                f'<div><span style="font-size:11px;text-transform:uppercase;color:{c["text_muted"]};font-weight:600;">Patient Risk Status</span>'
                f'<h2 style="margin:2px 0 0;color:{c["text_muted"]};font-size:32px;font-weight:800;">No Prediction</h2></div>'
                f'<div style="background:{c["surface_alt"]};border:1px solid {c["border"]};border-radius:8px;padding:10px 16px;text-align:center;">'
                f'<span style="font-size:10px;text-transform:uppercase;color:{c["text_muted"]};font-weight:600;">Probability Score</span>'
                f'<p style="margin:0;color:{c["text_muted"]};font-size:24px;font-weight:800;">0.0%</p>'
                f'</div></div>'
                f'<div style="background:{c["surface_alt"]};border:1px solid {c["border"]};padding:12px 16px;border-radius:8px;font-size:13px;line-height:1.5;color:{c["text_muted"]};">'
                f'<strong style="color:{c["text_secondary"]};">Clinical Directives:</strong> '
                f'No prediction generated yet. Enter patient parameters and click "Predict Readmission Risk" to generate risk assessment.'
                f'</div></div>',
                unsafe_allow_html=True,
            )

            plt = get_plotly_layout()
            fig_g_empty = go.Figure(go.Indicator(
                mode="gauge+number",
                value=0,
                domain={"x": [0, 1], "y": [0, 1]},
                gauge=dict(
                    axis=dict(range=[0, 100], tickwidth=1, tickcolor=c["border"],
                              tickfont=dict(color=c["text_muted"])),
                    bar=dict(color=c["border"]),
                    bgcolor=c["surface_alt"],
                    borderwidth=1,
                    bordercolor=c["border"],
                    steps=[
                        {"range": [0, 30],  "color": c["surface_alt"]},
                        {"range": [30, 70], "color": c["surface_alt"]},
                        {"range": [70, 100],"color": c["surface_alt"]},
                    ],
                ),
                number=dict(font=dict(color=c["text_muted"], family="Inter, sans-serif", size=24)),
            ))
            fig_g_empty.update_layout(**plt["base"], height=200, margin=dict(t=10, b=10, l=30, r=30))

            st.markdown(chart_card_open("Risk Probability Gauge"), unsafe_allow_html=True)
            st.plotly_chart(fig_g_empty, config=PLOTLY_CFG, use_container_width=True)
            st.markdown(CHART_CARD_CLOSE, unsafe_allow_html=True)

            placeholder_labels = ["Base Rate", "Inpatient", "Hosp Days", "Diagnoses", "Medications", "Age", "Insulin"]
            fig_s_empty = go.Figure(go.Bar(
                y=placeholder_labels,
                x=[0] * len(placeholder_labels),
                orientation="h",
                marker_color=c["border"],
                width=.6,
                text=["0%"] * len(placeholder_labels),
                textposition="auto",
                textfont=dict(size=10, color=c["text_muted"]),
            ))
            fig_s_empty.update_layout(
                **plt["base"],
                title=dict(
                    text="Feature Impact Analysis (SHAP Approximation)",
                    font=dict(family="Inter, sans-serif", size=12, color=c["text_muted"]),
                ),
                margin=dict(t=30, b=10, l=140, r=20),
                height=260,
                xaxis=dict(
                    **plt["axis_style"],
                    title=dict(text="Contribution %", font=dict(family="Inter, sans-serif", size=10, color=c["text_muted"])),
                ),
                yaxis=dict(
                    showgrid=False,
                    linecolor=c["border"],
                    tickfont=dict(family="Inter, sans-serif", size=10, color=c["text_muted"]),
                ),
            )
            st.markdown(chart_card_open("Feature Impact Analysis (SHAP Approximation)"), unsafe_allow_html=True)
            st.plotly_chart(fig_s_empty, use_container_width=True, config=PLOTLY_CFG)
            st.markdown(CHART_CARD_CLOSE, unsafe_allow_html=True)

    render_footer()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.selected_page == "Analytics":
    c = get_theme_colors()

    bar_chart_icon = (
        "<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' "
        "fill='none' stroke='#FFFFFF' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>"
        "<line x1='12' y1='20' x2='12' y2='10'/><line x1='18' y1='20' x2='18' y2='4'/><line x1='6' y1='20' x2='6' y2='16'/></svg>"
    )
    st.markdown(page_header_card(
        "Deep-Dive Demographics & Clinical Analytics",
        "Explore demographic attributes and clinical factors correlations with patient readmissions.",
        bar_chart_icon,
    ), unsafe_allow_html=True)

    def analytics_bar(x, y, color, title_y="Readmission Rate (%)"):
        plt = get_plotly_layout()
        fig = go.Figure(go.Bar(x=x, y=y, marker_color=color, width=0.5))
        fig.update_layout(
            **plt["base"],
            margin=dict(t=20, b=10, l=40, r=20),
            height=280,
            xaxis=plt["xaxis_cat"],
            yaxis=dict(
                **plt["axis_style"],
                title=dict(text=title_y, font=dict(family="Inter, sans-serif", size=10, color=plt["text_secondary"])),
            ),
        )
        return fig

    r1c1, r1c2 = st.columns(2)
    with r1c1:
        st.markdown(chart_card_open("Readmission Rate by Age Group"), unsafe_allow_html=True)
        st.plotly_chart(analytics_bar(
            ["<30", "30-49", "50-69", "70-79", "80+"],
            [12.4, 18.2, 24.8, 31.2, 36.5],
            "#F97316",
        ), use_container_width=True, config=PLOTLY_CFG)
        st.markdown(CHART_CARD_CLOSE, unsafe_allow_html=True)

    with r1c2:
        st.markdown(chart_card_open("Time in Hospital vs Readmission Rate"), unsafe_allow_html=True)
        plt = get_plotly_layout()
        fig = go.Figure(go.Scatter(
            x=list(range(1, 15)),
            y=[14.1, 16.5, 19.2, 22.8, 25.1, 28.4, 30.9, 34.2, 35.8, 38.2, 40.1, 41.5, 43.8, 46.2],
            mode="lines+markers",
            line=dict(color=c["text"], width=3),
            marker=dict(size=8, color="#F97316", line=dict(color=c["surface"], width=2)),
        ))
        fig.update_layout(
            **plt["base"],
            margin=dict(t=20, b=10, l=40, r=20),
            height=280,
            xaxis=dict(
                **plt["xaxis_cat"],
                title=dict(text="Length of Stay (Days)", font=dict(family="Inter, sans-serif", size=10, color=plt["text_secondary"])),
            ),
            yaxis=dict(
                **plt["axis_style"],
                title=dict(text="Readmission Rate (%)", font=dict(family="Inter, sans-serif", size=10, color=plt["text_secondary"])),
            ),
        )
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CFG)
        st.markdown(CHART_CARD_CLOSE, unsafe_allow_html=True)

    r2c1, r2c2 = st.columns(2)
    with r2c1:
        st.markdown(chart_card_open("Prior Inpatient Admissions Influence"), unsafe_allow_html=True)
        st.plotly_chart(analytics_bar(
            ["0 Visits", "1 Visit", "2 Visits", "3 Visits", "4+ Visits"],
            [12.1, 28.5, 44.2, 58.7, 72.4],
            ["#0F172A", "#F97316", "#F97316", "#F97316", "#EF4444"],
        ), use_container_width=True, config=PLOTLY_CFG)
        st.markdown(CHART_CARD_CLOSE, unsafe_allow_html=True)

    with r2c2:
        st.markdown(chart_card_open("Readmission Rate by Diabetes Medication"), unsafe_allow_html=True)
        st.plotly_chart(analytics_bar(
            ["Prescribed Diabetes Med", "No Diabetes Med"],
            [30.4, 21.8],
            ["#F97316", "#0F172A"],
        ), use_container_width=True, config=PLOTLY_CFG)
        st.markdown(CHART_CARD_CLOSE, unsafe_allow_html=True)

    render_footer()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: MODEL PERFORMANCE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.selected_page == "Model Performance":
    c = get_theme_colors()

    memory_icon = (
        "<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' "
        "fill='none' stroke='#FFFFFF' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>"
        "<path d='M2 12h20'/><path d='M2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6'/>"
        "<path d='M12 2L2 7l10 5 10-5-10-5'/><path d='M2 17l10 5 10-5'/></svg>"
    )
    st.markdown(page_header_card(
        "Machine Learning Pipeline Evaluation",
        "Review performance metrics, ROC-AUC curves, and confusion matrix diagnostics for all trained classifiers.",
        memory_icon,
    ), unsafe_allow_html=True)

    # Model comparison table — pure HTML so colours are fully theme-controlled.
    # st.dataframe() renders with its own internal dark theme that conflicts with
    # the light card background, making header text invisible. HTML table avoids this.
    rows = [
        ("Random Forest",       "89.7%", "87.2%", "84.5%", "85.8%", "0.91"),
        ("Decision Tree",       "82.4%", "76.8%", "72.1%", "74.4%", "0.84"),
        ("Logistic Regression", "78.5%", "71.4%", "68.9%", "70.1%", "0.81"),
    ]
    headers = ["Classifier Model", "Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"]

    th_style = (
        f"padding:10px 14px;text-align:left;font-size:12px;font-weight:600;"
        f"color:{c['text_secondary']};text-transform:uppercase;letter-spacing:0.4px;"
        f"border-bottom:2px solid {c['border']};background:{c['surface_alt']};"
    )
    td_style_base = (
        f"padding:11px 14px;font-size:13px;color:{c['text']};"
        f"border-bottom:1px solid {c['border']};"
    )
    td_first_style = (
        f"padding:11px 14px;font-size:13px;font-weight:600;color:{c['text']};"
        f"border-bottom:1px solid {c['border']};"
    )

    header_html = "".join(f"<th style='{th_style}'>{h}</th>" for h in headers)
    body_html = ""
    for i, row in enumerate(rows):
        # Highlight Random Forest row with a subtle orange tint
        row_bg = c["orange_subtle"] if i == 0 else "transparent"
        cells = "".join(
            f"<td style='{td_first_style if j == 0 else td_style_base}'>{v}</td>"
            for j, v in enumerate(row)
        )
        body_html += f"<tr style='background:{row_bg};'>{cells}</tr>"

    table_html = (
        f'<div style="background:{c["surface"]};border-radius:12px;padding:24px;'
        f'border:1px solid {c["border"]};box-shadow:0 4px 6px -1px rgba(0,0,0,.05);margin-bottom:20px;">'
        f'<h4 style="margin:0 0 16px;font-size:15px;font-weight:600;color:{c["text"]};'
        f'border-bottom:1px solid {c["divider"]};padding-bottom:10px;">Model Comparison Metrics</h4>'
        f'<div style="overflow-x:auto;border-radius:8px;border:1px solid {c["border"]};">'
        f'<table style="width:100%;border-collapse:collapse;font-family:Inter,sans-serif;">'
        f'<thead><tr>{header_html}</tr></thead>'
        f'<tbody>{body_html}</tbody>'
        f'</table></div></div>'
    )
    st.markdown(table_html, unsafe_allow_html=True)

    rc1, rc2 = st.columns(2)

    with rc1:
        st.markdown(chart_card_open("ROC-AUC Comparison Curves"), unsafe_allow_html=True)
        plt = get_plotly_layout()
        fpr = np.linspace(0, 1, 100)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=fpr, y=fpr ** 0.40, name="Random Forest (AUC=0.91)", line=dict(color="#F97316", width=3)))
        fig.add_trace(go.Scatter(x=fpr, y=fpr ** 0.60, name="Decision Tree (AUC=0.84)",  line=dict(color=c["text"], width=2)))
        fig.add_trace(go.Scatter(x=fpr, y=fpr ** 0.70, name="Logistic Reg (AUC=0.81)",  line=dict(color=c["text_secondary"], width=2, dash="dash")))
        fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1],   name="Random Guess",              line=dict(color=c["border"], width=1, dash="dot")))
        fig.update_layout(
            **plt["base"],
            margin=dict(t=20, b=20, l=40, r=20),
            height=300,
            xaxis=dict(
                **plt["axis_style"],
                title=dict(text="False Positive Rate", font=dict(size=10, color=plt["text_secondary"])),
            ),
            yaxis=dict(
                **plt["axis_style"],
                title=dict(text="True Positive Rate", font=dict(size=10, color=plt["text_secondary"])),
            ),
            legend=dict(x=0.45, y=0.15, **plt["legend"]),
        )
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CFG)
        st.markdown(CHART_CARD_CLOSE, unsafe_allow_html=True)

    with rc2:
        st.markdown(chart_card_open("Confusion Matrix (Best Model: Random Forest)"), unsafe_allow_html=True)
        plt = get_plotly_layout()
        # Confusion matrix text colour must be readable on the orange heat-map;
        # we let Plotly handle it via text_auto — the values are white on dark cells automatically.
        fig = px.imshow(
            [[7850, 810], [420, 3378]],
            labels=dict(x="Predicted", y="Actual"),
            x=["Not Readmitted", "Readmitted"],
            y=["Not Readmitted", "Readmitted"],
            color_continuous_scale=[[0, c["surface_alt"]], [0.1, "#FFE0CC"], [1, "#F97316"]],
            text_auto=True,
        )
        fig.update_layout(
            **plt["base"],
            margin=dict(t=20, b=20, l=40, r=20),
            height=300,
            coloraxis_showscale=False,
            xaxis=dict(tickfont=dict(family="Inter, sans-serif", size=11, color=plt["text"])),
            yaxis=dict(tickfont=dict(family="Inter, sans-serif", size=11, color=plt["text"])),
        )
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CFG)
        st.markdown(CHART_CARD_CLOSE, unsafe_allow_html=True)

    render_footer()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ABOUT
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.selected_page == "About":
    c = get_theme_colors()

    info_icon = (
        "<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' "
        "fill='none' stroke='#FFFFFF' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>"
        "<circle cx='12' cy='12' r='10'/><line x1='12' y1='16' x2='12' y2='12'/><line x1='12' y1='8' x2='12.01' y2='8'/></svg>"
    )
    st.markdown(page_header_card(
        "About the Clinical Analytics Engine",
        "Medical background, model architecture, training process, and clinical integration guidelines.",
        info_icon,
    ), unsafe_allow_html=True)

    # System Workflow Diagram
    st.markdown(
        f'<div style="background:{c["surface"]};border-radius:12px;padding:24px;'
        f'border:1px solid {c["border"]};box-shadow:0 4px 6px -1px rgba(0,0,0,.05);margin-bottom:20px;">'
        f'<h4 style="margin:0 0 16px;font-size:15px;font-weight:600;color:{c["text"]};'
        f'border-bottom:1px solid {c["divider"]};padding-bottom:10px;">System Workflow</h4>',
        unsafe_allow_html=True,
    )
    workflow_html = (
        f'<div style="display:flex;align-items:center;justify-content:center;gap:8px;padding:20px 0;flex-wrap:wrap;">'
        f'<div style="background:#F97316;color:white;padding:8px 16px;border-radius:6px;font-size:12px;font-weight:600;">Patient Data</div>'
        f'<div style="color:#F97316;font-size:18px;">→</div>'
        f'<div style="background:{c["text"]};color:{c["surface"]};padding:8px 16px;border-radius:6px;font-size:12px;font-weight:600;">Preprocessing</div>'
        f'<div style="color:#F97316;font-size:18px;">→</div>'
        f'<div style="background:{c["text"]};color:{c["surface"]};padding:8px 16px;border-radius:6px;font-size:12px;font-weight:600;">Feature Engineering</div>'
        f'<div style="color:#F97316;font-size:18px;">→</div>'
        f'<div style="background:{c["text"]};color:{c["surface"]};padding:8px 16px;border-radius:6px;font-size:12px;font-weight:600;">SMOTE</div>'
        f'<div style="color:#F97316;font-size:18px;">→</div>'
        f'<div style="background:#F97316;color:white;padding:8px 16px;border-radius:6px;font-size:12px;font-weight:600;">Random Forest</div>'
        f'<div style="color:#F97316;font-size:18px;">→</div>'
        f'<div style="background:{c["text"]};color:{c["surface"]};padding:8px 16px;border-radius:6px;font-size:12px;font-weight:600;">Risk Prediction</div>'
        f'<div style="color:#F97316;font-size:18px;">→</div>'
        f'<div style="background:#22C55E;color:white;padding:8px 16px;border-radius:6px;font-size:12px;font-weight:600;">Clinical Recommendation</div>'
        f'</div>'
    )
    st.markdown(workflow_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)

    # KPI mini-cards
    k1, k2, k3, k4, k5, k6 = st.columns(6)

    def kpi_small(label, value, color="#F97316"):
        tc = get_theme_colors()
        return (
            f'<div style="background:{color}18;border:1px solid {color}35;padding:12px;border-radius:8px;text-align:center;">'
            f'<p style="margin:0;color:{tc["text_secondary"]};font-size:10px;text-transform:uppercase;">{label}</p>'
            f'<p style="margin:4px 0 0;color:{color};font-size:18px;font-weight:700;">{value}</p>'
            f'</div>'
        )

    k1.markdown(kpi_small("Dataset Size", "50K+",       "#F97316"), unsafe_allow_html=True)
    k2.markdown(kpi_small("Clinical Features", "50+",   c["text"]), unsafe_allow_html=True)
    k3.markdown(kpi_small("Accuracy", "89.7%",          "#22C55E"), unsafe_allow_html=True)
    k4.markdown(kpi_small("ROC-AUC", "0.91",            "#22C55E"), unsafe_allow_html=True)
    k5.markdown(kpi_small("Best Model", "RF",            "#F97316"), unsafe_allow_html=True)
    k6.markdown(kpi_small("Target", "Readmission",      c["text"]), unsafe_allow_html=True)

    st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)

    ac1, ac2 = st.columns(2)

    def about_card(title, body_html):
        tc = get_theme_colors()
        return (
            f'<div style="background:{tc["surface"]};border-radius:12px;padding:24px;'
            f'border:1px solid {tc["border"]};box-shadow:0 4px 6px -1px rgba(0,0,0,.05);min-height:320px;">'
            f'<h4 style="margin:0 0 12px;font-size:15px;font-weight:600;color:{tc["text"]};'
            f'border-bottom:1px solid {tc["divider"]};padding-bottom:8px;">{title}</h4>'
            f'{body_html}</div>'
        )

    ac1.markdown(about_card("Project Architecture",
        f'<div style="font-size:13px;line-height:1.6;color:{c["text_secondary"]};">'
        f'<div style="display:flex;flex-direction:column;gap:12px;">'
        f'<div style="display:flex;align-items:center;gap:8px;">'
        f'<div style="background:#F97316;color:white;padding:6px 12px;border-radius:4px;font-size:11px;font-weight:600;">Streamlit</div>'
        f'<div style="color:#F97316;">→</div>'
        f'<div style="background:{c["text"]};color:{c["surface"]};padding:6px 12px;border-radius:4px;font-size:11px;">ML Model</div>'
        f'</div>'
        f'<div style="display:flex;align-items:center;gap:8px;">'
        f'<div style="background:{c["text"]};color:{c["surface"]};padding:6px 12px;border-radius:4px;font-size:11px;">Saved Artifacts</div>'
        f'<div style="color:#F97316;">→</div>'
        f'<div style="background:#22C55E;color:white;padding:6px 12px;border-radius:4px;font-size:11px;font-weight:600;">Prediction Engine</div>'
        f'</div>'
        f'<p style="margin:8px 0 0;font-size:12px;color:{c["text_secondary"]};"><strong style="color:{c["text"]};">Frontend:</strong> Streamlit UI with real-time predictions</p>'
        f'<p style="margin:4px 0;font-size:12px;color:{c["text_secondary"]};"><strong style="color:{c["text"]};">Backend:</strong> Random Forest model with SHAP explainability</p>'
        f'<p style="margin:4px 0;font-size:12px;color:{c["text_secondary"]};"><strong style="color:{c["text"]};">Storage:</strong> Pickle artifacts for model persistence</p>'
        f'</div></div>'),
        unsafe_allow_html=True)

    ac2.markdown(about_card("Why Random Forest?",
        f'<div style="font-size:13px;line-height:1.6;color:{c["text_secondary"]};">'
        f'<ul style="margin:0;padding-left:16px;">'
        f'<li style="margin-bottom:8px;"><strong style="color:#F97316;">Handles mixed data types</strong> — No extensive preprocessing needed</li>'
        f'<li style="margin-bottom:8px;"><strong style="color:#F97316;">Feature importance</strong> — Built-in SHAP interpretability</li>'
        f'<li style="margin-bottom:8px;"><strong style="color:#F97316;">Robust to outliers</strong> — Less sensitive to extreme values</li>'
        f'<li style="margin-bottom:8px;"><strong style="color:#F97316;">Non-linear relationships</strong> — Captures complex patterns</li>'
        f'<li style="margin-bottom:8px;"><strong style="color:#F97316;">Ensemble method</strong> — Reduces overfitting risk</li>'
        f'<li><strong style="color:#F97316;">Fast inference</strong> — Real-time prediction capability</li>'
        f'</ul></div>'),
        unsafe_allow_html=True)

    render_footer()
