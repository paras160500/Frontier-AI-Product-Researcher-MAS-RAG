from crewai import Crew, Process
from crew_ai_logic.crew_ai_agents import patent_research_agent, patent_intelligence_agent
from crew_ai_logic.crew_ai_tasks import search_patents_task,analyze_trends_task


def generate_crew_for_patent_analysis(query : str):

    # Making Crew
    patent_crew = Crew(
        agents=[
            patent_research_agent,
            patent_intelligence_agent
        ],
        tasks=[
            search_patents_task,
            analyze_trends_task
        ],
        process=Process.sequential,
        verbose=True
    )

    # Kicking off the crew
    result = patent_crew.kickoff(
        inputs={
            "query": query
        }
    )

    print(result)


if __name__ == "__main__":
    generate_crew_for_patent_analysis("Bio Fuel")