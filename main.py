import os
from crewai import Agent, Task, Crew, Process, LLM

# Set your Gemini API key - OFFICIAL METHOD
os.environ["GEMINI_API_KEY"] = "AIzaSyA2H_YClEXgtuIEAGKw3tI5D1Lf_yvtz0s"  # Replace with your full key

# Read API key from environment - OFFICIAL PATTERN
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini LLM - OFFICIAL FORMAT
gemini_llm = LLM(
    model='gemini/gemini-2.0-flash',
    api_key=gemini_api_key,
    temperature=0.7
)

# Define agents - OFFICIAL STRUCTURE
research_agent = Agent(
    role='Research Paper Finder',
    goal='Find relevant academic papers on {topic}',
    backstory=(
        """You are an expert at searching academic databases and finding 
        high-quality research papers. You use Semantic Scholar and arXiv 
        to find the best papers."""
    ),
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm
)

analysis_agent = Agent(
    role='Research Analyst',
    goal='Analyze and summarize papers about {topic}',
    backstory=(
        """You are skilled at reading research papers and extracting the 
        most important information, methodologies, and conclusions."""
    ),
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm
)

quiz_agent = Agent(
    role='Knowledge Assessment Specialist',
    goal='Create quiz questions and identify knowledge gaps',
    backstory=(
        """You create insightful questions to test understanding and 
        identify areas where the user needs more information."""
    ),
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm
)

# Define tasks - OFFICIAL STRUCTURE
research_task = Task(
    description=(
        """Search for 5 relevant academic papers about {topic}.
        Focus on recent publications from 2023-2025.
        Return paper titles, authors, abstracts, and key findings."""
    ),
    expected_output=(
        """A list of 5 papers with complete metadata including titles, authors, 
        publication year, abstract, and key findings."""
    ),
    agent=research_agent
)

analysis_task = Task(
    description=(
        """Read and analyze the papers found by the research agent.
        Extract key findings, methodologies, and conclusions from each paper.
        Create a comprehensive summary highlighting common themes."""
    ),
    expected_output=(
        """A structured summary of key findings across all papers, organized by theme,
        with citations to specific papers."""
    ),
    agent=analysis_agent
)

quiz_task = Task(
    description=(
        """Based on the summary, create 5 multiple-choice questions to test 
        understanding. Include correct answers and brief explanations.
        Identify potential knowledge gaps based on question difficulty."""
    ),
    expected_output=(
        """5 quiz questions with answer options, correct answers, explanations, 
        and a knowledge gap analysis."""
    ),
    agent=quiz_agent
)

# Create crew - OFFICIAL PATTERN
research_crew = Crew(
    agents=[research_agent, analysis_agent, quiz_agent],
    tasks=[research_task, analysis_task, quiz_task],
    process=Process.sequential,
    verbose=True
)

# Run the crew - OFFICIAL EXECUTION
if __name__ == "__main__":
    print("--- Starting Research Assistant Crew ---")
    result = research_crew.kickoff(inputs={"topic": "multi-agent AI systems"})
    print("\n--- Crew Execution Finished ---")
    print("\n=== FINAL RESULT ===")
    print(result)
