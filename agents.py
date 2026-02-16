from crewai import Agent, Task, Crew, Process, LLM
from pydantic import BaseModel

# --- DATA SCHEMA ---
class ProposalModel(BaseModel):
    proposed_building: str
    logic: str
    target_segment: str
    roi: str
    risk_analysis: str
    space_utilization: str
    estimated_total_cost: str
    financial_feasibility_note: str

class RealEstateCrew:
    def __init__(self, location, land_size, budget):
        self.location = location
        self.land_size = land_size
        self.budget = budget
        # Local LLM Connection (Ollama)
        self.local_llm = LLM(model="ollama/llama3.2:1b",
                             base_url="http://localhost:11434",
                             timeout = 1200,
                             temperature = 0.3)

    def run(self):
        # 1. AGENTS
        researcher = Agent(
            role='Market Data Researcher',
            goal='Identify business types and service gaps in {location}',
            backstory='Quick and precise urban data analyst',
            llm=self.local_llm,
        )

        demographer = Agent(
            role='Socio-Economic Analyst',
            goal='Analyze population density and income levels for {location}',
            backstory='Data scientist specializing in census data and buyer personas.',
            llm=self.local_llm,
        )

        risk_officer = Agent(
            role='Risk & Compliance Specialist',
            goal='Identify flooding, zoning, and oversaturation risks for {location}',
            backstory='A cautious analyst who finds potential deal-breakers.',
            llm=self.local_llm,
        )

        strategist = Agent(
            role='Lead Investment Strategist',
            goal='Synthesize all data to propose a high-ROI project within budget.',
            backstory='Seasoned developer who balances demand with physical and financial limits.',
            llm=self.local_llm,
        )

        # 2. TASKS
        t1 = Task(description="Identify top businesses in {location}.", 
                  expected_output="Bullet points of market gaps.", 
                  agent=researcher)
        t2 = Task(description="Analyze demographics for {location}.", expected_output="Demographic profile.", agent=demographer)
        t3 = Task(description="List top 3 risks in {location}.", expected_output="Risk assessment report.", agent=risk_officer)
        
        t4 = Task(
            description="""Propose one specific building type for {location} with {land_size} acres and RM {budget}.
    
            IMPORTANT: Return ONLY a flat JSON object. Do not include 'properties' or 'type' descriptors.
            Fields needed:
            - proposed_building
            - logic
            - target_segment
            - roi
            - risk_analysis
            - space_utilization
            - estimated_total_cost
            - financial_feasibility_note""",
            agent=strategist,
            expected_output="A flat JSON object containing the investment proposal.",
            output_json=ProposalModel
        )

        # 3. CREW
        crew = Crew(
            agents=[researcher, demographer, risk_officer, strategist],
            tasks=[t1, t2, t3, t4],
            process=Process.sequential,
            verbose=True
        )

        return crew.kickoff(inputs={
            'location': self.location, 
            'land_size': self.land_size, 
            'budget': self.budget
        })