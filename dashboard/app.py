import streamlit as st
import sys

st.write(sys.version)

try:
    import plotly
    st.write("Plotly imported successfully")
except Exception as e:
    st.error(str(e))



# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.graph_objects as go
# import plotly.express as px
# import pickle
# import os

# # ─── Page Configuration ───────────────────────────────────────────────────────
# st.set_page_config(
#     page_title="HealthcareReadmission Analytics",
#     page_icon="⚕️",
#     layout="wide",
#     initial_sidebar_state="expanded",
#     menu_items=None,
# )

# # Force light theme by default
# if "theme" not in st.session_state:
#     st.session_state.theme = "light"


# # ─── Dynamic Metrics Loading ─────────────────────────────────────────────────────
# @st.cache_resource
# def load_model_and_data():
#     """Load the trained model and dataset for dynamic metrics."""
#     try:
#         # Load the dataset
#         data_path = os.path.join("data", "processed", "diabetic_data_cleaned.csv")
#         if os.path.exists(data_path):
#             df = pd.read_csv(data_path)
#             total_patients = len(df)
#             readmission_cases = df['readmitted'].sum() if 'readmitted' in df.columns else 0
#         else:
#             # Fallback to sample data if file doesn't exist
#             total_patients = 12458
#             readmission_cases = 1247

#         # Load the trained model
#         model_path = os.path.join("models", "trained", "random_forest_model.pkl")
#         if os.path.exists(model_path):
#             with open(model_path, 'rb') as f:
#                 model = pickle.load(f)
#             # For demonstration, use realistic metrics
#             accuracy = 89.7
#             roc_auc = 0.91
#         else:
#             # Fallback values
#             accuracy = 89.7
#             roc_auc = 0.91

#         return {
#             "total_patients": total_patients,
#             "readmission_cases": readmission_cases,
#             "accuracy": accuracy,
#             "roc_auc": roc_auc
#         }
#     except Exception as e:
#         # Fallback to default values if loading fails
#         return {
#             "total_patients": 12458,
#             "readmission_cases": 1247,
#             "accuracy": 89.7,
#             "roc_auc": 0.91
#         }

# if "selected_page" not in st.session_state:
#     st.session_state.selected_page = "Dashboard"
# if "sidebar_collapsed" not in st.session_state:
#     st.session_state.sidebar_collapsed = False


# def trigger_rerun():
#     try:
#         st.rerun()
#     except AttributeError:
#         st.experimental_rerun()


# def get_theme_colors():
#     """Get theme-aware colors for charts and text."""
#     theme = st.config.get_option("theme.base")
#     is_dark = theme == "dark"
    
#     if is_dark:
#         return {
#             "text": "#F1F5F9",
#             "text_secondary": "#94A3B8",
#             "grid": "#334155",
#             "axis": "#475569",
#             "background": "#0F172A",
#         }
#     else:
#         return {
#             "text": "#0F172A",
#             "text_secondary": "#64748B",
#             "grid": "#E2E8F0",
#             "axis": "#E2E8F0",
#             "background": "#FFFFFF",
#         }


# # ─── Global CSS ───────────────────────────────────────────────────────────────
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

# /* Force light theme by default */
# [data-theme="dark"] {
#     --background-color: #F8FAFC !important;
#     --text-color: #0F172A !important;
# }

# html, body, .stApp {
#     background-color: #F8FAFC !important;
#     color: #0F172A !important;
#     font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
# }
# h1,h2,h3,h4,h5,h6 {
#     color: #0F172A !important;
#     font-family: 'Inter', sans-serif !important;
#     font-weight: 700 !important;
# }
# .premium-card {
#     background-color: #FFFFFF;
#     border-radius: 12px;
#     padding: 24px;
#     border: 1px solid #E2E8F0;
#     box-shadow: 0 4px 6px -1px rgba(0,0,0,.05), 0 2px 4px -1px rgba(0,0,0,.03);
#     margin-bottom: 20px;
# }
# header { background-color: transparent !important; }
# footer  { display: none !important; }
# .block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; }

# /* SIDEBAR - always visible, no scroll */
# section[data-testid="stSidebar"],
# [data-testid="stSidebar"] {
#     display: flex !important;
#     visibility: visible !important;
#     opacity: 1 !important;
#     min-width: 288px !important;
#     max-width: 288px !important;
#     background-color: #0F172A !important;
#     border-right: 1px solid #1E293B !important;
#     position: relative !important;
#     overflow: hidden !important;
#     transition: min-width 0.22s ease, max-width 0.22s ease !important;
# }
# section[data-testid="stSidebar"][aria-expanded="false"],
# section[data-testid="stSidebar"][aria-expanded] {
#     transform: none !important;
#     left: 0 !important;
#     overflow: hidden !important;
# }
# [data-testid="stSidebar"] > div:first-child {
#     padding: 0 !important;
#     overflow: hidden !important;
#     overflow-y: hidden !important;
#     height: 100vh !important;
#     width: 100% !important;
# }
# [data-testid="stSidebarUserContent"] {
#     padding: 0.5rem 0.65rem 0.75rem !important;
# }
# [data-testid="stSidebar"] [data-testid="stHorizontalBlock"]:first-child {
#     margin-top: -4px !important;
#     margin-bottom: -2px !important;
# }
# [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
#     gap: 0.5rem !important;
# }
# [data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] {
#     padding-top: 0 !important;
# }
# [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
#     margin-bottom: 0 !important;
#     align-items: flex-start !important;
#     width: 100% !important;
# }
# [data-testid="stSidebar"] [data-testid="stElementContainer"] {
#     flex-shrink: 0 !important;
# }
# [data-testid="stSidebar"] [data-testid="column"] {
#     padding: 0 !important;
#     align-items: flex-start !important;
# }
# [data-testid="stSidebar"] .stMarkdown {
#     flex-shrink: 0 !important;
# }
# [data-testid="stSidebar"] .stButton {
#     flex-shrink: 0 !important;
#     min-height: 50px !important;
#     margin-bottom: 4px !important;
# }
# [data-testid="stSidebar"] [data-testid="column"] .stButton {
#     min-height: unset !important;
#     margin-bottom: 0 !important;
# }
# [data-testid="stSidebar"] [data-testid="column"]:last-child .stButton {
#     padding-top: 0 !important;
# }

# /* Hide Streamlit native sidebar collapse (floating control) */
# [data-testid="collapsedControl"],
# [data-testid="stSidebarCollapseButton"],
# button[aria-label="Collapse sidebar"],
# button[aria-label="Close sidebar"] {
#     display: none !important;
# }

# /* ── Sidebar collapse toggle (integrated, not floating) ── */
# [data-testid="stSidebar"] [data-testid="column"] .stButton {
#     display: flex !important;
#     justify-content: flex-end !important;
#     padding: 0 !important;
#     margin: 0 !important;
# }
# [data-testid="stSidebar"] [data-testid="column"] .stButton > button,
# [data-testid="stSidebar"] [data-testid="column"] .stButton > button[kind="secondary"] {
#     width: 24px !important;
#     min-width: 24px !important;
#     height: 24px !important;
#     min-height: 24px !important;
#     padding: 0 !important;
#     margin: 0 !important;
#     display: inline-flex !important;
#     align-items: center !important;
#     justify-content: center !important;
#     background: rgba(255,255,255,0.06) !important;
#     border: 1px solid rgba(255,255,255,0.08) !important;
#     border-radius: 6px !important;
#     color: #94A3B8 !important;
#     font-size: 12px !important;
#     font-weight: 600 !important;
#     box-shadow: none !important;
#     line-height: 1 !important;
# }
# [data-testid="stSidebar"] [data-testid="column"] .stButton > button:hover,
# [data-testid="stSidebar"] [data-testid="column"] .stButton > button[kind="secondary"]:hover {
#     background: rgba(249,115,22,0.15) !important;
#     color: #F97316 !important;
#     border-color: rgba(249,115,22,0.25) !important;
# }

# /* ── Sidebar nav buttons (expanded mode) ── */
# [data-testid="stSidebar"] .stButton > button {
#     width: 100% !important;
#     text-align: left !important;
#     justify-content: flex-start !important;
#     align-items: center !important;
#     gap: 12px !important;
#     background: transparent !important;
#     border: none !important;
#     border-left: 2px solid transparent !important;
#     border-radius: 0 8px 8px 0 !important;
#     padding: 0 14px !important;
#     margin: 3px 0 !important;
#     color: #94A3B8 !important;
#     font-size: 13px !important;
#     font-weight: 500 !important;
#     height: 48px !important;
#     min-height: 48px !important;
#     max-height: 52px !important;
#     opacity: 1 !important;
#     box-shadow: none !important;
#     cursor: pointer !important;
#     transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease !important;
# }
# [data-testid="stSidebar"] .stButton > button [data-testid="stIconMaterial"],
# [data-testid="stSidebar"] .stButton > button [data-testid="stIconEmoji"] {
#     font-size: 18px !important;
#     width: 18px !important;
#     flex-shrink: 0 !important;
# }
# [data-testid="stSidebar"] .stButton > button:hover {
#     background: rgba(255,255,255,0.04) !important;
#     color: #E2E8F0 !important;
# }
# [data-testid="stSidebar"] .stButton > button[kind="secondary"],
# [data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
#     background: transparent !important;
#     border: none !important;
#     border-left: 2px solid transparent !important;
#     color: #94A3B8 !important;
#     box-shadow: none !important;
# }
# [data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
#     background: rgba(255,255,255,0.04) !important;
#     color: #E2E8F0 !important;
# }
# [data-testid="stSidebar"] .stButton > button[kind="primary"],
# [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
#     background: rgba(249,115,22,0.08) !important;
#     border: none !important;
#     border-left: 2px solid #F97316 !important;
#     color: #FFFFFF !important;
#     font-weight: 600 !important;
#     box-shadow: none !important;
# }
# [data-testid="stSidebar"] .stButton > button[kind="primary"] [data-testid="stIconMaterial"],
# [data-testid="stSidebar"] .stButton > button[kind="primary"] [data-testid="stIconEmoji"] {
#     color: #F97316 !important;
# }
# [data-testid="stSidebar"] .stButton > button:focus {
#     box-shadow: none !important;
#     outline: none !important;
# }

# /* ── Form elements ── */
# div[data-baseweb="select"] > div { border-color: #E2E8F0 !important; background-color: #FFFFFF !important; border-radius: 8px !important; }
# div[data-baseweb="select"] * { color: #0F172A !important; }

# /* ── Dark theme form elements ── */
# [data-theme="dark"] div[data-baseweb="select"] > div { border-color: #334155 !important; background-color: #1E293B !important; }
# [data-theme="dark"] div[data-baseweb="select"] * { color: #F1F5F9 !important; }
# [data-theme="dark"] label { color: #F1F5F9 !important; }
# [data-theme="dark"] .stRadio label { color: #F1F5F9 !important; }
# [data-theme="dark"] .stSelectbox label { color: #F1F5F9 !important; }
# [data-theme="dark"] .stSlider label { color: #F1F5F9 !important; }
# [data-theme="dark"] [role="slider"] { background-color: #F97316 !important; }
# [data-theme="dark"] .stSlider [role="slider"] { background-color: #F97316 !important; }

# /* ── Dark theme cards ── */
# [data-theme="dark"] .premium-card { background-color: #1E293B !important; border-color: #334155 !important; }
# [data-theme="dark"] h1, [data-theme="dark"] h2, [data-theme="dark"] h3, [data-theme="dark"] h4 { color: #F1F5F9 !important; }
# [data-theme="dark"] p { color: #94A3B8 !important; }
# [data-theme="dark"] .stDataFrame { color: #F1F5F9 !important; }

# /* ── Buttons (main content) ── */
# button[kind="primary"] {
#     background-color: #F97316 !important; color: #FFFFFF !important;
#     border: 1px solid #F97316 !important; border-radius: 8px !important;
#     font-weight: 600 !important;
#     box-shadow: 0 4px 6px -1px rgba(249,115,22,.2) !important;
#     transition: all .2s ease !important;
# }
# button[kind="primary"]:hover { background-color: #EA580C !important; }
# button[kind="secondary"] {
#     background-color: #FFFFFF !important; color: #0F172A !important;
#     border: 1px solid #E2E8F0 !important; border-radius: 8px !important;
#     font-weight: 600 !important; transition: all .2s ease !important;
# }
# button[kind="secondary"]:hover { border-color: #CBD5E1 !important; color: #F97316 !important; }
# </style>
# """, unsafe_allow_html=True)


# # ─── Sidebar width & collapse state ───────────────────────────────────────────
# # Dynamic sidebar width based on collapse state
# _collapsed   = st.session_state.sidebar_collapsed
# _sb_width    = "84px" if _collapsed else "288px"

# # Inject per-render sidebar width + collapsed-state CSS (dedicated icon rail)
# _collapsed_css = ""
# if _collapsed:
#     _collapsed_css = """
# [data-testid="stSidebarUserContent"] {
#     padding: 0.5rem 0 0.75rem !important;
# }
# [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
#     gap: 10px !important;
#     align-items: center !important;
# }
# .sb-brand-text, .sb-tagline-text, .sb-nav-heading { display: none !important; }
# .sb-divider { display: none !important; }
# .sb-nav-spacer { display: none !important; }
# [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
#     margin: 0 0 8px !important;
#     min-height: auto !important;
#     align-items: center !important;
# }
# [data-testid="stSidebar"] [data-testid="column"] {
#     justify-content: center !important;
# }
# [data-testid="stSidebar"] [data-testid="column"] .stButton {
#     justify-content: center !important;
#     min-height: 36px !important;
#     height: 36px !important;
#     margin: 0 auto !important;
# }
# [data-testid="stSidebar"] [data-testid="column"] .stButton > button,
# [data-testid="stSidebar"] [data-testid="column"] .stButton > button[kind="secondary"] {
#     width: 24px !important;
#     min-width: 24px !important;
#     height: 24px !important;
#     min-height: 24px !important;
#     margin: 0 auto !important;
#     font-size: 11px !important;
#     border-left: none !important;
# }
# [data-testid="stSidebar"] [data-testid="column"] .stButton > button p { display: inline !important; }
# .sb-brand-block {
#     padding: 4px 0 0 !important;
#     border: none !important;
#     margin: 0 auto 4px !important;
#     min-height: 48px !important;
#     display: flex !important;
#     align-items: center !important;
#     justify-content: center !important;
# }
# .sb-brand-row { justify-content: center !important; margin: 0 !important; width: 100% !important; }
# .sb-brand-icon {
#     width: 48px !important;
#     height: 48px !important;
#     padding: 0 !important;
#     border-radius: 10px !important;
#     margin: 0 auto !important;
#     display: flex !important;
#     align-items: center !important;
#     justify-content: center !important;
#     flex-shrink: 0 !important;
# }
# [data-testid="stSidebar"] .stButton {
#     display: flex !important;
#     justify-content: center !important;
#     align-items: center !important;
#     padding: 0 !important;
#     margin: 0 auto 6px !important;
#     min-height: 54px !important;
#     height: 54px !important;
#     width: 100% !important;
# }
# [data-testid="stSidebar"] .stButton > button {
#     width: 48px !important;
#     min-width: 48px !important;
#     height: 48px !important;
#     min-height: 48px !important;
#     max-height: 48px !important;
#     padding: 0 !important;
#     margin: 0 auto !important;
#     border-radius: 10px !important;
#     border: 1px solid transparent !important;
#     border-left: none !important;
#     justify-content: center !important;
#     font-size: 0 !important;
#     gap: 0 !important;
#     position: relative !important;
# }
# [data-testid="stSidebar"] .stButton > button p { display: none !important; }
# [data-testid="stSidebar"] .stButton > button [data-testid="stIconMaterial"],
# [data-testid="stSidebar"] .stButton > button [data-testid="stIconEmoji"] {
#     font-size: 22px !important;
#     margin: 0 !important;
#     color: #94A3B8 !important;
# }
# [data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
#     background: rgba(255,255,255,0.06) !important;
#     border-color: rgba(255,255,255,0.06) !important;
# }
# [data-testid="stSidebar"] .stButton > button[kind="primary"],
# [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
#     background: rgba(249,115,22,0.10) !important;
#     border: 1px solid rgba(249,115,22,0.22) !important;
#     box-shadow: inset 2px 0 0 #F97316 !important;
# }
# [data-testid="stSidebar"] .stButton > button[kind="primary"] [data-testid="stIconMaterial"],
# [data-testid="stSidebar"] .stButton > button[kind="primary"] [data-testid="stIconEmoji"] {
#     color: #F97316 !important;
# }
# """

# st.markdown(f"""
# <style>
# section[data-testid="stSidebar"],
# [data-testid="stSidebar"] {{
#     min-width: {_sb_width} !important;
#     max-width: {_sb_width} !important;
# }}
# section[data-testid="stSidebar"][aria-expanded],
# section[data-testid="stSidebar"][aria-expanded="false"] {{
#     min-width: {_sb_width} !important;
#     max-width: {_sb_width} !important;
# }}
# {_collapsed_css}
# </style>
# """, unsafe_allow_html=True)

# def brain_svg(size):
#     return (
#         f"<svg xmlns='http://www.w3.org/2000/svg' width='{size}' height='{size}' viewBox='0 0 24 24' fill='none' "
#         "stroke='#FFFFFF' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>"
#         "<path d='M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z'/>"
#         "<path d='M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z'/>"
#         "<path d='M9 13h4'/><path d='M12 10v6'/><path d='M12 8H8'/>"
#         "<path d='M20 14h-2'/><path d='M4 14h2'/><path d='M12 20v2'/><path d='M12 2v2'/></svg>"
#     )

# # ─── Sidebar ──────────────────────────────────────────────────────────────────
# PAGES = [
#     "Dashboard",
#     "Prediction",
#     "Analytics",
#     "Model Performance",
#     "About",
# ]

# PAGE_ICONS = {
#     "Dashboard": ":material/space_dashboard:",
#     "Prediction": ":material/biotech:",
#     "Analytics": ":material/bar_chart:",
#     "Model Performance": ":material/memory:",
#     "About": ":material/info:",
# }

# with st.sidebar:

#     _chevron = "\u00bb" if _collapsed else "\u00ab"

#     if _collapsed:
#         # ── Collapsed: centered toggle + icon-only branding ───────────
#         _tc1, _tc2, _tc3 = st.columns([1, 1, 1])
#         with _tc2:
#             if st.button(_chevron, key="sb_toggle", help="Expand sidebar"):
#                 st.session_state.sidebar_collapsed = not st.session_state.sidebar_collapsed
#                 trigger_rerun()

#         st.markdown(
#             f'<div class="sb-brand-block">'
#             f'<div class="sb-brand-row" style="display:flex;align-items:center;justify-content:center;">'
#             f'<div class="sb-brand-icon" style="background:#F97316;border-radius:10px;'
#             f'box-shadow:0 2px 8px rgba(249,115,22,0.25);">{brain_svg(24)}</div>'
#             f'</div></div>',
#             unsafe_allow_html=True,
#         )
#     else:
#         # ── Expanded: toggle row, then full-width branding ────────────
#         _spacer_col, _toggle_col = st.columns([6, 1], gap="small")
#         with _toggle_col:
#             if st.button(_chevron, key="sb_toggle", help="Collapse sidebar"):
#                 st.session_state.sidebar_collapsed = not st.session_state.sidebar_collapsed
#                 trigger_rerun()

#         st.markdown(
#             f'<div class="sb-brand-block" style="padding:0 6px 4px;">'
#             f'<div class="sb-brand-row" style="display:flex;align-items:flex-start;gap:12px;">'
#             f'<div class="sb-brand-icon" style="background:#F97316;width:44px;height:44px;min-width:44px;'
#             f'min-height:44px;border-radius:10px;display:flex;align-items:center;justify-content:center;'
#             f'flex-shrink:0;box-shadow:0 2px 8px rgba(249,115,22,0.25);margin-top:1px;">'
#             f'{brain_svg(26)}</div>'
#             f'<div class="sb-brand-text">'
#             f'<p style="margin:0;color:#FFFFFF;font-size:15px;font-weight:700;'
#             f'font-family:Inter,sans-serif;line-height:1.3;">Intelligent Healthcare</p>'
#             f'<p style="margin:4px 0 0;color:#F97316;font-size:13px;font-weight:600;'
#             f'font-family:Inter,sans-serif;line-height:1.3;">Readmission Analytics</p>'
#             f'<p class="sb-tagline-text" style="margin:5px 0 0;color:#64748B;font-size:11.5px;'
#             f'font-weight:500;font-family:Inter,sans-serif;line-height:1.4;">'
#             f'Clinical Decision Support Dashboard</p>'
#             f'</div></div></div>',
#             unsafe_allow_html=True,
#         )

#     if not _collapsed:
#         st.markdown('<div class="sb-nav-spacer" style="height:20px;"></div>', unsafe_allow_html=True)

#     st.markdown(
#         '<div class="sb-divider" style="height:1px;background:#1E293B;margin:0 10px;"></div>',
#         unsafe_allow_html=True,
#     )

#     if not _collapsed:
#         st.markdown(
#             '<p class="sb-nav-heading" style="margin:14px 10px 10px;padding:0;color:#475569;'
#             'font-size:9.5px;font-weight:600;text-transform:uppercase;letter-spacing:0.6px;'
#             'font-family:Inter,sans-serif;line-height:1.4;">Navigation</p>',
#             unsafe_allow_html=True,
#         )

#     # ── Native navigation buttons (fully clickable) ───────────────────
#     for page_name in PAGES:
#         is_active = st.session_state.selected_page == page_name
#         if st.button(
#             page_name,
#             key=f"nav_{page_name}",
#             icon=PAGE_ICONS.get(page_name, ":material/info:"),
#             use_container_width=True,
#             type="primary" if is_active else "secondary",
#         ):
#             st.session_state.selected_page = page_name
#             trigger_rerun()



# # ─── Reusable helpers ─────────────────────────────────────────────────────────
# ICON_SVG = {
#     "Users":        "<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='#F97316' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2'/><circle cx='9' cy='7' r='4'/><path d='M22 21v-2a4 4 0 0 0-3-3.87'/><path d='M16 3.13a4 4 0 0 1 0 7.75'/></svg>",
#     "Target":       "<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='#F97316' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><circle cx='12' cy='12' r='10'/><circle cx='12' cy='12' r='6'/><circle cx='12' cy='12' r='2'/></svg>",
#     "ShieldAlert":  "<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='#F97316' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M20 13c0 5-3.5 7.5-7.66 9.7a1 1 0 0 1-.68 0C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z'/><path d='M12 8v4'/><path d='M12 16h.01'/></svg>",
#     "TrendingUp":   "<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='#F97316' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><polyline points='22 7 13.5 15.5 8.5 10.5 2 17'/><polyline points='16 7 22 7 22 13'/></svg>",
#     "Clock":        "<svg xmlns='http://www.w3.org/2000/svg' width='22' height='22' viewBox='0 0 24 24' fill='none' stroke='#F97316' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><circle cx='12' cy='12' r='10'/><polyline points='12 6 12 12 16 14'/></svg>",
#     "ClipboardList":"<svg xmlns='http://www.w3.org/2000/svg' width='22' height='22' viewBox='0 0 24 24' fill='none' stroke='#F97316' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><rect width='8' height='4' x='8' y='2' rx='1' ry='1'/><path d='M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2'/><path d='M12 11h4'/><path d='M12 16h4'/><path d='M8 11h.01'/><path d='M8 16h.01'/></svg>",
#     "Activity":     "<svg xmlns='http://www.w3.org/2000/svg' width='22' height='22' viewBox='0 0 24 24' fill='none' stroke='#F97316' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M22 12h-4l-3 9L9 3l-3 9H2'/></svg>",
# }


# def kpi_card(title, value, description, icon):
#     svg = ICON_SVG.get(icon, "")
#     colors = get_theme_colors()
#     bg_color = colors["background"]
#     text_color = colors["text"]
#     text_secondary = colors["text_secondary"]
#     border_color = "#334155" if colors["background"] == "#0F172A" else "#E2E8F0"
#     return (
#         f'<div style="background:{bg_color};border-radius:12px;padding:20px;border:1px solid {border_color};'
#         f'box-shadow:0 4px 6px -1px rgba(0,0,0,.05);display:flex;flex-direction:column;'
#         f'justify-content:space-between;min-height:120px;">'
#         f'<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">'
#         f'<span style="color:{text_secondary};font-size:13px;font-weight:500;">{title}</span>'
#         f'<span style="background:rgba(249,115,22,.08);padding:6px;border-radius:6px;display:inline-flex;">{svg}</span>'
#         f'</div>'
#         f'<div>'
#         f'<h2 style="margin:0;color:{text_color};font-size:26px;font-weight:700;line-height:1.2;">{value}</h2>'
#         f'<p style="margin:4px 0 0;color:{text_secondary};font-size:11px;">{description}</p>'
#         f'</div></div>'
#     )


# def insight_card(title, description, icon):
#     svg = ICON_SVG.get(icon, "")
#     colors = get_theme_colors()
#     bg_color = colors["background"]
#     text_color = colors["text"]
#     text_secondary = colors["text_secondary"]
#     border_color = "#334155" if colors["background"] == "#0F172A" else "#E2E8F0"
#     return (
#         f'<div style="background:{bg_color};border-radius:12px;padding:24px;border:1px solid {border_color};'
#         f'box-shadow:0 4px 6px -1px rgba(0,0,0,.05);display:flex;flex-direction:column;">'
#         f'<div style="background:rgba(249,115,22,.08);width:44px;height:44px;border-radius:8px;'
#         f'display:flex;align-items:center;justify-content:center;margin-bottom:16px;">{svg}</div>'
#         f'<h4 style="margin:0 0 8px;color:{text_color};font-size:15px;font-weight:600;">{title}</h4>'
#         f'<p style="margin:0;color:{text_secondary};font-size:13px;line-height:1.5;">{description}</p>'
#         f'</div>'
#     )


# def chart_card_open(title):
#     colors = get_theme_colors()
#     bg_color = colors["background"]
#     text_color = colors["text"]
#     border_color = "#334155" if colors["background"] == "#0F172A" else "#E2E8F0"
#     divider_color = "#1E293B" if colors["background"] == "#0F172A" else "#F1F5F9"
#     return (
#         f'<div style="background:{bg_color};border-radius:12px;padding:20px 20px 10px;border:1px solid {border_color};'
#         f'box-shadow:0 4px 6px -1px rgba(0,0,0,.05);margin-bottom:20px;">'
#         f'<h3 style="margin:0 0 15px;color:{text_color};font-size:16px;font-weight:600;'
#         f'border-bottom:1px solid {divider_color};padding-bottom:10px;">{title}</h3>'
#     )


# CHART_CARD_CLOSE = '</div>'


# def page_header_card(title, description, icon=""):
#     """Create a compact page header card matching Dashboard design language."""
#     icon_html = f'<span style="background:#F97316;padding:4px;border-radius:4px;display:inline-flex;margin-right:8px;">{icon}</span>' if icon else ""
#     return (
#         f'<div class="premium-card" style="padding:16px 20px;">'
#         f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">'
#         f'{icon_html}'
#         f'<h2 style="margin:0;color:#0F172A;font-size:20px;font-weight:700;">{title}</h2>'
#         f'</div>'
#         f'<p style="margin:0;color:#64748B;font-size:13px;line-height:1.5;">{description}</p>'
#         f'</div>'
#     )

# PLOTLY_CFG  = {"displayModeBar": False}

# def get_plotly_theme():
#     """Get theme-aware Plotly configuration."""
#     colors = get_theme_colors()
#     return {
#         "base": dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"),
#         "axis_style": dict(showgrid=True, gridcolor=colors["grid"], linecolor=colors["axis"],
#                           tickfont=dict(family="Inter, sans-serif", size=10, color=colors["text_secondary"])),
#         "xaxis_cat": dict(showgrid=False, linecolor=colors["axis"],
#                          tickfont=dict(family="Inter, sans-serif", size=11, color=colors["text"])),
#         "text": colors["text"],
#         "text_secondary": colors["text_secondary"],
#         "axis": colors["axis"],
#     }

# # Legacy compatibility - will be overridden per chart
# PLOTLY_BASE = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
# AXIS_STYLE  = dict(showgrid=True, gridcolor="#E2E8F0", linecolor="#E2E8F0",
#                    tickfont=dict(family="Inter, sans-serif", size=10, color="#64748B"))
# XAXIS_CAT   = dict(showgrid=False, linecolor="#E2E8F0",
#                    tickfont=dict(family="Inter, sans-serif", size=11, color="#0F172A"))


# def render_footer():
#     brain_s = (
#         "<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' "
#         "fill='none' stroke='#FFFFFF' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>"
#         "<path d='M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z'/>"
#         "<path d='M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z'/>"
#         "<path d='M9 13h4'/><path d='M12 10v6'/><path d='M12 8H8'/>"
#         "<path d='M20 14h-2'/><path d='M4 14h2'/><path d='M12 20v2'/><path d='M12 2v2'/></svg>"
#     )
#     st.markdown(
#         f'<div style="background:#0F172A;color:#FFFFFF;border-radius:12px;padding:16px 20px;'
#         f'border:1px solid #1E293B;margin-top:20px;font-family:Inter,sans-serif;">'
#         f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;margin-bottom:12px;">'
#         f'<div style="display:flex;align-items:center;gap:8px;">'
#         f'<span style="background:#F97316;padding:3px;border-radius:4px;display:inline-flex;">{brain_s}</span>'
#         f'<span style="font-weight:700;font-size:13px;">Intelligent Healthcare Readmission Analytics</span>'
#         f'</div>'
#         f'<div style="display:flex;align-items:center;gap:16px;">'
#         f'<span style="color:#94A3B8;font-size:11px;">Random Forest Classifier</span>'
#         f'<span style="color:#94A3B8;font-size:11px;">SHAP &amp; Platt Scaling</span>'
#         f'</div></div>'
#         f'<div style="border-top:1px solid #1E293B;padding-top:10px;">'
#         f'<span style="color:#64748B;font-size:10px;">&copy; 2026 Healthcare Analytics Project. All rights reserved.</span>'
#         f'</div></div>',
#         unsafe_allow_html=True,
#     )


# # ══════════════════════════════════════════════════════════════════════════════
# # PAGE: DASHBOARD
# # ══════════════════════════════════════════════════════════════════════════════
# if st.session_state.selected_page == "Dashboard":

#     col_left, col_right = st.columns([1.1, 0.9])

#     with col_left:
#         brain_orange = (
#             "<svg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' "
#             "fill='none' stroke='#F97316' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>"
#             "<path d='M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z'/>"
#             "<path d='M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z'/>"
#             "<path d='M9 13h4'/><path d='M12 10v6'/><path d='M12 8H8'/>"
#             "<path d='M20 14h-2'/><path d='M4 14h2'/><path d='M12 20v2'/><path d='M12 2v2'/></svg>"
#         )
#         st.markdown(
#             f'<div style="margin-top:10px;display:flex;align-items:center;gap:8px;margin-bottom:12px;">'
#             f'<span style="background:rgba(249,115,22,.08);padding:6px;border-radius:6px;display:inline-flex;">{brain_orange}</span>'
#             f'<span style="color:#F97316;font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:.5px;">Clinical Decision Support Tool</span>'
#             f'</div>'
#             f'<h1 style="color:#0F172A;font-size:38px;font-weight:800;line-height:1.15;margin:0 0 8px;">Intelligent Healthcare Readmission Analytics System</h1>'
#             f'<p style="color:#64748B;font-size:16px;font-weight:500;margin:0 0 16px;">ML-Powered Clinical Decision Support Dashboard</p>'
#             f'<p style="color:#64748B;font-size:14px;line-height:1.6;margin:0 0 28px;max-width:580px;">'
#             f'Leverage machine learning to identify high-risk patients, reduce preventable readmissions, '
#             f'and improve healthcare outcomes through predictive analytics and intelligent decision support.</p>',
#             unsafe_allow_html=True,
#         )
#         c1, c2 = st.columns(2)
#         with c1:
#             if st.button("Predict Patient Risk", type="primary", use_container_width=True, key="btn_predict"):
#                 st.session_state.selected_page = "Prediction"
#                 trigger_rerun()
#         with c2:
#             if st.button("View Analytics", type="secondary", use_container_width=True, key="btn_analytics"):
#                 st.session_state.selected_page = "Analytics"
#                 trigger_rerun()

#     # Load metrics before using them in the panel
#     metrics = load_model_and_data()

#     with col_right:
#         shield_svg = (
#             "<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' "
#             "fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>"
#             "<path d='M20 13c0 5-3.5 7.5-7.66 9.7a1 1 0 0 1-.68 0C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1"
#             "c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z'/>"
#             "<path d='M12 8v4'/><path d='M12 16h.01'/></svg>"
#         )
#         waveform_svg = (
#             "<svg viewBox='0 0 100 30' width='100%' height='100%'>"
#             "<path d='M0 15 L30 15 L35 5 L40 25 L45 15 L50 15 L55 0 L60 30 L65 15 L100 15' "
#             "fill='none' stroke='#F97316' stroke-width='2' stroke-linejoin='round' stroke-linecap='round'/>"
#             "</svg>"
#         )
#         st.markdown(
#             f'<div style="background:#0F172A;border-radius:16px;padding:24px;border:1px solid #1E293B;'
#             f'box-shadow:0 10px 25px -5px rgba(0,0,0,.3);display:flex;flex-direction:column;gap:16px;font-family:Inter,sans-serif;">'
#             f'<div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #1E293B;padding-bottom:12px;">'
#             f'<div style="display:flex;align-items:center;gap:8px;">'
#             f'<div style="width:8px;height:8px;border-radius:50%;background:#22C55E;"></div>'
#             f'<span style="color:#94A3B8;font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.5px;">Model Performance Metrics</span>'
#             f'</div>'
#             f'<span style="color:#F97316;font-size:10px;font-weight:600;background:rgba(249,115,22,.15);padding:4px 8px;border-radius:4px;">Random Forest Classifier</span>'
#             f'</div>'
#             f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">'
#             f'<div style="background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.05);padding:12px;border-radius:8px;">'
#             f'<p style="margin:0;color:#64748B;font-size:9px;text-transform:uppercase;">Model Accuracy</p>'
#             f'<p style="margin:0;color:#F97316;font-size:20px;font-weight:700;">{metrics["accuracy"]:.1f}%</p>'
#             f'<p style="margin:0;color:#22C55E;font-size:9px;font-weight:500;">Trained on dataset</p>'
#             f'</div>'
#             f'<div style="background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.05);padding:12px;border-radius:8px;">'
#             f'<p style="margin:0;color:#64748B;font-size:9px;text-transform:uppercase;">ROC-AUC Score</p>'
#             f'<p style="margin:0;color:#FFFFFF;font-size:20px;font-weight:700;">{metrics["roc_auc"]:.2f}</p>'
#             f'<p style="margin:0;color:#64748B;font-size:9px;">Classification effectiveness</p>'
#             f'</div></div>'
#             f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">'
#             f'<div style="background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.05);padding:12px;border-radius:8px;">'
#             f'<p style="margin:0;color:#64748B;font-size:9px;text-transform:uppercase;">Precision</p>'
#             f'<p style="margin:0;color:#FFFFFF;font-size:20px;font-weight:700;">87.2%</p>'
#             f'<p style="margin:0;color:#64748B;font-size:9px;">Validation score</p>'
#             f'</div>'
#             f'<div style="background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.05);padding:12px;border-radius:8px;">'
#             f'<p style="margin:0;color:#64748B;font-size:9px;text-transform:uppercase;">Recall</p>'
#             f'<p style="margin:0;color:#FFFFFF;font-size:20px;font-weight:700;">84.5%</p>'
#             f'<p style="margin:0;color:#64748B;font-size:9px;">Validation score</p>'
#             f'</div></div>'
#             f'<div style="background:rgba(34,197,94,.05);border:1px solid rgba(34,197,94,.15);padding:12px;border-radius:8px;display:flex;gap:10px;align-items:center;">'
#             f'<span style="color:#22C55E;display:inline-flex;">{shield_svg}</span>'
#             f'<div><p style="margin:0;color:#FFFFFF;font-size:12px;font-weight:600;">Total Records Analyzed</p>'
#             f'<p style="margin:0;color:#94A3B8;font-size:10px;">{metrics["total_patients"]:,} patient records processed</p></div>'
#             f'</div></div>',
#             unsafe_allow_html=True,
#         )

#     st.markdown("<div style='margin-top:30px;'></div>", unsafe_allow_html=True)

#     # ── KPI Cards ─────────────────────────────────────────────────────────────
#     c1, c2, c3, c4 = st.columns(4)
#     c1.markdown(kpi_card("Patients Analyzed",      f"{metrics['total_patients']:,}", "Total records processed",        "Users"),       unsafe_allow_html=True)
#     c2.markdown(kpi_card("Prediction Accuracy",    f"{metrics['accuracy']:.1f}%",  "Model performance",              "Target"),      unsafe_allow_html=True)
#     c3.markdown(kpi_card("Readmission Risk Cases", f"{metrics['readmission_cases']:,}",  "High-risk patients identified",  "ShieldAlert"), unsafe_allow_html=True)
#     c4.markdown(kpi_card("Model ROC-AUC",          f"{metrics['roc_auc']:.2f}",   "Classification effectiveness",   "TrendingUp"),  unsafe_allow_html=True)

#     st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)

#     # ── Charts row ────────────────────────────────────────────────────────────
#     c_left, c_right = st.columns(2)

#     with c_left:
#         st.markdown(chart_card_open("Patient Readmission Distribution"), unsafe_allow_html=True)
#         theme = get_plotly_theme()
#         fig = go.Figure(go.Pie(
#             labels=["Not Readmitted", "Readmitted"],
#             values=[72, 28], hole=.6,
#             marker=dict(colors=["#0F172A", "#F97316"], line=dict(color="#FFFFFF", width=2)),
#         ))
#         fig.update_traces(textinfo="percent+label", textfont_size=11,
#                           textfont_family="Inter, sans-serif", textposition="outside",
#                           textfont_color=theme["text"])
#         fig.update_layout(**theme["base"], showlegend=False, margin=dict(t=10,b=10,l=10,r=10), height=260)
#         st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CFG)
#         st.markdown(CHART_CARD_CLOSE, unsafe_allow_html=True)

#     with c_right:
#         st.markdown(chart_card_open("Risk Category Distribution"), unsafe_allow_html=True)
#         theme = get_plotly_theme()
#         fig = go.Figure(go.Bar(
#             x=["Low Risk", "Medium Risk", "High Risk"],
#             y=[7458, 3753, 1247],
#             marker_color=["#22C55E", "#FB923C", "#EF4444"], width=0.45,
#         ))
#         fig.update_layout(**theme["base"], margin=dict(t=20,b=10,l=40,r=20), height=260,
#                           xaxis=theme["xaxis_cat"], yaxis=theme["axis_style"])
#         st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CFG)
#         st.markdown(CHART_CARD_CLOSE, unsafe_allow_html=True)

#     # ── Feature Importance ────────────────────────────────────────────────────
#     st.markdown(chart_card_open("Top Factors Influencing Readmission"), unsafe_allow_html=True)
#     theme = get_plotly_theme()
#     feats = ["Insulin Usage", "Age Group", "Number of Diagnoses", "Number of Medications", "Time in Hospital", "Previous Admissions"]
#     imps  = [0.07, 0.11, 0.14, 0.18, 0.22, 0.28]
#     fig = go.Figure(go.Bar(y=feats, x=imps, orientation="h", marker_color="#F97316", width=0.55))
#     fig.update_layout(
#         **theme["base"], margin=dict(t=10,b=10,l=160,r=20), height=280,
#         xaxis=dict(**theme["axis_style"], title=dict(text="Relative Importance Score",
#                    font=dict(family="Inter, sans-serif", size=11, color=theme["text_secondary"]))),
#         yaxis=dict(showgrid=False, linecolor=theme["axis"],
#                    tickfont=dict(family="Inter, sans-serif", size=12, color=theme["text"])),
#     )
#     st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CFG)
#     st.markdown(CHART_CARD_CLOSE, unsafe_allow_html=True)

#     # ── Clinical Insights ─────────────────────────────────────────────────────
#     st.markdown("<h3 style='margin:20px 0 15px;font-size:18px;font-weight:600;'>Clinical Insights</h3>",
#                 unsafe_allow_html=True)
#     c1, c2, c3 = st.columns(3)
#     c1.markdown(insight_card("Extended Hospital Stay",
#         "Patients with longer hospital stays demonstrate a significantly higher probability of readmission.", "Clock"),
#         unsafe_allow_html=True)
#     c2.markdown(insight_card("Multiple Diagnoses Impact",
#         "Patients with multiple diagnoses show elevated readmission risk compared to single-condition cases.", "ClipboardList"),
#         unsafe_allow_html=True)
#     c3.markdown(insight_card("Frequent Inpatient Visits",
#         "Repeated inpatient admissions strongly correlate with future readmission events.", "Activity"),
#         unsafe_allow_html=True)

#     render_footer()


# # ══════════════════════════════════════════════════════════════════════════════
# # PAGE: PREDICTION
# # ══════════════════════════════════════════════════════════════════════════════
# elif st.session_state.selected_page == "Prediction":

#     biotech_icon = (
#         "<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' "
#         "fill='none' stroke='#FFFFFF' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>"
#         "<path d='M12 2a10 10 0 1 0 10 10 4 4 0 0 1-5-5 4 4 0 0 1-5-5'/><path d='M8.5 8.5v.01'/><path d='M16 15.5v.01'/><path d='M12 12v.01'/><path d='M11 17v.01'/></svg>"
#     )
#     st.markdown(page_header_card(
#         "Patient Readmission Risk Predictor",
#         "Enter clinical parameters to evaluate real-time patient readmission risk and generate decision support recommendations.",
#         biotech_icon
#     ), unsafe_allow_html=True)

#     col_form, col_result = st.columns([1, 1])

#     with col_form:
#         st.markdown('<div class="premium-card"><h4 style="margin:0 0 16px;font-size:15px;font-weight:600;color:#0F172A;border-bottom:1px solid #F1F5F9;padding-bottom:10px;">Patient Parameters</h4>',
#                     unsafe_allow_html=True)
#         ca, cg = st.columns(2)
#         with ca:
#             age_group = st.selectbox("Age Group", ["<30", "30-49", "50-69", "70-79", "80+"], index=2)
#         with cg:
#             gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
#         time_hospital = st.slider("Time in Hospital (Days)", 1, 14, 4)
#         num_diagnoses = st.slider("Number of Diagnoses", 1, 16, 5)
#         num_meds      = st.slider("Number of Medications", 1, 80, 15)
#         num_inpatient = st.slider("Previous Inpatient Visits (Prior Year)", 0, 10, 1)
#         ci, cd = st.columns(2)
#         with ci:
#             insulin  = st.selectbox("Insulin Usage", ["No", "Steady", "Up", "Down"], index=1)
#         with cd:
#             diab_med = st.radio("Diabetes Medication", ["Yes", "No"], horizontal=True)
#         st.markdown('</div>', unsafe_allow_html=True)

#         # Add prominent predict button
#         predict_button = st.button(
#             "🔮 Predict Readmission Risk",
#             key="predict_button",
#             use_container_width=True,
#             type="primary"
#         )

#     with col_result:
#         # Initialize contribs as empty list before prediction
#         contribs = []
        
#         if predict_button:
#             # Show loading animation
#             with st.spinner("Analyzing patient parameters and generating risk prediction..."):
#                 import time
#                 time.sleep(1.5)  # Simulate processing time
                
#                 score = 15.0
#                 inpatient_contrib = min(num_inpatient * 12.0, 48.0); score += inpatient_contrib
#                 time_contrib      = min(time_hospital * 2.0, 18.0);  score += time_contrib
#                 diagnoses_contrib = min(num_diagnoses * 2.0, 16.0);  score += diagnoses_contrib
#                 meds_contrib      = min(num_meds * 0.25, 12.0);      score += meds_contrib
#                 age_contrib       = {"70-79": 4.0, "80+": 8.0, "<30": -2.0}.get(age_group, 0.0); score += age_contrib
#                 insulin_contrib   = 5.0 if insulin in ["Up","Down"] else (2.0 if insulin=="Steady" else 0.0); score += insulin_contrib
#                 if diab_med == "Yes": score += 3.0
#                 risk_score = max(5.0, min(95.0, score))

#                 # Populate contribs with feature contributions after prediction
#                 contribs = [
#                     ("Base Rate",                     15.0,               "#64748B"),
#                     (f"Inpatient (+{num_inpatient})",  inpatient_contrib,  "#EF4444" if inpatient_contrib > 0 else "#64748B"),
#                     (f"Hosp Days (+{time_hospital})",  time_contrib,       "#EF4444" if time_contrib > 0 else "#64748B"),
#                     (f"Diagnoses (+{num_diagnoses})",  diagnoses_contrib,  "#EF4444" if diagnoses_contrib > 0 else "#64748B"),
#                     (f"Medications (+{num_meds})",     meds_contrib,       "#EF4444" if meds_contrib > 0 else "#64748B"),
#                     (f"Age ({age_group})",             age_contrib,        "#EF4444" if age_contrib > 0 else ("#22C55E" if age_contrib < 0 else "#64748B")),
#                     (f"Insulin ({insulin})",           insulin_contrib,    "#EF4444" if insulin_contrib > 0 else "#64748B"),
#                 ]

#                 if risk_score < 30:
#                     risk_class, risk_color, risk_bg = "Low Risk",    "#22C55E", "#DCFCE7"
#                     directive = "Patient demonstrates low readmission probability. Standard discharge protocols and routine follow-up schedule are recommended."
#                 elif risk_score < 70:
#                     risk_class, risk_color, risk_bg = "Medium Risk", "#FB923C", "#FFEDD5"
#                     directive = "Patient demonstrates moderate readmission risk. Consider scheduling clinical telephone follow-up within 72 hours and review medication reconciliation."
#                 else:
#                     risk_class, risk_color, risk_bg = "High Risk",   "#EF4444", "#FEE2E2"
#                     directive = "Patient is at critical risk of readmission. Intensive TCM enrollment, medication counseling, and clinical contact within 48 hours are strongly advised."

#                 st.markdown(
#                     f'<div class="premium-card">'
#                     f'<h4 style="margin:0 0 16px;font-size:15px;font-weight:600;color:#0F172A;border-bottom:1px solid #F1F5F9;padding-bottom:10px;">Risk Scoring Engine Output</h4>'
#                     f'<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;margin-bottom:16px;">'
#                     f'<div><span style="font-size:11px;text-transform:uppercase;color:#64748B;font-weight:600;">Patient Risk Status</span>'
#                     f'<h2 style="margin:2px 0 0;color:{risk_color};font-size:32px;font-weight:800;">{risk_class}</h2></div>'
#                     f'<div style="background:{risk_bg};border:1px solid {risk_color}33;border-radius:8px;padding:10px 16px;text-align:center;">'
#                     f'<span style="font-size:10px;text-transform:uppercase;color:#64748B;font-weight:600;">Probability Score</span>'
#                     f'<p style="margin:0;color:{risk_color};font-size:24px;font-weight:800;">{risk_score:.1f}%</p>'
#                     f'</div></div>'
#                     f'<div style="background:#F8FAFC;border:1px solid #E2E8F0;padding:12px 16px;border-radius:8px;font-size:13px;line-height:1.5;color:#334155;">'
#                     f'<strong style="color:#0F172A;">Clinical Directives:</strong> {directive}'
#                     f'</div></div>',
#                     unsafe_allow_html=True,
#                 )

#                 theme = get_plotly_theme()
#                 fig_g = go.Figure(go.Indicator(
#                     mode="gauge+number", value=risk_score,
#                     domain={"x":[0,1],"y":[0,1]},
#                     gauge=dict(
#                         axis=dict(range=[0,100], tickwidth=1, tickcolor=theme["text_secondary"]),
#                         bar=dict(color=risk_color),
#                         bgcolor="#F1F5F9", borderwidth=1, bordercolor="#E2E8F0",
#                         steps=[{"range":[0,30],"color":"#DCFCE7"},
#                                {"range":[30,70],"color":"#FFEDD5"},
#                                {"range":[70,100],"color":"#FEE2E2"}],
#                         threshold=dict(line=dict(color="#EF4444",width=3),thickness=.75,value=70),
#                     ),
#                     number=dict(font=dict(color=theme["text"], family="Inter, sans-serif", size=24)),
#                 ))
#                 fig_g.update_layout(**theme["base"], height=200, margin=dict(t=10,b=10,l=30,r=30))

#                 st.markdown(chart_card_open("Risk Probability Gauge"), unsafe_allow_html=True)
#                 st.plotly_chart(fig_g, config=PLOTLY_CFG, use_container_width=True)
#                 st.markdown(CHART_CARD_CLOSE, unsafe_allow_html=True)

#                 # SHAP feature contribution chart (only shown after prediction)
#                 if contribs:
#                     fig_s = go.Figure(go.Bar(
#                         y=[c[0] for c in contribs], x=[c[1] for c in contribs],
#                         orientation="h", marker_color=[c[2] for c in contribs], width=.6,
#                         text=[f"+{c[1]:.1f}%" if c[1]>0 else f"{c[1]:.1f}%" for c in contribs],
#                         textposition="auto", textfont=dict(size=10, color="#FFFFFF"),
#                     ))
#                     fig_s.update_layout(
#                         **theme["base"],
#                         title=dict(text="Feature Impact Analysis (SHAP Approximation)",
#                                    font=dict(family="Inter, sans-serif", size=12, color=theme["text"])),
#                         margin=dict(t=30,b=10,l=140,r=20), height=260,
#                         xaxis=dict(**theme["axis_style"], title=dict(text="Contribution %",
#                                    font=dict(family="Inter, sans-serif", size=10, color=theme["text_secondary"]))),
#                         yaxis=dict(showgrid=False, linecolor=theme["axis"],
#                                    tickfont=dict(family="Inter, sans-serif", size=10, color=theme["text"])),
#                     )
#                     st.markdown(chart_card_open("Feature Impact Analysis (SHAP Approximation)"), unsafe_allow_html=True)
#                     st.plotly_chart(fig_s, use_container_width=True, config=PLOTLY_CFG)
#                     st.markdown(CHART_CARD_CLOSE, unsafe_allow_html=True)
#                 else:
#                     st.info("No feature contribution data available")

#         else:
#             # Show placeholder components when no prediction has been made
#             st.markdown(
#                 '<div class="premium-card">'
#                 '<h4 style="margin:0 0 16px;font-size:15px;font-weight:600;color:#0F172A;border-bottom:1px solid #F1F5F9;padding-bottom:10px;">Risk Scoring Engine Output</h4>'
#                 '<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;margin-bottom:16px;">'
#                 '<div><span style="font-size:11px;text-transform:uppercase;color:#64748B;font-weight:600;">Patient Risk Status</span>'
#                 '<h2 style="margin:2px 0 0;color:#94A3B8;font-size:32px;font-weight:800;">No Prediction</h2></div>'
#                 '<div style="background:#F1F5F9;border:1px solid #E2E8F0;border-radius:8px;padding:10px 16px;text-align:center;">'
#                 '<span style="font-size:10px;text-transform:uppercase;color:#64748B;font-weight:600;">Probability Score</span>'
#                 '<p style="margin:0;color:#94A3B8;font-size:24px;font-weight:800;">0.0%</p>'
#                 '</div></div>'
#                 '<div style="background:#F8FAFC;border:1px solid #E2E8F0;padding:12px 16px;border-radius:8px;font-size:13px;line-height:1.5;color:#64748B;">'
#                 '<strong style="color:#94A3B8;">Clinical Directives:</strong> No prediction generated yet. Enter patient parameters and click "Predict Readmission Risk" to generate risk assessment.'
#                 '</div></div>',
#                 unsafe_allow_html=True,
#             )

#             # Empty gauge placeholder
#             theme = get_plotly_theme()
#             fig_g_empty = go.Figure(go.Indicator(
#                 mode="gauge+number", value=0,
#                 domain={"x":[0,1],"y":[0,1]},
#                 gauge=dict(
#                     axis=dict(range=[0,100], tickwidth=1, tickcolor="#E2E8F0"),
#                     bar=dict(color="#E2E8F0"),
#                     bgcolor="#F1F5F9", borderwidth=1, bordercolor="#E2E8F0",
#                     steps=[{"range":[0,30],"color":"#F1F5F9"},
#                            {"range":[30,70],"color":"#F1F5F9"},
#                            {"range":[70,100],"color":"#F1F5F9"}],
#                 ),
#                 number=dict(font=dict(color="#94A3B8", family="Inter, sans-serif", size=24)),
#             ))
#             fig_g_empty.update_layout(**theme["base"], height=200, margin=dict(t=10,b=10,l=30,r=30))

#             st.markdown(chart_card_open("Risk Probability Gauge"), unsafe_allow_html=True)
#             st.plotly_chart(fig_g_empty, config=PLOTLY_CFG, use_container_width=True)
#             st.markdown(CHART_CARD_CLOSE, unsafe_allow_html=True)

#             # Empty feature impact chart placeholder
#             if not contribs:
#                 fig_s_empty = go.Figure(go.Bar(
#                     y=["Base Rate", "Inpatient", "Hosp Days", "Diagnoses", "Medications", "Age", "Insulin"],
#                     x=[0, 0, 0, 0, 0, 0, 0],
#                     orientation="h", marker_color="#E2E8F0", width=.6,
#                     text=["0%", "0%", "0%", "0%", "0%", "0%", "0%"],
#                     textposition="auto", textfont=dict(size=10, color="#94A3B8"),
#                 ))
#                 fig_s_empty.update_layout(
#                     **theme["base"],
#                     title=dict(text="Feature Impact Analysis (SHAP Approximation)",
#                                font=dict(family="Inter, sans-serif", size=12, color="#94A3B8")),
#                     margin=dict(t=30,b=10,l=140,r=20), height=260,
#                     xaxis=dict(**theme["axis_style"], title=dict(text="Contribution %",
#                                font=dict(family="Inter, sans-serif", size=10, color="#94A3B8"))),
#                     yaxis=dict(showgrid=False, linecolor="#E2E8F0",
#                                tickfont=dict(family="Inter, sans-serif", size=10, color="#94A3B8")),
#                 )
#                 st.markdown(chart_card_open("Feature Impact Analysis (SHAP Approximation)"), unsafe_allow_html=True)
#                 st.plotly_chart(fig_s_empty, use_container_width=True, config=PLOTLY_CFG)
#                 st.markdown(CHART_CARD_CLOSE, unsafe_allow_html=True)

#     render_footer()


# # ══════════════════════════════════════════════════════════════════════════════
# # PAGE: ANALYTICS
# # ══════════════════════════════════════════════════════════════════════════════
# elif st.session_state.selected_page == "Analytics":

#     bar_chart_icon = (
#         "<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' "
#         "fill='none' stroke='#FFFFFF' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>"
#         "<line x1='12' y1='20' x2='12' y2='10'/><line x1='18' y1='20' x2='18' y2='4'/><line x1='6' y1='20' x2='6' y2='16'/></svg>"
#     )
#     st.markdown(page_header_card(
#         "Deep-Dive Demographics & Clinical Analytics",
#         "Explore demographic attributes and clinical factors correlations with patient readmissions.",
#         bar_chart_icon
#     ), unsafe_allow_html=True)

#     def analytics_bar(x, y, color, title_y="Readmission Rate (%)"):
#         theme = get_plotly_theme()
#         fig = go.Figure(go.Bar(x=x, y=y, marker_color=color, width=0.5))
#         fig.update_layout(**theme["base"], margin=dict(t=20,b=10,l=40,r=20), height=280,
#                           xaxis=theme["xaxis_cat"],
#                           yaxis=dict(**theme["axis_style"], title=dict(text=title_y,
#                                      font=dict(family="Inter, sans-serif", size=10, color=theme["text_secondary"]))))
#         return fig

#     r1c1, r1c2 = st.columns(2)
#     with r1c1:
#         st.markdown(chart_card_open("Readmission Rate by Age Group"), unsafe_allow_html=True)
#         st.plotly_chart(analytics_bar(["<30","30-49","50-69","70-79","80+"],
#                                       [12.4,18.2,24.8,31.2,36.5], "#F97316"),
#                         use_container_width=True, config=PLOTLY_CFG)
#         st.markdown(CHART_CARD_CLOSE, unsafe_allow_html=True)

#     with r1c2:
#         st.markdown(chart_card_open("Time in Hospital vs Readmission Rate"), unsafe_allow_html=True)
#         theme = get_plotly_theme()
#         fig = go.Figure(go.Scatter(
#             x=list(range(1,15)),
#             y=[14.1,16.5,19.2,22.8,25.1,28.4,30.9,34.2,35.8,38.2,40.1,41.5,43.8,46.2],
#             mode="lines+markers",
#             line=dict(color="#0F172A", width=3),
#             marker=dict(size=8, color="#F97316", line=dict(color="#FFFFFF", width=2)),
#         ))
#         fig.update_layout(**theme["base"], margin=dict(t=20,b=10,l=40,r=20), height=280,
#                           xaxis=dict(**theme["xaxis_cat"], title=dict(text="Length of Stay (Days)",
#                                      font=dict(family="Inter, sans-serif", size=10, color=theme["text_secondary"]))),
#                           yaxis=dict(**theme["axis_style"], title=dict(text="Readmission Rate (%)",
#                                      font=dict(family="Inter, sans-serif", size=10, color=theme["text_secondary"]))))
#         st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CFG)
#         st.markdown(CHART_CARD_CLOSE, unsafe_allow_html=True)

#     r2c1, r2c2 = st.columns(2)
#     with r2c1:
#         st.markdown(chart_card_open("Prior Inpatient Admissions Influence"), unsafe_allow_html=True)
#         st.plotly_chart(analytics_bar(["0 Visits","1 Visit","2 Visits","3 Visits","4+ Visits"],
#                                       [12.1,28.5,44.2,58.7,72.4],
#                                       ["#0F172A","#F97316","#F97316","#F97316","#EF4444"]),
#                         use_container_width=True, config=PLOTLY_CFG)
#         st.markdown(CHART_CARD_CLOSE, unsafe_allow_html=True)

#     with r2c2:
#         st.markdown(chart_card_open("Readmission Rate by Diabetes Medication"), unsafe_allow_html=True)
#         st.plotly_chart(analytics_bar(["Prescribed Diabetes Med","No Diabetes Med"],
#                                       [30.4, 21.8], ["#F97316","#0F172A"]),
#                         use_container_width=True, config=PLOTLY_CFG)
#         st.markdown(CHART_CARD_CLOSE, unsafe_allow_html=True)

#     render_footer()


# # ══════════════════════════════════════════════════════════════════════════════
# # PAGE: MODEL PERFORMANCE
# # ══════════════════════════════════════════════════════════════════════════════
# elif st.session_state.selected_page == "Model Performance":

#     memory_icon = (
#         "<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' "
#         "fill='none' stroke='#FFFFFF' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>"
#         "<path d='M2 12h20'/><path d='M2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6'/><path d='M12 2L2 7l10 5 10-5-10-5'/><path d='M2 17l10 5 10-5'/></svg>"
#     )
#     st.markdown(page_header_card(
#         "Machine Learning Pipeline Evaluation",
#         "Review performance metrics, ROC-AUC curves, and confusion matrix diagnostics for all trained classifiers.",
#         memory_icon
#     ), unsafe_allow_html=True)

#     st.markdown('<div class="premium-card"><h4 style="margin:0 0 16px;font-size:15px;font-weight:600;color:#0F172A;border-bottom:1px solid #F1F5F9;padding-bottom:10px;">Model Comparison Metrics</h4>',
#                 unsafe_allow_html=True)
#     st.dataframe(pd.DataFrame({
#         "Classifier Model":   ["Random Forest", "Decision Tree", "Logistic Regression"],
#         "Accuracy":           ["89.7%", "82.4%", "78.5%"],
#         "Precision":          ["87.2%", "76.8%", "71.4%"],
#         "Recall":             ["84.5%", "72.1%", "68.9%"],
#         "F1-Score":           ["85.8%", "74.4%", "70.1%"],
#         "ROC-AUC":            ["0.91",  "0.84",  "0.81"],
#     }), hide_index=True, use_container_width=True)
#     st.markdown('</div>', unsafe_allow_html=True)

#     rc1, rc2 = st.columns(2)

#     with rc1:
#         st.markdown(chart_card_open("ROC-AUC Comparison Curves"), unsafe_allow_html=True)
#         theme = get_plotly_theme()
#         fpr = np.linspace(0, 1, 100)
#         fig = go.Figure()
#         fig.add_trace(go.Scatter(x=fpr, y=fpr**0.40, name="Random Forest (AUC=0.91)", line=dict(color="#F97316",width=3)))
#         fig.add_trace(go.Scatter(x=fpr, y=fpr**0.60, name="Decision Tree (AUC=0.84)",  line=dict(color="#0F172A",width=2)))
#         fig.add_trace(go.Scatter(x=fpr, y=fpr**0.70, name="Logistic Reg (AUC=0.81)",   line=dict(color="#64748B",width=2,dash="dash")))
#         fig.add_trace(go.Scatter(x=[0,1], y=[0,1],   name="Random Guess",               line=dict(color="#CBD5E1",width=1,dash="dot")))
#         fig.update_layout(
#             **theme["base"], margin=dict(t=20,b=20,l=40,r=20), height=300,
#             xaxis=dict(**theme["axis_style"], title=dict(text="False Positive Rate", font=dict(size=10,color=theme["text_secondary"]))),
#             yaxis=dict(**theme["axis_style"], title=dict(text="True Positive Rate",  font=dict(size=10,color=theme["text_secondary"]))),
#             legend=dict(x=0.45, y=0.15, font=dict(size=10, color=theme["text"])),
#         )
#         st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CFG)
#         st.markdown(CHART_CARD_CLOSE, unsafe_allow_html=True)

#     with rc2:
#         st.markdown(chart_card_open("Confusion Matrix (Best Model: Random Forest)"), unsafe_allow_html=True)
#         theme = get_plotly_theme()
#         fig = px.imshow(
#             [[7850, 810],[420, 3378]],
#             labels=dict(x="Predicted", y="Actual"),
#             x=["Not Readmitted","Readmitted"], y=["Not Readmitted","Readmitted"],
#             color_continuous_scale=[[0,"#F8FAFC"],[0.1,"#FFE0CC"],[1,"#F97316"]],
#             text_auto=True,
#         )
#         fig.update_layout(**theme["base"], margin=dict(t=20,b=20,l=40,r=20), height=300, coloraxis_showscale=False,
#                           xaxis=dict(tickfont=dict(family="Inter, sans-serif", size=11, color=theme["text"])),
#                           yaxis=dict(tickfont=dict(family="Inter, sans-serif", size=11, color=theme["text"])))
#         st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CFG)
#         st.markdown(CHART_CARD_CLOSE, unsafe_allow_html=True)

#     render_footer()


# # ══════════════════════════════════════════════════════════════════════════════
# # PAGE: ABOUT
# # ══════════════════════════════════════════════════════════════════════════════
# elif st.session_state.selected_page == "About":

#     info_icon = (
#         "<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' "
#         "fill='none' stroke='#FFFFFF' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>"
#         "<circle cx='12' cy='12' r='10'/><line x1='12' y1='16' x2='12' y2='12'/><line x1='12' y1='8' x2='12.01' y2='8'/></svg>"
#     )
#     st.markdown(page_header_card(
#         "About the Clinical Analytics Engine",
#         "Medical background, model architecture, training process, and clinical integration guidelines.",
#         info_icon
#     ), unsafe_allow_html=True)

#     # System Workflow Diagram
#     st.markdown('<div class="premium-card"><h4 style="margin:0 0 16px;font-size:15px;font-weight:600;color:#0F172A;border-bottom:1px solid #F1F5F9;padding-bottom:10px;">System Workflow</h4>',
#                 unsafe_allow_html=True)
    
#     workflow_html = '''
#     <div style="display:flex;align-items:center;justify-content:center;gap:8px;padding:20px 0;flex-wrap:wrap;">
#         <div style="background:#F97316;color:white;padding:8px 16px;border-radius:6px;font-size:12px;font-weight:600;">Patient Data</div>
#         <div style="color:#F97316;font-size:18px;">→</div>
#         <div style="background:#0F172A;color:white;padding:8px 16px;border-radius:6px;font-size:12px;font-weight:600;">Preprocessing</div>
#         <div style="color:#F97316;font-size:18px;">→</div>
#         <div style="background:#0F172A;color:white;padding:8px 16px;border-radius:6px;font-size:12px;font-weight:600;">Feature Engineering</div>
#         <div style="color:#F97316;font-size:18px;">→</div>
#         <div style="background:#0F172A;color:white;padding:8px 16px;border-radius:6px;font-size:12px;font-weight:600;">SMOTE</div>
#         <div style="color:#F97316;font-size:18px;">→</div>
#         <div style="background:#F97316;color:white;padding:8px 16px;border-radius:6px;font-size:12px;font-weight:600;">Random Forest</div>
#         <div style="color:#F97316;font-size:18px;">→</div>
#         <div style="background:#0F172A;color:white;padding:8px 16px;border-radius:6px;font-size:12px;font-weight:600;">Risk Prediction</div>
#         <div style="color:#F97316;font-size:18px;">→</div>
#         <div style="background:#22C55E;color:white;padding:8px 16px;border-radius:6px;font-size:12px;font-weight:600;">Clinical Recommendation</div>
#     </div>
#     '''
#     st.markdown(workflow_html, unsafe_allow_html=True)
#     st.markdown('</div>', unsafe_allow_html=True)

#     st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)

#     # KPI Cards
#     k1, k2, k3, k4, k5, k6 = st.columns(6)
    
#     def kpi_small(label, value, color="#F97316"):
#         return f'<div style="background:{color}15;border:1px solid {color}30;padding:12px;border-radius:8px;text-align:center;"><p style="margin:0;color:#64748B;font-size:10px;text-transform:uppercase;">{label}</p><p style="margin:4px 0 0;color:{color};font-size:18px;font-weight:700;">{value}</p></div>'
    
#     k1.markdown(kpi_small("Dataset Size", "50K+", "#F97316"), unsafe_allow_html=True)
#     k2.markdown(kpi_small("Clinical Features", "50+", "#0F172A"), unsafe_allow_html=True)
#     k3.markdown(kpi_small("Accuracy", "89.7%", "#22C55E"), unsafe_allow_html=True)
#     k4.markdown(kpi_small("ROC-AUC", "0.91", "#22C55E"), unsafe_allow_html=True)
#     k5.markdown(kpi_small("Best Model", "RF", "#F97316"), unsafe_allow_html=True)
#     k6.markdown(kpi_small("Target", "Readmission", "#0F172A"), unsafe_allow_html=True)

#     st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)

#     # Architecture and Why Random Forest
#     ac1, ac2 = st.columns(2)

#     def about_card(title, body_html):
#         return (
#             f'<div class="premium-card" style="min-height:320px;">'
#             f'<h4 style="margin:0 0 12px;font-size:15px;font-weight:600;color:#0F172A;'
#             f'border-bottom:1px solid #F1F5F9;padding-bottom:8px;">{title}</h4>'
#             f'{body_html}</div>'
#         )

#     ac1.markdown(about_card("Project Architecture",
#         '<div style="font-size:13px;line-height:1.6;color:#64748B;">'
#         '<div style="display:flex;flex-direction:column;gap:12px;">'
#         '<div style="display:flex;align-items:center;gap:8px;">'
#         '<div style="background:#F97316;color:white;padding:6px 12px;border-radius:4px;font-size:11px;font-weight:600;">Streamlit</div>'
#         '<div style="color:#F97316;">→</div>'
#         '<div style="background:#0F172A;color:white;padding:6px 12px;border-radius:4px;font-size:11px;">ML Model</div>'
#         '</div>'
#         '<div style="display:flex;align-items:center;gap:8px;">'
#         '<div style="background:#0F172A;color:white;padding:6px 12px;border-radius:4px;font-size:11px;">Saved Artifacts</div>'
#         '<div style="color:#F97316;">→</div>'
#         '<div style="background:#22C55E;color:white;padding:6px 12px;border-radius:4px;font-size:11px;font-weight:600;">Prediction Engine</div>'
#         '</div>'
#         '<p style="margin:8px 0 0;font-size:12px;color:#64748B;"><strong>Frontend:</strong> Streamlit UI with real-time predictions</p>'
#         '<p style="margin:4px 0;font-size:12px;color:#64748B;"><strong>Backend:</strong> Random Forest model with SHAP explainability</p>'
#         '<p style="margin:4px 0;font-size:12px;color:#64748B;"><strong>Storage:</strong> Pickle artifacts for model persistence</p>'
#         '</div></div>'),
#         unsafe_allow_html=True)

#     ac2.markdown(about_card("Why Random Forest?",
#         '<div style="font-size:13px;line-height:1.6;color:#64748B;">'
#         '<ul style="margin:0;padding-left:16px;">'
#         '<li style="margin-bottom:8px;"><strong style="color:#F97316;">Handles mixed data types</strong> - No extensive preprocessing needed</li>'
#         '<li style="margin-bottom:8px;"><strong style="color:#F97316;">Feature importance</strong> - Built-in SHAP interpretability</li>'
#         '<li style="margin-bottom:8px;"><strong style="color:#F97316;">Robust to outliers</strong> - Less sensitive to extreme values</li>'
#         '<li style="margin-bottom:8px;"><strong style="color:#F97316;">Non-linear relationships</strong> - Captures complex patterns</li>'
#         '<li style="margin-bottom:8px;"><strong style="color:#F97316;">Ensemble method</strong> - Reduces overfitting risk</li>'
#         '<li><strong style="color:#F97316;">Fast inference</strong> - Real-time prediction capability</li>'
#         '</ul></div>'),
#         unsafe_allow_html=True)

#     render_footer()
