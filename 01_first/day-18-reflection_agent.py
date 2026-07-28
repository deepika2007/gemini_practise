from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY= os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

print('\n'+ "="*50)
print('Welcome to Career Agent')
print('\n'+ "="*50)


class ReflectionAgent:
    """
    Reflection agent
    responsibilities:
    1. Review the first draft
    2. Identify weaknessess
    3. Suggest improvements
    4. Generate improved reports
    """

    def __init__(self):
        pass

    # review draft

    def review_draft(self, review):
        print('\n'+ "="*50)
        print(f"REVIEWING DRAFT : ")
        print('\n'+ "="*50)

        prompt ="""
        you are a senior ai reviewer.
        review the following career report.
        Career Report : {draft}

        Evaluate the report on:
        1. accuracy
        2. completeness
        3. clarity
        4. practically
        5. missing information
        6. actionable advice

        Rules:
        - do not rewrite the report 
        - only provide feedback 
        - mention strengths 
        - suggest improvements
        """

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        print('\n'+ "="*50)
        print(f"REVIEWER FEEDBACK : ")
        print('\n'+ "="*50)
        print(response.text)


    def improve_draft(self, draft, feedback):
        print('\n'+ "="*50)
        print(f"IMPROVE DRAFT : ")
        print('\n'+ "="*50)

        prompt = f"""
        you are expert AI career consultant.
        below is the original report 
        ----------------
        {draft}
        -------------------
        reviewer feedback 
        {feedback}
        -------------------
        Your task:
        Rewrite the report.
        requirement:
        - address every reviewer comment.
        - keep the good sections
        - add missing information
        - make recommendation more practical
        - make roadmap more actionable 
        """

    
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        print('\n'+ "="*50)
        print(f"IMPROVE FEEDBACK : ")
        print('\n'+ "="*50)
        print(response.text)


    def reflect(self, draft):

        """draft-> Review -> Improve -> final report """
        feedback = self.review_draft(draft)

        final_report = self.improve_draft(draft, feedback)

        return final_report




