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

    # first task - think
    def think(self):
        prompt = f"""
        you are a AI coach agent.
        User Goal:{self.goal}
        Available tools are:
        SKILL_TOOL 
        CERTIFICATION_TOOL 
        SALARY_TOOL
        PROJECT_TOOL

        previous Observation : {self.observation}
        think carefully .
        Decide what information you still need.

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

        return response.text.strip()

    # Second task - action

    def execute_action(self, action):
        tool= TOOL_REGISTRY.get(action)

        if tool:
            return tool(self.goal)

        return None

    # Final Response

    def generate_final_plan(self):
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
        """


        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )


        print('\n'+ "="*50)

        print('Result : ', response.text)

        print('\n'+ "="*50)

    # ReAct
    def run(self):
        step=1
        while True:

            print('\n'+ "="*50)
            print(f"Step : {step}")
            print('\n'+ "="*50)

            # thought

            action = self.think()
            print(f"thought")
            print(action)

            # Finish 
            if action =='FINISH':
                print("Enough")
                break

            # action 
            print("*****Action*****")
            result = self.execute_action(action)


            # observation
            print("*****Observation*****")
            print(result)

            self.observation.append(result)
            step +=1

        self.generate_final_plan()

            
goal = input('Enter Goal : ')
agent = CareerCoachAgent(goal)
agent.run()
