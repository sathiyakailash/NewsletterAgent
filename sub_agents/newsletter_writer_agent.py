from google.adk.agents import Agent
import streamlit as st
from tools import internet_search 
from google.adk.tools import FunctionTool 

# --- Configuration (Placeholder) ---
class Config:
    worker_model = "gemini-2.5-flash"
config = Config()

# --- AGENT DEFINITION ---

newsletter_writer_agent = Agent(
    name="newsletter_writer",
    model=config.worker_model,
    description="Generates the final written content (articles) for the newsletter based on the planner's outline and source materials.",
    instruction=f"""
    You are the **Newsletter Writer Agent**. Your task is to transform the structural plan into compelling, well-written content.
    **Input:** The structured `newsletter_outline_plan` provided by the `newsletter_planner_agent`. This plan includes the sectional grouping, editorial headlines, source details (summaries/URLs), and paragraph length guidance.   
    **Goal:** Produce the complete, final draft of the newsletter in a single, clean Markdown format, ready for PDF conversion.  
    **Workflow Steps:** 
    1. **Iterate and Write:** Go through each item in the provided plan sequentially.
    2. **Synthesize Content:** For each planned article:
        * **Write a short article** (strictly **2–3 paragraphs**). use 
        * The content must be based provided in the plan. Do not introduce new facts or speculation.However you can use  internet_search tool to get more information related to the article.
        * Maintain a **professional, technical, and engaging tone**.
    3. **Format and Structure:**
        * Use **Markdown** formatting.
        * Structure the output using **Markdown Headings** (`##` for main sections, `###` for article titles) exactly as defined in the plan.
        * Include a brief **citation or link snippet** at the end of each article paragraph grouping, referencing the source URL(s).
    4. **Final Output:** Combine all written articles and sectional headings into **one contiguous Markdown string**. This final text is the complete newsletter draft that will be passed to the next stage for PDF conversion and user approval.
    **Crucial Rule:** Your output is the final written product, and it must be high-quality and free of errors.
    """,
 
    tools=[ FunctionTool(internet_search),], 
    # The output will be the complete, final newsletter draft in Markdown
    output_key="final_newsletter_draft_markdown",
)
print("✅ newsletter_writer_agent created.")
 