"""
tab_about.py — About / How to Interpret
────────────────────────────────────────
Plain-language orientation for researchers visiting the ADAPT-D dashboard.

Explains what ADAPT-D is, what the model predicts, the difference between the
underlying predictive models (developed/evaluated on a large retrospective
dementia cohort) and the 100 synthetic prototype patients displayed here, and
how to interpret each tab.

All wording is intentionally cautious. Do not strengthen the claims.
"""

import streamlit as st

# Shared text colours (match the fixed light theme used across the dashboard)
_HEADING = "#1a365d"
_BODY    = "#2d3748"
_MUTED   = "#4a5568"


def _section(title: str, body_html: str, accent: str = "#2563eb") -> None:
    """Render one titled white card with dark, readable body text."""
    st.markdown(
        f'<div style="background:#ffffff;border:1px solid #e2e8f0;'
        f'border-left:4px solid {accent};border-radius:8px;'
        f'padding:1.1rem 1.4rem;margin-bottom:1rem;">'
        f'<div style="font-size:1.0rem;font-weight:700;color:{_HEADING};'
        f'margin-bottom:0.5rem;">{title}</div>'
        f'<div style="font-size:0.88rem;color:{_BODY};line-height:1.7;">'
        f'{body_html}</div></div>',
        unsafe_allow_html=True,
    )


def render_tab_about(n_patients: int = 100) -> None:
    # ── Intro banner ──────────────────────────────────────────────────────────
    st.markdown(
        f'<div style="background:linear-gradient(135deg,#1a3a5c,#2b5378);'
        f'border-radius:10px;padding:1.3rem 1.6rem;margin-bottom:1.2rem;color:#ffffff;">'
        f'<div style="font-size:1.15rem;font-weight:700;margin-bottom:0.3rem;">'
        f'About this dashboard &nbsp;·&nbsp; How to interpret it</div>'
        f'<div style="font-size:0.9rem;color:#dbe7f3;line-height:1.65;">'
        f'ADAPT-D (ALC and Dementia Analytics for Predicted Trajectories and Destinations) '
        f'is a research prototype. Please read this page before interpreting the other tabs.'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    # ── What is ADAPT-D? ──────────────────────────────────────────────────────
    _section(
        "What is ADAPT-D?",
        "ADAPT-D is a research prototype dashboard designed to demonstrate how "
        "trajectory-aware prediction models could support dementia discharge planning. "
        "The dashboard focuses on ALC/DHD-related care pathways and high-need discharge "
        "trajectories.<br><br>"
        "The underlying predictive models were developed and evaluated using a large "
        "retrospective dementia cohort, including more than <strong>300,000 patients</strong> "
        "and over <strong>2 million records</strong>. Model performance, threshold behaviour, "
        "and equity/reliability results are summarised in the corresponding dashboard tabs.<br><br>"
        "For privacy-preserving demonstration, the interactive dashboard does <strong>not</strong> "
        f"display real patient records. Instead, it uses <strong>{n_patients} synthetic prototype "
        "patients</strong> to illustrate how predicted trajectory risks, SHAP-based key drivers, "
        "and dashboard visualizations could be presented to users.",
    )

    # ── Models vs. dashboard data (key distinction) ───────────────────────────
    st.markdown(
        f'<div style="background:#fffbeb;border:1px solid #f6d98a;'
        f'border-left:4px solid #d69e2e;border-radius:8px;'
        f'padding:1.1rem 1.4rem;margin-bottom:1rem;">'
        f'<div style="font-size:1.0rem;font-weight:700;color:#744210;'
        f'margin-bottom:0.5rem;">An important distinction</div>'
        f'<ul style="font-size:0.88rem;color:#5b4410;line-height:1.7;margin:0;padding-left:1.1rem;">'
        f'<li>The predictive models were <strong>trained and evaluated using a large dementia '
        f'cohort</strong>.</li>'
        f'<li>The <strong>performance</strong> and <strong>fairness/reliability</strong> results '
        f'come from the model development and evaluation analyses.</li>'
        f'<li>The individual patient examples shown in the dashboard are '
        f'<strong>synthetic prototype patients</strong>.</li>'
        f'<li>The SHAP / key-driver visualizations for the prototype patients illustrate how '
        f'model explanations <em>could</em> be displayed.</li>'
        f'<li>The Population Insights tab summarises only the {n_patients} synthetic prototype '
        f'patients, so it should be interpreted very cautiously and <strong>not</strong> as a true '
        f'population-level estimate.</li>'
        f'</ul></div>',
        unsafe_allow_html=True,
    )

    # ── What does the model predict? ──────────────────────────────────────────
    _section(
        "What does the model predict?",
        "For each synthetic patient shown in the dashboard, ADAPT-D displays "
        "model-estimated probabilities for four possible post-hospitalization trajectories:"
        '<ol style="margin:0.5rem 0 0.5rem 0;padding-left:1.2rem;">'
        '<li><strong>ALC: Community Return</strong></li>'
        '<li><strong>ALC: High Need</strong></li>'
        '<li><strong>Non-ALC: Community-Oriented</strong></li>'
        '<li><strong>Non-ALC: High Need</strong></li>'
        '</ol>'
        "These probabilities represent model-estimated trajectory risks. They are "
        "<strong>not</strong> clinical diagnoses, <strong>not</strong> final discharge decisions, "
        "and <strong>not</strong> real population prevalence estimates.",
    )

    # ── Per-tab interpretation ────────────────────────────────────────────────
    st.markdown(
        f'<div style="font-size:1.05rem;font-weight:700;color:{_HEADING};'
        f'margin:0.6rem 0 0.8rem 0;">How to interpret each tab</div>',
        unsafe_allow_html=True,
    )

    _section(
        "🧑‍⚕️ Patient Risk Summary",
        "This tab is <strong>individual-patient oriented</strong>. It shows the selected "
        "synthetic patient's predicted trajectory probability distribution, the most likely "
        "trajectory, the second most likely trajectory, the probability gap between them, and "
        "a Sankey-style pathway view.<br><br>"
        "The <strong>most likely trajectory</strong> is the trajectory with the highest predicted "
        "probability. The <strong>probability gap</strong> shows how clearly the top trajectory is "
        "separated from the second most likely trajectory. A <strong>small gap</strong> means the "
        "result should be interpreted cautiously, because two trajectories may be similarly "
        "plausible.<br><br>"
        "This tab demonstrates how individual-level model outputs could be shown in practice, but "
        "the displayed patients are synthetic examples, not real patient records.",
        accent="#2b6cb0",
    )

    _section(
        "🔍 Key Drivers",
        "This tab explains which features contributed most to the selected synthetic patient's "
        "predicted trajectory.<br><br>"
        "<strong>Positive SHAP values</strong> increase the predicted probability of the selected "
        "trajectory, while <strong>negative SHAP values</strong> reduce it. SHAP values explain a "
        "prediction's contribution — they do <strong>not</strong> establish causality.<br><br>"
        "The clinical-domain and Andersen-framework charts summarise how much different groups of "
        "variables contributed to the explanation.",
        accent="#8e44ad",
    )

    _section(
        "👥 Population Insights",
        "This tab is <strong>population-level and planning-oriented</strong>. It lets users select "
        "subgroup variables such as region, sex, age group, rurality, prior care fragmentation, "
        "frailty, comorbidity, active surgical wait status, and marginalization indices.<br><br>"
        "For the selected subgroup, the dashboard shows average predicted trajectory probabilities "
        f"across the {n_patients} synthetic prototype patients.<br><br>"
        "<strong>This tab should be interpreted very cautiously.</strong> It demonstrates how "
        "subgroup exploration could work in a future implementation, but it is <strong>not</strong> "
        "a true population-level analysis and should not be interpreted as real regional burden, "
        "true prevalence, or a system-wide estimate.",
        accent="#2f855a",
    )

    _section(
        "📈 Model Performance",
        "This tab summarises model performance from the underlying model development and evaluation "
        "process. These results are <strong>not</strong> calculated from the "
        f"{n_patients} synthetic dashboard patients.<br><br>"
        "It helps users understand model discrimination, threshold behaviour, and classification "
        "performance. These results should be interpreted alongside calibration, fairness/"
        "reliability results, and clinical context.",
        accent="#2b6cb0",
    )

    _section(
        "⚖️ Equity & Reliability",
        "This tab summarises subgroup-level model behaviour from the underlying evaluation analyses. "
        "It is intended to support responsible <strong>model governance</strong> by showing whether "
        "model behaviour differs across equity-relevant or system-relevant groups.<br><br>"
        "These results should be reviewed as part of model governance and are separate from the "
        "synthetic patient examples shown in the interactive dashboard.",
        accent="#c0392b",
    )

    _section(
        "📋 Planning Support",
        "This tab translates a selected synthetic patient's predicted trajectory into structured "
        "<strong>planning prompts</strong>. The prompts are decision-support considerations, "
        "<strong>not</strong> automated clinical recommendations, and must be interpreted with "
        "clinical judgment in the context of the individual patient's full clinical picture.",
        accent="#dd6b20",
    )

    # ── Disclaimer ────────────────────────────────────────────────────────────
    st.markdown(
        f'<div style="background:#fff5f5;border:1px solid #fbcaca;'
        f'border-left:4px solid #c0392b;border-radius:8px;'
        f'padding:1.1rem 1.4rem;margin-top:0.4rem;">'
        f'<div style="font-size:1.0rem;font-weight:700;color:#9b2c2c;'
        f'margin-bottom:0.4rem;">Important research prototype disclaimer</div>'
        f'<p style="font-size:0.88rem;color:#742a2a;line-height:1.7;margin:0;">'
        f'ADAPT-D is intended for academic demonstration and knowledge translation. It has '
        f'<strong>not been prospectively validated for clinical deployment</strong>. It should not '
        f'be used to make real patient-care decisions, allocate clinical resources, or replace '
        f'professional judgment.</p></div>',
        unsafe_allow_html=True,
    )
