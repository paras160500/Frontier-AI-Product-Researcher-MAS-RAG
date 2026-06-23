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
            You are a world-class Patent Intelligence Analyst, Technology Futurist,
            and IP Strategy Consultant.

            Your job is not to summarize patents.

            Your job is to discover:
            - Hidden technology patterns
            - Engineering evolution paths
            - Emerging research directions
            - Future commercial opportunities
            - Competitive gaps

            PATENT DATA:
            ========================
            {patents_data}
            ========================

            Perform a deep patent landscape analysis.

            Instructions:

            1. TECHNOLOGY CLUSTERS
            - Group patents into major technology domains.
            - Explain the common technical theme behind each cluster.
            - Estimate relative prominence.

            2. EMERGING TECHNOLOGY TRAJECTORIES
            - Identify technologies showing acceleration.
            - Explain why these areas appear to be gaining momentum.
            - Highlight enabling technologies and convergence trends.

            3. FUTURE MARKET SIGNALS (3-5 YEARS)
            - Predict industries likely to benefit.
            - Predict products likely to emerge.
            - Explain the reasoning chain from patents to market impact.

            4. WHITE SPACE OPPORTUNITIES
            - Identify technical gaps.
            - Suggest areas with weak patent coverage.
            - Highlight opportunities for new filings.

            5. COMPETITIVE INTELLIGENCE
            - Infer likely strategic directions competitors are pursuing.
            - Identify potential disruption risks.

            6. EXECUTIVE SUMMARY
            - Provide the top 5 most important strategic insights.

            Output Requirements:
            - Use markdown.
            - Use clear headings.
            - Be analytical rather than descriptive.
            - Focus on insight generation, not patent summarization.
            - Support conclusions with evidence from the patent data.
        """

        response = open_ai_llm.call(prompt)

        return response