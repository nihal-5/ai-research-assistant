from crewai import Task

class ResearchTasks:
    def research_task(self, agent, topic):
        return Task(
            description=f"""Conduct comprehensive research on: {topic}
            
            Your objectives:
            1. Search for and gather information from credible sources
            2. Identify key facts, statistics, and developments
            3. Note important trends and patterns
            4. Collect relevant examples and case studies
            5. Document all sources for citations
            
            Provide a detailed summary of your findings with source attribution.""",
            agent=agent,
            expected_output="Detailed research findings with source citations"
        )
    
    def analysis_task(self, agent, topic):
        return Task(
            description=f"""Analyze the research findings on: {topic}
            
            Your objectives:
            1. Validate the accuracy of gathered information
            2. Identify patterns and connections in the data
            3. Assess the quality and credibility of sources
            4. Highlight key insights and implications
            5. Note any gaps or areas needing further investigation
            
            Provide a structured analysis with clear insights.""",
            agent=agent,
            expected_output="Comprehensive analysis with validated insights"
        )
    
    def writing_task(self, agent, topic):
        return Task(
            description=f"""Create a professional research report on: {topic}
            
            Your objectives:
            1. Structure the report with clear sections:
               - Executive Summary
               - Introduction
               - Key Findings
               - Analysis and Insights
               - Conclusion
               - References
            2. Write in a clear, professional tone
            3. Include all relevant citations
            4. Ensure logical flow and coherence
            5. Format for readability
            
            Produce a publication-ready markdown report.""",
            agent=agent,
            expected_output="Well-structured professional report in markdown format"
        )
