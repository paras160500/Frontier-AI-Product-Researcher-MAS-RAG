import streamlit as st
from crew_ai_logic.crew_ai_generator import generate_crew_for_patent_analysis

st.set_page_config(
    page_title="Patent Intelligence",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Patent Intelligence System")

query = st.text_input(
    "Enter technology/domain",
    placeholder="e.g. Bio Fuel"
)

if st.button("Analyze Patents", type="primary"):

    if not query.strip():
        st.warning("Please enter a query.")
    else:

        with st.spinner("Analyzing patents..."):

            try:
                result = generate_crew_for_patent_analysis(query)

                st.success("Analysis Complete")

                st.download_button(
                        "📥 Download Report",
                        data=result,
                        file_name="patent_intelligence_report.md",
                        mime="text/markdown"
                    )

                # Render markdown nicely
                with st.container(border=True):
                    st.markdown(result)

            except Exception as e:
                st.error(f"Error: {e}")