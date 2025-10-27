Here's your complete, detailed step-by-step guide to set up CrewAI with Gemini API in VSCode:
-------------------------
1- upgrade pip
2-  pip install crewai
3-  pip install 'crewai[embeddings]'
4-  pip install -q -U google-genai
5-  pyrhon main.py
-------------------------







## Step 1: Check Python Version

Open VSCode terminal (Ctrl + ` or View → Terminal) and verify Python version []:

```bash
python3 --version
```

You need Python 3.10 to 3.13. If you need to update, download from python.org/downloads.[1]

UV installation failed. **Skip UV entirely and use pip** - this is faster for your hackathon anyway. Here's what to do:[1][2]

## Direct Solution: Install CrewAI with pip

**Step 1: Verify Python and pip are working:**

```powershell
python --version
pip --version
```

You should see Python 3.10+.[2]

**Step 2: Install CrewAI directly with pip:**

```powershell
pip install crewai
```

**Step 3: Install CrewAI tools (includes extras):**

```powershell
pip install 'crewai[tools]'
```

Wait for installation to complete.[2]

**Step 4: Verify installation:**

```powershell
python -c "import crewai; print(crewai.__version__)"
```

If this prints a version number, you're ready to go.[2]

## Create Your Project Manually (No UV CLI Needed)

Since you can't use `crewai create crew`, create your project structure manually :[1][2]

**Step 1: Create folders:**

```powershell
mkdir src
mkdir src\research_assistant
mkdir src\research_assistant\config
mkdir src\research_assistant\tools
```

**Step 2: Create your main Python file:**

In VSCode, create `main.py` in the root folder with this code :[2]

```python
from crewai import Agent, Task, Crew, LLM
import os

# Set your Gemini API key
os.environ["GEMINI_API_KEY"] = "your-api-key-here"

# Create Gemini LLM
gemini_llm = LLM(model="gemini/gemini-2.0-flash")

# Define agents
research_agent = Agent(
    role="Research Paper Finder",
    goal="Find relevant academic papers on {topic}",
    backstory="Expert at searching academic databases",
    llm=gemini_llm,
    verbose=True
)

analysis_agent = Agent(
    role="Research Analyst",
    goal="Analyze and summarize papers",
    backstory="Skilled at extracting key findings",
    llm=gemini_llm,
    verbose=True
)

quiz_agent = Agent(
    role="Knowledge Assessment Specialist",
    goal="Create quiz questions and identify knowledge gaps",
    backstory="Expert at creating insightful questions",
    llm=gemini_llm,
    verbose=True
)

# Define tasks
research_task = Task(
    description="Search for 5 papers about {topic}",
    expected_output="List of 5 papers with titles and abstracts",
    agent=research_agent
)

analysis_task = Task(
    description="Analyze the papers and create a summary",
    expected_output="Structured summary of key findings",
    agent=analysis_agent,
    context=[research_task]
)

quiz_task = Task(
    description="Create 5 quiz questions based on the summary",
    expected_output="5 questions with answers and gap analysis",
    agent=quiz_agent,
    context=[analysis_task]
)

# Create crew
crew = Crew(
    agents=[research_agent, analysis_agent, quiz_agent],
    tasks=[research_task, analysis_task, quiz_task],
    verbose=True
)

# Run
if __name__ == "__main__":
    result = crew.kickoff(inputs={"topic": "multi-agent AI systems"})
    print("\n\n=== FINAL RESULT ===")
    print(result)
```

**Step 3: Get your Gemini API key:**

1. Go to https://aistudio.google.com/
2. Click "Get API key"
3. Copy your key
4. Replace `"your-api-key-here"` in the code above[3][4]

**Step 4: Run your project:**

```powershell
python main.py
```

This should work immediately.[1][2]

## If You Get Errors

**Error: "No module named 'tiktoken'"**[2]

```powershell
pip install 'crewai[embeddings]'
```

**Error: "Failed building wheel"**[5][2]

```powershell
pip install --upgrade pip
pip install tiktoken --prefer-binary
```

**Error: "uvloop" issues (Windows)**[6]

This is a known Windows issue. Add this to the top of your `main.py`:

```python
import sys
if sys.platform == 'win32':
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
```

## Why This is Better for Your Hackathon

**No UV complications** - You're coding within 5 minutes instead of fighting installation issues.[1][2]

**Single file to start** - All code in one `main.py` makes debugging faster.[2]

**Easier for teammates** - They just need to `pip install crewai` and run your script.[1][2]

**Less abstraction** - You see exactly what each agent does, making it easier to customize.[2]

## Next Steps

1. **Test the basic setup** - Run `main.py` with the example above
2. **Add Semantic Scholar API** - Create a custom tool in the research agent
3. **Build your demo** - Focus on working functionality, not perfect project structure

You're now ready to code without UV blocking you! For a 1-day hackathon, **working code beats perfect setup** every time.[7][8][1]

[1](https://www.reddit.com/r/crewai/comments/1hrb4li/how_do_i_install_this_on_my_laptop/)
[2](https://pypi.org/project/crewai/)
[3](https://docs.crewai.com/en/concepts/llms)
[4](https://ai.google.dev/gemini-api/docs/crewai-example)
[5](https://github.com/crewAIInc/crewAI/issues/1687)
[6](https://community.crewai.com/t/error-installing-crewai-in-windows/2640)
[7](https://tecknoworks.com/how-to-win-a-hackathon/)
[8](https://stories.mlh.io/10-tips-to-win-your-next-hackathon-5afc7d97db85)
[9](https://docs.crewai.com/en/installation)
[10](https://www.youtube.com/watch?v=70hOObbjwFQ)
[11](https://github.com/crewAIInc/crewAI/issues/2409)
[12](https://community.deeplearning.ai/t/installing-crewai-in-windows-anaconda/811796)