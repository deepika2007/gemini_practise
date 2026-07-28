from google import genai
from dotenv import load_dotenv
import os
import time

load_dotenv()

API_KEY= os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)


# agent 
class RoadMapAgent:
    def __init__(self, goal):
        # Goal = user input
        self.goal = goal

    # Step 1- Reasoning
    def reason(self):
        print('[Agent] Understanding goal')
        prompt=f"""
        User Goal :{self.goal}
        Identify all required skills.
        Return only skills
        """
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )
        return response.text

    # Step 2- Planning
    def plan(self, skills):
        print('[Agent] Creating Plan')
        prompt=f"""
        Goal :{self.goal}
        Skills:{skills}
        Arrange these skills in the best learning order
        """
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )
        return response.text

    # Step 3: Execute 
    def execute(self, plan):
        print('[Agent] Execute Plan')
        prompt=f"""
        Goal :{self.goal}
        Learning Plan:{plan}
        Create a detailed plan for 1 week 
        """
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )
        return response.text


    # Step 4: Run Agent 
    def run(self):

        skills = self.reason()
        time.sleep(1)

        plan= self.plan(skills)
        time.sleep(1)

        roadmap= self.execute(plan)
        print('\n'+ "="*50)

        print(roadmap)

print('\n'+ "="*50)

print('Welcome to RoadMap Agent')

print('\n'+ "="*50)

goal = input("Enter your Goal : ")
agent = RoadMapAgent(goal)
agent.run()

