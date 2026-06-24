#----------------------------------------------------------------------------------------
#                                   Import Statements
#----------------------------------------------------------------------------------------
from crewai import Agent
from crew_ai_logic.crew_ai_tools import SearchPatentsTool,AnalyszePatentTrendsTool
from crewai.llm import LLM
import os 

#----------------------------------------------------------------------------------------
#                                       LLM Creation
#----------------------------------------------------------------------------------------

open_ai_llm = LLM(
    model="openai/gpt-4o-mini",
    temperature=0.2,
    api_key=os.getenv("OPEN_AI_API")
)

#----------------------------------------------------------------------------------------
#                                   Agent Creation Statements
#----------------------------------------------------------------------------------------



patent_research_agent = Agent(
    role="Patent Research Specialist",
    goal=(
        "Find the most relevant patents, research documents, "
        "claims, classifications, and technical disclosures."
    ),
    backstory=(
        "You are a senior patent search expert with deep expertise "
        "in patent databases, prior art search, technology scouting, "
        "and intellectual property research."
    ),
    tools=[SearchPatentsTool()],
    verbose=True,
    allow_delegation=False,
    llm=open_ai_llm
)


patent_intelligence_agent = Agent(
    role="Chief Patent Intelligence Strategist",
    goal="""
    Transform patent data into executive-grade technology intelligence reports.

    Deliver reports that are:
    - Visually structured
    - Business-oriented
    - Actionable
    - Easy to consume by executives

    Always use:
    - Tables
    - Strategic insights
    - Opportunity matrices
    - Technology heatmaps
    - Bullet summaries

    Avoid large blocks of plain text.
    """,
    backstory="""
    You are a globally recognized patent strategist,
    technology futurist, and innovation consultant.

    You have advised Fortune 500 companies,
    venture capital firms, R&D organizations,
    and government innovation programs.

    Your reports resemble premium consulting
    deliverables from Gartner, McKinsey, BCG,
    Deloitte and Accenture.

    Your reports are known for:
    - Clear structure
    - Executive readability
    - Strategic depth
    - Beautiful markdown formatting
    """,
    tools=[AnalyszePatentTrendsTool()],
    verbose=True,
    allow_delegation=False,
    llm=open_ai_llm
)