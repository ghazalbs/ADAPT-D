"""tabs/shared_components.py — Shared UI utilities used across active tabs."""

import streamlit as st


def tab_note(text: str) -> None:
    """
    Renders a consistent, high-contrast "how to interpret" note at the top of a tab.

    Light blue panel with dark navy text so it stays readable on the fixed light
    theme. Use one short sentence describing what the tab shows and how to read it.
    """
    st.markdown(
        f'<div style="background:#eff6ff;border:1px solid #bfdbfe;'
        f'border-left:4px solid #2563eb;border-radius:0 8px 8px 0;'
        f'padding:0.65rem 1rem;margin-bottom:1rem;">'
        f'<p style="font-size:0.83rem;color:#1e3a5f;margin:0;line-height:1.55;">'
        f'ℹ️&nbsp; {text}</p></div>',
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, sub: str = "", color: str = "#2b6cb0") -> str:
    """
    Returns an HTML string for a KPI metric card.

    Args:
        label: Short uppercase label shown below the value.
        value: Primary metric value (string, e.g. "74%").
        sub:   Optional smaller subtitle line beneath the label.
        color: Accent colour for the top border stripe.
    """
    sub_html = (
        f"<div style='font-size:0.71rem;color:#64748b;margin-top:2px;'>{sub}</div>"
        if sub else ""
    )
    return f"""
    <div style="background:white;border-radius:10px;padding:1.1rem;
                box-shadow:0 2px 8px rgba(0,0,0,0.08);text-align:center;
                border-top:3px solid {color};">
      <div style="font-size:1.7rem;font-weight:700;color:#1a365d;line-height:1.2;">{value}</div>
      <div style="font-size:0.73rem;font-weight:600;color:#5f6b78;
                  text-transform:uppercase;letter-spacing:0.05em;margin-top:3px;">{label}</div>
      {sub_html}
    </div>"""
