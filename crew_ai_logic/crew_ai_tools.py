#----------------------------------------------------------------------------------------
#                                   Import Statements
#----------------------------------------------------------------------------------------

import os
import sys,json
from datetime import datetime,timedelta
import requests
from crewai import Agent,Task,Process,Crew
from crewai.tools import BaseTool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from research_fetch_logic.open_search_client import get_opensearch_client
from typing import Type
from pydantic import BaseModel, Field
from crewai.llm import LLM
from research_fetch_logic.research_fetch_logic_main import main_orchastrator


#----------------------------------------------------------------------------------------
#                                   Tools Definations
#----------------------------------------------------------------------------------------


class SearchPatentsTool(BaseTool):
    name: str = "search_patents"

    description: str = (
        "Searches patents and research documents using the internal patent "
        "knowledge system."
    )

    def _run(self, query: str, top_k: int = 20) -> str:
        try:
            results = main_orchastrator(query, top_k=top_k)

            with open("output123123123.txt", "w") as file:
                for item in results:
                    file.write(json.dumps(item) + "\n")

            if not results:
                return "No relevant patent information found."

            patents_text = []

            for idx, hit in enumerate(results, start=1):

                source = hit.get("_source", {})

                patents_text.append(
                    f"""
                        PATENT #{idx}

                        TITLE:
                        {source.get("title", "N/A")}

                        PATENT ID:
                        {source.get("patent_id", "N/A")}

                        PUBLICATION DATE:
                        {source.get("publication_date", "N/A")}

                        CLASSIFICATIONS:
                        {source.get("classifications", [])}

                        CLAIMS:
                        {source.get("claims", [])}

                        ABSTRACT:
                        {source.get("abstract", "N/A")}

                        --------------------------------------------------
                    """
                )

            return "\n".join(patents_text)

        except Exception as e:
            return f"Patent search failed: {str(e)}"
        

class PatentTrendsInput(BaseModel):
    patents_data : str = Field(
        ...,
        description="Raw patent records, abstracts, claims, summaries and many more useful patent information"
    )


class AnalyszePatentTrendsTool(BaseTool):
    name : str = "analyze_patent_trends"
    description : str = (
        "Analyze patent data and identifies technology trends, future opportunities,"
        "competitive white spaces, and market signals"
    )
    args_schema : Type[BaseModel] = PatentTrendsInput

    def _run(self,patents_data : str) -> str:
        open_ai_llm = LLM(
            model="openai/gpt-4o-mini",
            temperature=0.2,
            api_key=os.getenv("OPEN_AI_API")
        )

        prompt = f"""
                You are a Chief Patent Intelligence Strategist.

                PATENT DATA
                ========================
                {patents_data}
                ========================

                Your objective is to create a PREMIUM PATENT INTELLIGENCE REPORT.

                This report will be displayed directly inside a Streamlit application.

                Therefore the report must be:

                - Beautiful markdown
                - Executive-friendly
                - Highly visual
                - Rich in tables
                - Rich in strategic insights

                DO NOT generate long paragraphs.

                Prefer:
                - Tables
                - Bullet points
                - Rankings
                - Opportunity scores
                - Strategic callouts

                Use a few professional emojis only.

                Maximum:
                1 emoji per major section.

                ===================================================
                REPORT FORMAT
                ===================================================

                # 🔍 Patent Intelligence Report

                Provide a 2-3 sentence executive overview.

                ---

                # 📌 Executive Summary

                Create a table:

                | Strategic Insight | Impact | Confidence |
                |------------------|---------|------------|

                Include top 5 insights.

                ---

                # 🧩 Technology Clusters

                Create a table:

                | Cluster | Related Patents | Prominence | Strategic Importance |
                |----------|----------------|------------|----------------------|

                After table provide:

                ### Key Observations

                - observation
                - observation
                - observation

                ---

                # 📈 Emerging Technology Trajectories

                Create a table:

                | Technology Direction | Growth Signal | Confidence |
                |----------------------|--------------|------------|

                Then explain:

                ### Why It Matters

                - point
                - point
                - point

                ---

                # 🚀 Future Market Signals

                Create a table:

                | Industry | Expected Impact | Opportunity |
                |-----------|----------------|------------|

                Then list:

                ### Emerging Products

                - product
                - product
                - product

                ---

                # 🎯 White Space Opportunities

                Create a table:

                | Opportunity Area | Gap | Filing Potential |
                |-----------------|-----|------------------|

                Rank opportunities:

                | Rank | Area | Strategic Value |
                |-------|------|-----------------|

                ---

                # 🏢 Competitive Intelligence

                Create a table:

                | Strategic Direction | Evidence | Risk Level |
                |--------------------|-----------|-----------|

                Then:

                ### Disruption Risks

                - risk
                - risk
                - risk

                ---

                # 🔥 Opportunity Heatmap

                Use markdown table:

                | Area | Opportunity Score |
                |------|-------------------|
                | Safety | 🟢 High |
                | AI Integration | 🟢 High |
                | Recycling | 🟡 Medium |
                | Alternative Chemistries | 🟢 High |

                ---

                # 💡 Recommended R&D Investments

                Provide top 5 recommendations.

                ---

                # 🔗 Patent Reference Library

                For EVERY patent found in the input data create a table:

                | Patent Title | Patent Number | Assignee | Why It Matters | Patent URL |
                |-------------|--------------|----------|----------------|------------|

                IMPORTANT:
                If URL exists in source data include it.
                Never invent URLs.

                ---

                # ⭐ Final Strategic Conclusion

                Provide a concise executive conclusion.

                ===================================================
                OUTPUT RULES
                ===================================================

                - Markdown only
                - No XML
                - No JSON
                - No code blocks
                - No chain of thought
                - No explanations about methodology
                - Focus on strategic insight
            """

        response = open_ai_llm.call(prompt)

        return response