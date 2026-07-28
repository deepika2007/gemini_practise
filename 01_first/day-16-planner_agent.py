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

class CareerCoachAgent:
    def __init__(self, goal):
        self.goal = goal
        self.observation = []
        self.plan =[]

    # first- create plan
    def create_plan(self):
        print(f"[PLANNER] Creating a plan for you")
        prompt = f"""
        you are a planner agent.
        User Goal:{self.goal}
        Available tools are:
        SKILL_TOOL 
        CERTIFICATION_TOOL 
        SALARY_TOOL
        PROJECT_TOOL

        Your task:
        Create the BEST execution plan

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

    # Second task - action

    def execute_plan(self):
        print(f"[EXECUTING] Executing plan...")

        step =1
        for tool_name in self.plan:
            print('\n'+ "="*50)
            print(f"Step: {step}")
            print('\n'+ "="*50)

            tool = TOOL_REGISTRY.get(tool_name)
            result = tool(self.goal)
            print(f"\n Observation:\n  {step}")
            self.observation.append(result)
            step+=1
       

    # Final Response

    def generate_final_plan(self):
        print(f"[AGENT] Generating plan...")

        prompt= f"""
        User Goal : {self.goal}
        Collected Information : {self.observation}
        Generate :
        1. Career Summary
        2. Skills Required
        3. Certification
        4. Project
        5. Salary Expectation
        6. 20 days leaning roadmap

        generate professional plan 
        """


        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )


        print('\n'+ "="*50)

        print('Result : ', response.text)

        print('\n'+ "="*50)

    # Run Agent
    def run(self):

        # create plan
        self.plan = self.create_plan()
        print('\n'+ "="*50)


        for index, tool in enumerate(self.plan, start=1):
            print(f"{index}, {tool}")

        self.execute_plan()

        self.generate_final_plan()
            
goal = input('Enter Plan : ')
agent = CareerCoachAgent(goal)
agent.run()
