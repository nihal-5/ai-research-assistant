from crewai import Crew, Process
from agents import ResearchAgents
from tasks import ResearchTasks

class ResearchCrew:
    def __init__(self):
        self.agents_factory = ResearchAgents()
        self.tasks_factory = ResearchTasks()
    
    def run(self, topic):
        researcher = self.agents_factory.research_agent()
        analyst = self.agents_factory.analyst_agent()
        writer = self.agents_factory.writer_agent()
        
        research_task = self.tasks_factory.research_task(researcher, topic)
        analysis_task = self.tasks_factory.analysis_task(analyst, topic)
        writing_task = self.tasks_factory.writing_task(writer, topic)
        
        crew = Crew(
            agents=[researcher, analyst, writer],
            tasks=[research_task, analysis_task, writing_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        return result
