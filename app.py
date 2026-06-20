import streamlit as st
from sample import call_me_sample

# -------------------------------
# Page Configuration
# -------------------------------

st.set_page_config(
    page_title="Patent Intelligence System",
    page_icon="🧠",
    layout="wide"
)


# -------------------------------
# Header
# -------------------------------

st.title("🧠 Patent Intelligence System")
st.caption(
    "AI-powered patent research, analysis, and innovation discovery"
)


# -------------------------------
# Query Input
# -------------------------------

query = st.text_area(
    label="Enter your research topic",
    placeholder=(
        "Example:\n"
        "Future of solid-state battery technology"
    ),
    height=150
)


# -------------------------------
# Submit Button
# -------------------------------

if st.button(
    "🔍 Analyze Patent Landscape",
    type="primary",
    use_container_width=True
):

    if not query.strip():
        st.warning("Please enter a research query.")
        st.stop()

    with st.spinner(
        "Analyzing patents and research data..."
    ):
        try:
            response = call_me_sample(query)

        except Exception as e:
            st.error(
                f"Something went wrong: {str(e)}"
            )
            st.stop()


    # ---------------------------
    # Markdown Output
    # ---------------------------

    st.divider()

    st.subheader("📊 Patent Intelligence Report")

    st.markdown(
        response,
        unsafe_allow_html=False
    )
