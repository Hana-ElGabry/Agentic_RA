Here's your complete, detailed step-by-step guide to set up CrewAI with Gemini API in VSCode:

## Step 1: Check Python Version

Open VSCode terminal (Ctrl + ` or View → Terminal) and verify Python version []:

```bash
python3 --version
```

You need Python 3.10 to 3.13. If you need to update, download from python.org/downloads.[1]

## Step 2: Install UV Package Manager

UV is CrewAI's required dependency manager.[2][1]

**For Windows (in PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**For macOS/Linux (in Terminal):**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After installation, update your shell :[1]
```bash
uv tool update-shell
```

Close and reopen VSCode terminal to apply changes.[1]

## Step 3: Install CrewAI CLI

In VSCode terminal, run :[1]

```bash
uv tool install crewai
```

Verify installation :[1]
```bash
uv tool list
```

You should see: `crewai v0.102.0 - crewai` (or similar version).[1]

## Step 4: Get Gemini API Key

**Go to Google AI Studio:**
- Visit: https://aistudio.google.com/[3][4][5]
- Log in with your Google account[5]
- Click **"Get API key"** → **"Create API key"**[5]
- Copy your API key (starts with something like `AIza...`)[4][3]
[AIzaSyDFv62r34ViLIcQdNw0gYaFEERdWMnnCDI]
**This is completely free** - no credit card required.[6][7][8]

## Step 5: Create Your CrewAI Project

In VSCode terminal, navigate to where you want your project :[1]

```bash
cd C:\Users\YourName\Documents  # Windows
# or
cd ~/Documents  # macOS/Linux
```

Create your project :[9][1]
```bash
crewai create crew research_assistant
```

This creates a complete project structure :[9][1]
```
research_assistant/
├── .gitignore
├── .env                    # Your API keys go here
├── pyproject.toml
├── README.md
└── src/
    └── research_assistant/
        ├── main.py         # Run from here
        ├── crew.py         # Define your crew
        ├── config/
        │   ├── agents.yaml # Agent definitions
        │   └── tasks.yaml  # Task definitions
        └── tools/
            └── custom_tool.py
```

## Step 6: Open Project in VSCode

Open the newly created project :[2]

```bash
cd research_assistant
code .
```

This opens the project folder in VSCode.[2]

## Step 7: Configure Gemini API Key

Open the `.env` file in VSCode (it's in the root folder).[3][4]

Add your Gemini API key :[3]

```bash
# Required - use your actual API key
GEMINI_API_KEY=AIza...your-actual-key-here

# Optional: specify default model
MODEL=gemini/gemini-2.0-flash
```

**Important:** Never commit `.env` to Git - it's already in `.gitignore`.[3]

## Step 8: Install Project Dependencies

In VSCode terminal (make sure you're in the `research_assistant` folder) :[1]

```bash
crewai install
```

This installs all required dependencies including Google Gemini support.[3][1]

## Step 9: Configure Agents to Use Gemini

Open `src/research_assistant/config/agents.yaml` in VSCode.[4][9][3]

Edit it to look like this:

```yaml
research_agent:
  role: >
    Research Paper Finder
  goal: >
    Find the most relevant academic papers on {research_topic}
  backstory: >
    You are an expert at searching academic databases and finding 
    high-quality research papers. You use Semantic Scholar and arXiv 
    to find the best papers.
  llm: gemini/gemini-2.0-flash
  verbose: true

analysis_agent:
  role: >
    Research Paper Analyst
  goal: >
    Analyze and summarize academic papers to extract key findings
  backstory: >
    You are skilled at reading research papers and extracting the 
    most important information, methodologies, and conclusions.
  llm: gemini/gemini-2.0-flash
  verbose: true

quiz_agent:
  role: >
    Knowledge Assessment Specialist
  goal: >
    Create quiz questions and identify knowledge gaps
  backstory: >
    You create insightful questions to test understanding and 
    identify areas where the user needs more information.
  llm: gemini/gemini-2.0-flash
  verbose: true
```

## Step 10: Configure Tasks

Open `src/research_assistant/config/tasks.yaml` :[4][9]

```yaml
research_task:
  description: >
    Search for the top 5 most relevant academic papers about {research_topic}.
    Use Semantic Scholar or arXiv APIs to find papers with high citation counts.
    Return paper titles, authors, abstracts, and links.
  expected_output: >
    A list of 5 papers with complete metadata including titles, authors, 
    publication year, abstract, and PDF links.
  agent: research_agent

analysis_task:
  description: >
    Read and analyze the papers found by the research agent.
    Extract key findings, methodologies, and conclusions from each paper.
    Create a comprehensive summary highlighting common themes.
  expected_output: >
    A structured summary of key findings across all papers, organized by theme,
    with citations to specific papers.
  agent: analysis_agent
  context:
    - research_task

quiz_task:
  description: >
    Based on the summary, create 5 multiple-choice questions to test 
    understanding. After the user answers, identify knowledge gaps and 
    suggest areas for deeper study.
  expected_output: >
    5 quiz questions with answer options, correct answers, and a knowledge 
    gap analysis based on incorrect responses.
  agent: quiz_agent
  context:
    - analysis_task
```

## Step 11: Verify Gemini Integration in crew.py

Open `src/research_assistant/crew.py` :[4]

The file should already import the LLM class. If you want to explicitly set Gemini, add this at the top :[4][3]

```python
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

# Optional: explicitly create Gemini LLM instance
gemini_llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7
)
```

## Step 12: Test Your Setup

Run your crew :[4][1]

```bash
crewai run
```

You should see output like :[4]
```
--- Starting Research Assistant Crew ---
[research_agent] Task: Search for papers...
[research_agent] Using model: gemini/gemini-2.0-flash
...
```

## Step 13: Customize for Your Research Assistant

To add paper search functionality, create a custom tool in `src/research_assistant/tools/custom_tool.py` :[4]

```python
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests

class PaperSearchInput(BaseModel):
    """Input for paper search tool"""
    query: str = Field(..., description="Research topic to search for")
    limit: int = Field(5, description="Number of papers to return")

class SemanticScholarTool(BaseTool):
    name: str = "Semantic Scholar Search"
    description: str = "Search for academic papers using Semantic Scholar API"
    args_schema: Type[BaseModel] = PaperSearchInput

    def _run(self, query: str, limit: int = 5) -> str:
        """Search Semantic Scholar for papers"""
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": query,
            "limit": limit,
            "fields": "title,authors,abstract,year,citationCount,url"
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            papers = response.json().get("data", [])
            result = []
            
            for paper in papers:
                result.append(f"""
Title: {paper.get('title')}
Authors: {', '.join([a['name'] for a in paper.get('authors', [])])}
Year: {paper.get('year')}
Citations: {paper.get('citationCount')}
Abstract: {paper.get('abstract', 'No abstract available')}
URL: {paper.get('url')}
---
""")
            
            return "\n".join(result)
        else:
            return f"Error: Failed to fetch papers (status {response.status_code})"
```

Then register the tool in your agent configuration by editing `crew.py` :[4]

```python
from research_assistant.tools.custom_tool import SemanticScholarTool

@agent
def research_agent(self) -> Agent:
    return Agent(
        config=self.agents_config['research_agent'],
        tools=[SemanticScholarTool()],  # Add your custom tool
        verbose=True
    )
```

## Step 14: Run Complete Workflow

Test with a research topic :[4]

```bash
crewai run
```

When prompted, enter a research topic like: `"multi-agent systems in healthcare"`

## Troubleshooting Common Issues

**"Command not found: crewai"**[1]
- Run `uv tool update-shell` and restart terminal

**"GEMINI_API_KEY not found"**[3]
- Verify `.env` file has the correct key format
- Make sure you're in the project root directory when running

**"Rate limit exceeded"**[7][6]
- Gemini free tier: 15 RPM, 1,500 RPD[6][7]
- Add delays between agent calls if needed

**"Module not found"**[1]
- Run `crewai install` again
- If you need additional packages: `uv add package-name`[1]

## Quick Reference Commands

```bash
# Create new project
crewai create crew project_name

# Install dependencies
crewai install

# Add new package
uv add package-name

# Run your crew
crewai run

# Update CrewAI
uv tool install crewai --upgrade
```

## Verify Everything Works

Your terminal should show :[4]
1. Agents activating with Gemini model
2. API calls being made
3. Results from each agent
4. Final output

You now have a fully functional CrewAI setup with Gemini API running in VSCode! The entire setup is **completely free** using Google's generous Gemini API limits.[8][7][6]

[1](https://docs.crewai.com/en/installation)
[2](https://lablab.ai/t/developing-intelligent-agents-with-crewai)
[3](https://docs.crewai.com/en/concepts/llms)
[4](https://ai.google.dev/gemini-api/docs/crewai-example)
[5](https://towardsai.net/p/l/building-ai-agents-with-crew-ai-using-google-gemini-groq-llama3)
[6](https://blog.laozhang.ai/api-guides/gemini-api-free-tier/)
[7](https://ai.google.dev/gemini-api/docs/rate-limits)
[8](https://ai.google.dev/gemini-api/docs/pricing)
[9](https://docs.crewai.com/en/guides/crews/first-crew)
[10](https://www.youtube.com/watch?v=WUkQJiAlGUM)
[11](https://www.youtube.com/watch?v=07vd9dWYjyI)
[12](https://community.crewai.com/t/automated-project-notebook-gemini/2441)
[13](https://docs.crewai.com/en/quickstart)
[14](https://github.com/google-gemini/crewai-quickstart)
[15](https://www.youtube.com/watch?v=70hOObbjwFQ)
[16](https://aiagentinsider.ai/crewai-review-complete-2025-guide/)
[17](https://www.youtube.com/watch?v=SuTMYly8xXg)
[18](https://community.deeplearning.ai/t/total-beginner-how-to-install-crew-ai/838194)
[19](https://www.linkedin.com/posts/khanh-vy-nguyen0331_crewai-dockerdesktop-vscode-activity-7320079604638011393-g6wi)