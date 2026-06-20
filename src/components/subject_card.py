import streamlit as st

def subject_card(name, code, section, stats=None, footer_callback=None):
    # Build stats HTML first (outside f-string to avoid brace conflicts)
    stats_html = ""
    if stats:
        stats_html += '<div style="display:flex; gap:20px; flex-wrap:wrap; align-items:center;">'
        for icon, label, value in stats:
            stats_html += (
                '<div style="display:flex; align-items:center; gap:5px;'
                ' color:#475569; font-size:0.9rem;">'
                '<span style="font-size:1rem;">' + str(icon) + '</span>'
                '<span><b>' + str(value) + '</b> ' + str(label) + '</span>'
                '</div>'
            )
        stats_html += "</div>"

    # Build full HTML in one shot, then render once
    html = (
        '<div style="background:white; border:1px solid #e2e8f0; border-radius:16px;'
        ' padding:24px 28px; margin-bottom:16px; box-shadow:0 1px 4px rgba(0,0,0,0.06);">'
        '<h3 style="margin:0 0 10px 0; color:#1e293b; font-size:1.25rem; font-weight:700;">'
        + str(name) +
        '</h3>'
        '<p style="color:#64748b; margin:0 0 14px 0; font-size:0.95rem;">'
        'Code :&nbsp;'
        '<span style="background:#5865F2; color:#E0E3FF; padding:2px 10px;'
        ' border-radius:6px; font-size:0.85rem; font-weight:600;">'
        + str(code) +
        '</span>'
        '&nbsp;| Section : ' + str(section) +
        '</p>'
        + stats_html +
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()


# ── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    st.set_page_config(page_title="Manage Subjects", layout="wide")

    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] { background: #EEF0FF; }
        [data-testid="stHeader"] { background: transparent; }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(
            "<h1 style='font-family:Arial Black,sans-serif; color:#1e293b;'>Manage<br>Subjects</h1>",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown("""
            <div style="display:flex; justify-content:flex-end; padding-top:16px;">
                <button style="background:#EB459E; color:white; border:none;
                    padding:14px 28px; border-radius:30px; font-size:1rem;
                    font-weight:600; cursor:pointer;">
                    Create New Subject
                </button>
            </div>
        """, unsafe_allow_html=True)

    subject_card(
        name="Introduction to memes",
        code="CS204",
        section="C",
        stats=[
            ("👥", "Students", 0),
            ("🔒", "Classes", 0),
        ],
    )