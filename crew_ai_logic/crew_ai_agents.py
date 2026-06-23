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
    role="Patent Intelligence Analyst",
    goal=(
        "Analyze patent landscapes and identify technology trends, "
        "innovation trajectories, white-space opportunities, "
        "competitive intelligence, and future market signals."
    ),
    backstory=(
        "You are a world-class patent strategist, technology futurist, "
        "and innovation consultant. You transform raw patent data into "
        "actionable strategic intelligence."
    ),
    tools=[AnalyszePatentTrendsTool()],
    verbose=True,
    allow_delegation=False,
    llm=open_ai_llm
)