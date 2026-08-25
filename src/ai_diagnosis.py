import os
from google import genai

# Initialize Gemini Client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# 1. Read prompt template
with open("prompts/diagnose_prompt.md", "r") as f:
    prompt_template = f.read()

# 2. Define problem input
problem = """
A PC cannot communicate with another PC on the same network.
The switch ports are up, but the affected PC has an incorrect IP address.
Diagnose the likely root cause and suggest the fix.
"""

# 3. Inject problem into prompt
full_prompt = prompt_template.replace("{{PROBLEM}}", problem)

# 4. Generate diagnosis
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=full_prompt
)

print(response.text)