from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class ResearchAgents:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=os.getenv("MODEL", "gpt-4"),
            temperature=float(os.getenv("TEMPERATURE", "0.7"))
        )
    
    def research_agent(self):
        return Agent(
            role="Research Specialist",
            goal="Gather comprehensive and accurate information on the given topic",
            backstory="""You are an expert researcher with years of experience in 
            academic and industry research. You excel at finding relevant information 
            from multiple sources and identifying credible references.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
    
    def analyst_agent(self):
        return Agent(
            role="Data Analyst",
            goal="Synthesize research findings and validate information accuracy",
            backstory="""You are a skilled analyst who can identify patterns, 
            validate facts, and synthesize complex information into clear insights. 
            You have a keen eye for detecting inconsistencies and bias.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
    
    def writer_agent(self):
        return Agent(
            role="Technical Writer",
            goal="Create well-structured, comprehensive reports with proper citations",
            backstory="""You are an experienced technical writer who excels at 
            creating clear, engaging, and professional documentation. You know how 
            to structure information for maximum impact and readability.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
