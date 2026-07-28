from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import time

load_dotenv()

API_KEY= os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

print('\n'+ "="*50)

print('Welcome to Gemini Career Agent')

print('\n'+ "="*50)

# Function 1 : skills 
def get_skills(goal:str) :
    """
    Return required skills for a goal
    Paramertes: goal(str) - Career goal selected by user
    Return Dict : Required Skills
    """

    return {
        "goal": goal,
        "skills": ["LLMs", "ReactJS", "NodeJS", "Javascript"]
    }

def get_certificate(goal:str):
    """
    Return Certificate into 
    Paramertes: goal(str) : Career goal
    Return: dict
    """

    return {
        "goal": goal,
        "certification":[
            "AZ-102", "AZ-104", "AWS"
        ]
    }

def get_salary(goal:str):
    """
    Return Certificate into 
    Paramertes: goal(str)
    Return: dict
    """

    return {
        "goal": goal,
        "salary_range": "1-2 LPA"
    }

def project_tool():
    """
    Return project recommended
    """

    return """
    Project recommended:
    - Chatbot
    - RAG assistant
    - Research agent 
    """

TOOL_REGISTRY = {
    "SKILL_TOOL": get_skills,
    "CERTIFICATION_TOOL": get_certificate,
    "SALARY_TOOL": get_salary,
}

# Agent

class ResearchAgent:
    def __init__(self, goal):
        self.goal = goal
        self.observation = []
        self.plan =[]
        self.evidence =[]

    #  Reaserch plan
    def create_research_plan(self):
        print(f"[RESEARCH] you are a research planner ")
        prompt = f"""
        you are a planner agent.
        User Goal:{self.goal}
        Available tools are:
        SKILL_TOOL 
        CERTIFICATION_TOOL 
        SALARY_TOOL
        PROJECT_TOOL

        Your task:
        Create the BEST research plan

        Rules:
        1. Use only required tools
        2. Do not use unneccessary tools
        3. return one tool per line
        4. return only tool name

        return only: 
        SKILL_TOOL 
        CERTIFICATION_TOOL 
        SALARY_TOOL
        PROJECT_TOOL
        """

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        plan =[]
        for line in response.text.split('\n'):
            tool = line.strip()
            if tool in TOOL_REGISTRY:
                plan.append(tool)

        return plan

   
    # Gather Evidence
    def gather_evidence(self):
        print(f"[EVIDENCE] collecting evidence plan...")

        step =1
        for tool_name in self.plan:

            tool = TOOL_REGISTRY.get(tool_name)
            result = tool(self.goal)

            print('\n'+ "="*50)
            print(f"Tool Name: {tool_name}")
            print('\n'+ "="*50)

            print(f"\n Result:\n  {result}")
            self.evidence.append(f"\n{tool_name}\n{result}")

            step+=1
       

    def analyze_evidence(self):
        print(f"[ANALYZING EVIDENCE]")

        prompt= f"""
        You are a AI career Analyst
        Goal:
        {self.goal}

        Evidence:
        {self.evidence}
        generate:
        1. key finidngs
        2. opportunities
        3. challenges
        return Analysis 
        """
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text


    # Generate Recommendation
    def generate_recommendation(self, analysis):
        print(f"[GENETATE RECOMMENDATION] Generating recommendation...")

        prompt= f"""
        User Goal : {self.goal}
        Analysis : {analysis}
        Generate :
        1. Executive Summary
        2. Recommendations
        3. Learning Path
        4. Final verdict
        """

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )


        print('\n'+ "="*50)

        print('\nRecommendation : \n', response.text)

        print('\n'+ "="*50)

    # Run Agent
    def run(self):

        # create plan
        self.plan = self.create_research_plan()
        print('\n'+ "="*50)


        for index, tool in enumerate(self.plan, start=1):
            print(f"{index}, {tool}")

        analysis = self.gather_evidence()

        print('ANALYSIS:\n')
        print(analysis)

        self.generate_recommendation(analysis)
            
goal = input('Enter Your goal : ')
agent = ResearchAgent(goal)
agent.run()
