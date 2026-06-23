
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
    Analyze the patent dataset provided in the context.

    Produce:

    1. Technology Clusters
    2. Emerging Technology Trajectories
    3. Future Market Signals (3-5 years)
    4. White Space Opportunities
    5. Competitive Intelligence
    6. Executive Summary

    Focus on strategic insights rather than patent summaries.
    """,
    expected_output="""
    A comprehensive patent intelligence report including:
    technology clusters, future trends, market opportunities,
    white-space opportunities, competitive intelligence,
    and executive recommendations.
    """,
    agent=patent_intelligence_agent,
    context=[search_patents_task]
)