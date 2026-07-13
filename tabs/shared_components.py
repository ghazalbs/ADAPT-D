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


def kpi_card(
    label: str,
    value: str,
    sub: str = "",
    accent: str = "#2b6cb0",
    variant: str = "top",
) -> str:
    """
    Returns an HTML string for a KPI metric card.

    variant "top"  — centred card, large value, top-accent stripe
                     (Population Insights + Model Performance).
    variant "left" — left-aligned card, label above value, left-accent stripe
                     (Patient Risk Summary).

    Output is flattened to a single line: several cards are joined into one
    ``.kpi-grid`` container, and a blank/whitespace-only line (e.g. an empty
    subtitle) would otherwise terminate Streamlit's HTML block and make the
    following cards render as a Markdown code block.
    """
    if variant == "left":
        sub_html = (
            f"<div style='font-size:0.72rem;color:var(--clr-text-muted);margin-top:2px;'>{sub}</div>"
            if sub else ""
        )
        html = f"""
    <div style="background:var(--clr-bg-primary);
                border:1px solid var(--clr-border);border-left:4px solid {accent};
                border-radius:8px;padding:1rem 1.1rem;height:100%;">
      <div style="font-size:0.68rem;font-weight:500;color:var(--clr-text-muted);
                  text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px;">
        {label}
      </div>
      <div style="font-size:1.2rem;font-weight:500;color:var(--clr-text-primary);line-height:1.25;">
        {value}
      </div>
      {sub_html}
    </div>"""
    else:  # variant == "top"
        sub_html = (
            f"<div style='font-size:0.71rem;color:var(--clr-on-surface-hint);margin-top:2px;'>{sub}</div>"
            if sub else ""
        )
        html = f"""
    <div style="background:white;border-radius:10px;padding:1.1rem;
                box-shadow:0 2px 8px rgba(0,0,0,0.08);text-align:center;
                border-top:3px solid {accent};">
      <div style="font-size:1.7rem;font-weight:700;color:#1a365d;line-height:1.2;">{value}</div>
      <div style="font-size:0.73rem;font-weight:600;color:var(--clr-on-surface-muted);
                  text-transform:uppercase;letter-spacing:0.05em;margin-top:3px;">{label}</div>
      {sub_html}
    </div>"""

    return "".join(line.strip() for line in html.splitlines() if line.strip())
