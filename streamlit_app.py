import streamlit as st

from crew_ai_logic.crew_ai_generator import generate_crew_for_patent_analysis
from search_patents_logic.search_logic_orchestrator import (
    search_patents
)
from iterative_search_logic.iterative_main_orchastrator import iterative_exploration

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Patent Intelligence Hub",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Patent Intelligence Hub")
st.markdown("Choose what you want to do 👇")

# -----------------------------
# Mode Selector
# -----------------------------
mode = st.radio(
    "Select Mode",
    [
        "🔎 Patent Search",
        "🚀 Iterative Patent Search",
        "🧠 Patent Analysis (CrewAI)"
    ],
    horizontal=True
)

# -----------------------------
# Input
# -----------------------------
query = st.text_input(
    "Enter technology / domain",
    placeholder="e.g. Bio Fuel, Neural Networks, EV batteries"
)

# =========================================================
# 🔎 STANDARD SEARCH OPTIONS
# =========================================================
search_option = None
iteration_steps = 3

if mode == "🔎 Patent Search":

    st.info("OpenSearch Retrieval Mode")

    search_option = st.selectbox(
        "Select Search Type",
        options=["1", "2", "3"],
        format_func=lambda x: {
            "1": "Keyword Search 🔎",
            "2": "Semantic Search 🧠",
            "3": "Hybrid Search ⚡"
        }[x]
    )

# =========================================================
# 🚀 ITERATIVE SEARCH OPTIONS
# =========================================================
elif mode == "🚀 Iterative Patent Search":

    st.info(
        "Iterative Retrieval Mode: query is refined over multiple "
        "search cycles using top patent results."
    )

    iteration_steps = st.slider(
        "Number of Iterations",
        min_value=1,
        max_value=5,
        value=3,
        step=1
    )

# -----------------------------
# Run Button
# -----------------------------
if st.button("Run", type="primary"):

    if not query.strip():
        st.warning("Please enter a query.")
        st.stop()

    # =========================================================
    # 🔎 PATENT SEARCH EXECUTION
    # =========================================================
    if mode == "🔎 Patent Search":

        st.info("Running OpenSearch patent retrieval...")

        with st.spinner("Searching patents..."):

            try:

                result_md = search_patents(
                    query=query,
                    search_option=search_option
                )

                st.success("Search Complete")

                st.download_button(
                    "📥 Download Results",
                    data=result_md,
                    file_name="patent_search_results.md",
                    mime="text/markdown"
                )

                with st.container(border=True):
                    st.markdown(result_md)

            except Exception as e:
                st.error(f"Search Error: {e}")

    # =========================================================
    # 🚀 ITERATIVE SEARCH EXECUTION
    # =========================================================
    elif mode == "🚀 Iterative Patent Search":

        st.info("Running iterative patent exploration...")

        with st.spinner("Refining query and retrieving patents..."):

            try:

                result_md = iterative_exploration(
                    query=query,
                    steps=iteration_steps
                )

                st.success("Iterative Search Complete")

                st.download_button(
                    "📥 Download Results",
                    data=result_md,
                    file_name="iterative_patent_search.md",
                    mime="text/markdown"
                )

                with st.container(border=True):
                    st.markdown(result_md)

            except Exception as e:
                st.error(f"Iterative Search Error: {e}")

    # =========================================================
    # 🧠 CREW AI ANALYSIS
    # =========================================================
    elif mode == "🧠 Patent Analysis (CrewAI)":

        st.info("Running AI-powered patent analysis...")

        with st.spinner("Analyzing patents using CrewAI..."):

            try:

                result = generate_crew_for_patent_analysis(query)

                st.success("Analysis Complete")

                st.download_button(
                    "📥 Download Report",
                    data=result,
                    file_name="patent_intelligence_report.md",
                    mime="text/markdown"
                )

                with st.container(border=True):
                    st.markdown(result)

            except Exception as e:
                st.error(f"Analysis Error: {e}")

