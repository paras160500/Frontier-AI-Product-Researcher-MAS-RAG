
#----------------------------------------------------------------------------------------
#                                   Import Statements
#----------------------------------------------------------------------------------------

from crewai import Task
from crew_ai_logic.crew_ai_agents import patent_research_agent, patent_intelligence_agent

#----------------------------------------------------------------------------------------
#                                   Task Statements
#----------------------------------------------------------------------------------------

search_patents_task = Task(
    description="""
    Search for patents related to:

    {query}

    Retrieve the most relevant patents.

    Include:
    - Patent titles
    - Patent IDs
    - Publication dates
    - Abstracts
    - Claims
    - Patent classifications

    Return all relevant patent information.
    """,
    expected_output="""
    A collection of relevant patent documents including
    title, patent id, abstract, claims, classifications,
    and publication metadata.
    """,
    agent=patent_research_agent
)

analyze_trends_task = Task(
    description="""
    Create a premium executive-level patent intelligence report.

    The report must:

    - Be visually appealing in Markdown
    - Include tables wherever possible
    - Include strategic insights
    - Include opportunity scoring
    - Include competitive intelligence
    - Include white-space analysis
    - Include future technology trajectories
    - Include patent references and URLs

    This report will be consumed by:
    - CTOs
    - R&D leaders
    - Innovation teams
    - Investors

    Avoid generic patent summaries.
    Focus on strategic intelligence.
    """,

    expected_output="""
    A premium consulting-style patent intelligence report
    including executive summary tables,
    technology cluster analysis,
    opportunity matrices,
    competitive intelligence,
    market forecasts,
    and a patent reference library with URLs.
    """,
    agent=patent_intelligence_agent,
    context=[search_patents_task]
)