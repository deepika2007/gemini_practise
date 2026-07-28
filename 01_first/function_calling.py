from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import time

load_dotenv()

API_KEY= os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

print('\n'+ "="*50)

print('Welcome to Gemini Chatbot Agent')

print('\n'+ "="*50)

# Function 1 : skills 
def get_skills(role:str) :
    """
    Return required skills for a role
    Paramertes: role(str) - Career role selected by user
    Return Dict : Required Skills
    """

    return {
        "role": role,
        "skills": ["LLMs", "ReactJS", "NodeJS", "Javascript"]
    }

def get_certificate(role:str):
    """
    Return Certificate into 
    Paramertes: role(str) : Career role
    Return: dict
    """

    return {
        "role": role,
        "certification":[
            "AZ-102", "AZ-104", "AWS"
        ]
    }

def get_salary(role:str):
    """
    Return Certificate into 
    Paramertes: role(str)
    Return: dict
    """

    return {
        "role": role,
        "salary_range": "1-2 LPA"
    }

# Register functions

tools =[
    get_skills, get_certificate, get_salary
]

query = input("Prompt : ")


response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=query,
    config= types.GenerateContentConfig(
        tools=tools
    )
)

print(response.text)