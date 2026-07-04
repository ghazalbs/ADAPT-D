"""
app.py — Main entry point
─────────────────────────
Trajectory-Aware AI Decision Support for Dementia Discharge Planning
Research prototype · Synthetic data only · Not for clinical use.

Run:
    streamlit run app.py
"""

import os
import sys
import streamlit as st
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIGURATION  (must be first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Trajectory-Aware AI — Dementia Discharge Support",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import DASHBOARD_TITLE, DASHBOARD_SUBTITLE, DISCLAIMER, MODEL_FRAMING
from data_loader import load_patients, load_shap, load_threshold_performance, load_fairness
from banner_asset import BANNER_DATA_URI  # hero banner artwork (base64 data URI)

# ─────────────────────────────────────────────────────────────────────────────
# PLOTLY THEME — centralised light template for ALL charts
# ─────────────────────────────────────────────────────────────────────────────
# Every Plotly figure in this app inherits this template, so chart titles, axis
# titles, tick labels, legends, and hover labels are forced dark-on-white and
# stay readable regardless of the visitor's browser/OS dark-mode setting.
# Individual figures may still override family/size; colours come from here.

pio.templates["adaptd"] = go.layout.Template(
    layout=go.Layout(
        font=dict(color="#1a202c", family="Inter, 'Segoe UI', Arial, sans-serif"),
        title=dict(font=dict(color="#1a202c")),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        xaxis=dict(
            title=dict(font=dict(color="#1a202c")),
            tickfont=dict(color="#2d3748"),
            linecolor="#cbd5e0",
        ),
        yaxis=dict(
            title=dict(font=dict(color="#1a202c")),
            tickfont=dict(color="#2d3748"),
            linecolor="#cbd5e0",
        ),
        legend=dict(font=dict(color="#1a202c")),
        hoverlabel=dict(
            font=dict(color="#1a202c", family="Inter, 'Segoe UI', Arial, sans-serif"),
            bgcolor="#ffffff",
            bordercolor="#cbd5e0",
        ),
    )
)
# Compose on top of plotly_white (white background + light grid) so every chart
# is consistently light with dark, legible text.
pio.templates.default = "plotly_white+adaptd"

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS — professional healthcare analytics look
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
/* ── Force light mode — overrides OS/browser dark-mode preference ── */
:root {
  color-scheme: light;
  --clr-text-primary:   #1a202c;
  --clr-text-secondary: #4a5568;
  --clr-text-muted:     #718096;
  --clr-bg-primary:     #ffffff;
  --clr-bg-secondary:   #f7fafc;
  --clr-bg-page:        #f0f4f8;
  --clr-border:         #e2e8f0;
  --clr-border-subtle:  #f0f4f8;
}

/* ── Typography ── */
html, body, [class*="css"] {
  font-family: 'Segoe UI', 'Inter', Arial, sans-serif;
  font-weight: 400;
}

/* ── Page background — force light everywhere, ignore OS/browser dark mode ── */
html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
  background-color: var(--clr-bg-page) !important;
  color: var(--clr-text-primary) !important;
}
.main { background-color: var(--clr-bg-page); }
.block-container { color: var(--clr-text-primary); }

/* Default dark text for body copy, headings, markdown, captions, list items.
   (Scoped to the main area so the navy sidebar below keeps its white text.) */
[data-testid="stMain"] h1,
[data-testid="stMain"] h2,
[data-testid="stMain"] h3,
[data-testid="stMain"] h4,
[data-testid="stMain"] h5,
[data-testid="stMain"] h6,
[data-testid="stMain"] p,
[data-testid="stMain"] li,
[data-testid="stMain"] label,
[data-testid="stMain"] .stMarkdown,
[data-testid="stCaptionContainer"] {
  color: var(--clr-text-primary) !important;
}

/* Widget labels (selectbox / slider / etc.) in the main area — keep dark */
[data-testid="stMain"] [data-testid="stWidgetLabel"] label,
[data-testid="stMain"] .stSelectbox label,
[data-testid="stMain"] .stSlider label {
  color: var(--clr-text-secondary) !important;
}

/* Selectbox / dropdown — dark text on white field */
[data-testid="stMain"] div[data-baseweb="select"] > div {
  background-color: var(--clr-bg-primary) !important;
  color: var(--clr-text-primary) !important;
}
[data-testid="stMain"] div[data-baseweb="select"] * { color: var(--clr-text-primary) !important; }
div[data-baseweb="popover"] li { color: var(--clr-text-primary) !important; }

/* Dataframes / tables — dark text on white */
[data-testid="stDataFrame"], [data-testid="stTable"] {
  color: var(--clr-text-primary) !important;
  background-color: var(--clr-bg-primary) !important;
}
[data-testid="stDataFrame"] * { color: var(--clr-text-primary); }

/* Expander header text */
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary * { color: var(--clr-text-primary) !important; }

/* ── Sidebar (intentionally navy with white text) ── */
section[data-testid="stSidebar"] { background: #1a3a5c; }
section[data-testid="stSidebar"] * { color: white !important; }
section[data-testid="stSidebar"] .stSelectbox label { color: #cbd5e0 !important; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, [data-testid="stHeader"] { visibility: hidden; }
.block-container { padding-top: 0.5rem; padding-bottom: 2rem; }

/* ── Tab strip ── */
.stTabs [data-baseweb="tab-list"] {
  gap: 4px;
  background: transparent;
  padding-bottom: 2px;
}
.stTabs [data-baseweb="tab"] {
  background: var(--clr-bg-primary);
  border-radius: 6px 6px 0 0;
  padding: 0.42rem 0.85rem;
  font-size: 0.82rem;
  font-weight: 500;
  border: 1px solid var(--clr-border);
  border-bottom: none;
  color: var(--clr-text-secondary);
  white-space: nowrap;
}
.stTabs [aria-selected="true"] {
  background: #1a3a5c !important;
  color: #ffffff !important;
  border-color: #1a3a5c !important;
}

/* ── Sankey node labels — crisp dark text, no white halo/outline/shadow ── */
.js-plotly-plot text.node-label,
.js-plotly-plot .node-label,
.js-plotly-plot .sankey text {
  text-shadow: none !important;
  stroke: none !important;
  paint-order: normal !important;
}
.js-plotly-plot text.node-label { fill: #111827 !important; }

/* ── Inputs ── */
.stSelectbox > div > div { border-radius: 6px; }
.stSlider { padding: 0; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--clr-bg-page); }
::-webkit-scrollbar-thumb { background: var(--clr-border); border-radius: 3px; }

/* ── Hero header (full-bleed navy→blue gradient) ── */
.stApp { overflow-x: hidden; }                 /* guard against 100vw scrollbar */

.dash-hero {
  position: relative;
  overflow: hidden;
  width: 100vw;
  left: 50%;
  margin-left: -50vw;
  margin-top: -0.5rem;                          /* reach the very top edge */
  margin-bottom: 1rem;
  padding: 2.35rem clamp(1.5rem, 4vw, 3.25rem) 2.35rem;
  color: #ffffff;
  background: linear-gradient(115deg, #122c49 0%, #1b4068 46%, #2356a3 88%, #2563eb 120%);
  box-shadow: 0 8px 22px rgba(18,44,73,0.22);
}
/* decorative circuit/network art — faint corner texture, never affects layout
   (absolutely positioned, behind the row) and stays out of the badges' way */
.dash-hero-art {
  position: absolute;
  top: 0; right: 0; bottom: 0;
  width: 26%;
  opacity: 0.13;
  pointer-events: none;
}
.dash-hero-row {
  position: relative;
  z-index: 1;                                   /* always above the decorative art */
  display: flex;
  align-items: center;
  gap: 22px;
  width: 100%;                                   /* span full hero width so badges
                                                    anchor to the true right edge
                                                    (no centred max-width cap) */
}
.dash-hero-icon {
  width: 74px; height: 74px;
  border-radius: 18px;
  background: rgba(255,255,255,0.11);
  border: 1px solid rgba(255,255,255,0.24);
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.16), 0 3px 10px rgba(0,0,0,0.14);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.dash-hero-text { flex: 1; min-width: 0; }
.dash-hero-brand {
  font-size: 2.25rem;
  font-weight: 800;
  letter-spacing: 0.5px;
  line-height: 1.04;
  margin: 0;
  color: #ffffff;
}
.dash-hero-fulltitle {
  font-size: 1.06rem;
  font-weight: 600;
  color: #e8f1fb;
  margin-top: 0.3rem;
  line-height: 1.35;
}
.dash-hero-subtitle {
  font-size: 0.95rem;
  font-style: italic;
  color: #cfe2f8;
  margin-top: 0.2rem;
  font-weight: 500;
}
.dash-hero-framing {
  display: flex; align-items: center; gap: 8px;
  font-size: 0.79rem;
  color: rgba(233,241,251,0.78);
  margin-top: 0.75rem;
  font-weight: 400;
}
.dash-hero-framing svg { flex-shrink: 0; opacity: 0.85; }
.dash-hero-badges {
  flex-shrink: 0;
  margin-left: auto;                             /* push the stack to the far right */
  padding-left: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: stretch;                          /* equal-width pills = clean stack */
  gap: 10px;
}
.dash-pill {
  display: inline-flex; align-items: center; gap: 8px;
  justify-content: flex-start;
  font-size: 0.79rem;
  font-weight: 600;
  padding: 7px 16px;
  border-radius: 9999px;
  background: rgba(255,255,255,0.13);
  border: 1px solid rgba(255,255,255,0.26);
  color: #ffffff;
  white-space: nowrap;
}
.dash-pill svg { flex-shrink: 0; opacity: 0.92; }

@media (max-width: 900px) {
  .dash-hero-row { flex-direction: column; align-items: flex-start; }
  .dash-hero-badges { flex-direction: row; flex-wrap: wrap; align-items: flex-start; }
  .dash-hero-brand { font-size: 1.85rem; }
  .dash-hero-art { display: none; }
}

/* ── Amber research-prototype banner (compact, inset card) ── */
.dash-alert-bar {
  display: flex; align-items: flex-start; gap: 11px;
  background: #fef7e6;
  border: 1px solid #f3d68a;
  border-radius: 10px;
  padding: 0.75rem 1.15rem;
  margin: 0 0 1rem 0;
}
.dash-alert-bar svg { flex-shrink: 0; margin-top: 1px; }
.dash-alert-text {
  color: #6f5300;
  font-size: 0.82rem;
  font-weight: 400;
  line-height: 1.55;
}
.dash-alert-text strong { color: #5a4205; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# LOAD DATA  (each loader is cached; validation happens inside data_loader.py)
# ─────────────────────────────────────────────────────────────────────────────

patients_df  = load_patients()
shap_df      = load_shap()
threshold_df = load_threshold_performance()
fairness_df  = load_fairness()

# Convenience alias kept for the header patient count
df = patients_df

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────

if "selected_patient_id" not in st.session_state:
    st.session_state["selected_patient_id"] = patients_df["dashboard_patient_id"].iloc[0]

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────

# Split the full title into the brand ("ADAPT-D") and its descriptive expansion.
_brand, _, _descriptor = DASHBOARD_TITLE.partition(": ")
_descriptor = _descriptor or DASHBOARD_TITLE

# Bold the first sentence of the disclaimer for the amber banner.
_disclaimer_clean = DISCLAIMER.replace("⚠️", "").strip()
_first, _sep, _rest = _disclaimer_clean.partition(". ")
_banner_html = f"<strong>{_first}.</strong> {_rest}" if _sep else _disclaimer_clean

# Reusable small SVG (white people glyph) for badges / framing line.
_people_svg = (
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#ffffff" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>'
    '<path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'
)

st.markdown(f"""
<style>
/* Hero banner artwork (Higgsfield, 21:5) layered under a left scrim so the
   text column stays readable. The banner's brain/pathway art begins ~37% from
   the left, so text is confined to the dark left zone and badges to the
   lower-left; the prior inline SVG art + brain-icon tile are dropped (the
   banner now carries that imagery). */
.dash-hero {{
  background:
    linear-gradient(90deg, rgba(9,19,35,0.94) 0%, rgba(9,19,35,0.86) 30%,
                    rgba(9,19,35,0.34) 47%, rgba(9,19,35,0) 62%),
    url({BANNER_DATA_URI}) center / cover no-repeat,
    linear-gradient(115deg, #122c49 0%, #1b4068 46%, #2356a3 88%, #2563eb 120%);
  min-height: 220px;
}}
.dash-hero-row {{
  flex-direction: column;
  align-items: stretch;
  justify-content: space-between;
  gap: 16px;
  min-height: 176px;
}}
.dash-hero-text {{ flex: none; max-width: 36%; }}
.dash-hero-brand {{ text-shadow: 0 1px 12px rgba(6,16,30,0.92); }}
.dash-hero-fulltitle,
.dash-hero-subtitle,
.dash-hero-framing {{ text-shadow: 0 1px 9px rgba(6,16,30,0.94); }}
.dash-hero-badges {{
  margin-left: 0;
  padding-left: 0;
  flex-direction: row;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  max-width: 62%;
}}
.dash-pill {{
  background: rgba(9,20,36,0.58);
  border: 1px solid rgba(103,232,249,0.30);
  backdrop-filter: blur(3px);
}}
@media (max-width: 900px) {{
  .dash-hero-text {{ max-width: 100%; }}
  .dash-hero-badges {{ max-width: 100%; }}
}}
</style>
<div class="dash-hero">
  <div class="dash-hero-row">
    <div class="dash-hero-text">
      <div class="dash-hero-brand">{_brand}</div>
      <div class="dash-hero-fulltitle">{_descriptor}</div>
      <div class="dash-hero-subtitle">{DASHBOARD_SUBTITLE}</div>
      <div class="dash-hero-framing">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#e8f1fb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>
          <path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>
        </svg>
        <span>{MODEL_FRAMING}</span>
      </div>
    </div>
    <div class="dash-hero-badges">
      <span class="dash-pill">{_people_svg}N = {len(df)} synthetic patients</span>
      <span class="dash-pill">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M22 10L12 5 2 10l10 5 10-5z"/><path d="M6 12v5c0 1 2 3 6 3s6-2 6-3v-5"/>
        </svg>Academic research prototype</span>
      <span class="dash-pill">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
        </svg>Privacy-preserving demonstration</span>
    </div>
  </div>
</div>
<div class="dash-alert-bar">
  <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#b7791f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
    <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
  </svg>
  <span class="dash-alert-text">{_banner_html}</span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────

tab_labels = [
    "ℹ️ About / How to interpret",
    "👥 Population insights",
    "🧑‍⚕️ Patient risk summary",
    "🔍 Key drivers",
    "📋 Planning support",
    "⚖️ Equity & reliability",
    "📈 Model performance",
]

(tab_about, tab_pop, tab1, tab3, tab4, tab7, tab8) = st.tabs(tab_labels)

from tabs.tab_about              import render_tab_about
from tabs.tab_population_insights import render_tab_population_insights
from tabs.tab1_patient_risk       import render_tab1
from tabs.tab3_explainability     import render_tab3
from tabs.tab4_decision_support   import render_tab4
from tabs.tab7_equity_monitoring  import render_tab7
from tabs.tab8_model_performance  import render_tab8

with tab_about: render_tab_about(n_patients=len(df))
with tab_pop:   render_tab_population_insights(patients_df)
with tab1:      render_tab1(patients_df)
with tab3:      render_tab3(patients_df, shap_df)
with tab4:      render_tab4(patients_df)
with tab7:      render_tab7(patients_df, fairness_df)
with tab8:      render_tab8(threshold_df)
