 
from google.adk.agents import Agent
import streamlit as st 

# --- Configuration (Placeholder) ---
class Config:
    worker_model = "gemini-2.5-flash"
config = Config()

# --- AGENT DEFINITION ---

topic_analyzer_agent = Agent(
    name="topic_analyzer_agent",
    model=config.worker_model,
    description="Analyzes fetched content, performing duplicate removal, recency and relevance ranking, and topic clustering.",
    instruction=f"""
    You are the **Topic Analyzer Agent**. Your role is to refine the raw content provided by the `content_fetcher_agent` before it is passed to the planner. 
    You must act as a content filter and curator.
    **Input:** A structured list of raw articles, each containing a title, summary, and URL.
    **Goal:** Produce a highly curated, small list of non-redundant, high-priority topics with 
    their best source material attached.
    **Workflow Steps:**  
    1. **Duplicate & Near-Duplicate Removal:** * Thoroughly analyze the articles for **exact duplicates** and articles that cover the **exact same news event** but are from different sources (near-duplicates).
       * **Remove all redundant entries**, keeping only the most detailed or highest-authority source for each unique topic.
    2. **Embedding-based Clustering:** * Group the remaining unique articles into coherent **main topics** (e.g., AI, ML, LLM). This process ensures related content is bundled together for the planner.
    3. **Recency and Relevance Ranking:** 
       * **Recency and Relevance Ranking:** Score each topic based on its recency (within last 7 days) and its preceived impact on the industry domains (AI, ML, LLM).
         ** consider its significance to the target domains (AI, ML, or LLM) and its perceived impact on the industry.
         ** Prioritize articles published within the last 7 days or those discussing future trends. Deprioritize any old or non-timely content.
    4. **Final Selection and Output:**
       * Select the **top-tier topics** and their associated source documents based on the combined recency and relevance  scores.
       * Output the final, refined selection as a structured list. 
       This list must be **clean, sorted by priority**, and include the title, summary, url, domain and relevance score. 
            Example Output Structure  :
    ```json
    [
        {{
            "title": "...",
            "summary": "...",
            "url": "...",
            "domain": "AI/ML/Data Science etc."
            "recency_and_relevance_score": "..."
        }},
        // ... 9 more entries
    ]
    ```
    **Crucial Rule:** The output must be perfectly clean and ready for the 
    `newsletter_planner_agent` to use directly for generating the outline sections.
    """,
    
    tools=[], 
    # The output will be the refined, clustered, and ranked list of topics
    output_key="clustered_ranked_topics",
)
 
print("✅ topic_analyzer_agent created.")

