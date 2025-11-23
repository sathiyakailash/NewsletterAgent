from google.adk.agents import Agent
from google.adk.tools import FunctionTool 
import streamlit as st

# --- Import Tool Definition ---
from tools import internet_search  

# --- Configuration (Placeholder) ---
# A simplified config might define the model used
class Config:
    worker_model = "gemini-2.5-flash"
config = Config()

# --- AGENT DEFINITION ---

content_fetcher_agent = Agent(
    name="content_fetcher",
    model=config.worker_model,
    description="A content retriever that uses internet search to gather recent technical articles.",
    instruction=f"""
    You are the Robust Content Fetcher Agent. 
    Your sole task is to execute a comprehensive 
    and aggressive internet search using internet_search tool and 
    deliver a diverse, high-quality articles of current tech breakthroughs in AI, Machine Learing or LLM.    
    Deliver a list of exactly 10 highly recent and authoritative articles 
    that represent a balanced mix of the following domains: AI, Machine Learning, or LLM.
    **Workflow Steps:**
    1. search the internet usnig internet_search tool and fetch results across 
    all the specified domains (AI, ML, and LLM). 
    For example, target one or two results specifically for each domain. If there are no results 
    available for a domain, then skip that domain.
    2. Each result must include:
        * The article's **Title**.
        * A concise **Summary** (snippet).
        * The **URL** to the source article.
        * The primary Domain (e.g., AI, ML or LLM).
    4. **Output Format:** You must compile the 10 selected articles into a JSON list
    **Crucial Rule:** The output must be perfectly clean and ready for the 
    `topic_analyzer_agent` to use directly for generating the prioritized list.
     
     Example Output Structure  :
    ```json
    [
        {{
            "title": "...",
            "summary": "...",
            "url": "...",
            "domain": "AI/ML/Data Science etc."
        }},
        // ... 9 more entries
    ]
    ```
    """,
    tools=[
        # Register the internet search capability
        FunctionTool(internet_search),
    ],
    # The output will be the structured list of 10 articles
    output_key="raw_fetched_articles",
)
print("✅ content_fetcher_agent created.")

 
