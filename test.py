import os
from crewai import LLM

# Set your API key
os.environ["GEMINI_API_KEY"] = "AIzaSyA2H_YClEXgtuIEAGKw3tI5D1Lf_yvtz0s"

# Test if key is loaded
print(f"API Key: {os.environ.get('GEMINI_API_KEY')[:15]}...")

# Try to create LLM
try:
    llm = LLM(model="gemini/gemini-2.0-flash")
    print("✅ LLM created successfully!")
    
    # Try a simple call
    response = llm.call(["Hello, are you working?"])
    print(f"✅ API call successful: {response[:100]}...")
except Exception as e:
    print(f"❌ Error: {e}")
