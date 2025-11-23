import datetime
from google.adk.agents import Agent
from google.adk.tools import FunctionTool 
import os
from dotenv import load_dotenv
load_dotenv()
import logging


# --- Import Sub-Agents and Tools ---
 
from sub_agents.content_fetcher_agent import content_fetcher_agent
from sub_agents.topic_analyzer_agent import topic_analyzer_agent
from sub_agents.newsletter_planner_agent import newsletter_planner_agent
from sub_agents.newsletter_writer_agent import newsletter_writer_agent

logging.basicConfig(level=logging.INFO)

def trace(msg: str):
    """
    A tool to log a trace message. The message will be prefixed with [TRACE]
    and logged to the console. It also returns the formatted message.
    """
    logging.info(f"[TRACE] {msg}")
    return f"[TRACE] {msg}"

# --- Configuration (Placeholder) ---
# A simplified config might define the model used
class Config:
    worker_model = "gemini-2.5-flash"
config = Config()

# --- AGENT DEFINITION ---

newsletter_creator_agent = Agent(
    name="newsletter_creator_agent",
    model=config.worker_model,
    description="The main orchestrator for the AI Newsletter generation pipeline. It manages content fetching, writing, and user approval.",
    instruction=f"""
    You are the **Main Orchestrator Agent**, "The Sathya Scout". 
    Your primary goal is to produce a final newsletter draft. You have two modes of operation:
    
    1. **Initial Creation**: If the user asks to create a newsletter from scratch, execute the full content generation workflow.
    2. **Rework/Feedback**: If the user provides feedback on a previous draft, you must intelligently re-run parts of the workflow to incorporate the feedback. Usually, this means you will re-plan and re-write the content.

    **Goal:** Produce a final newsletter draft, and pass it to the user in as a 
    markdown to the streamlit app for user approval. 

    **Standard Workflow (for initial creation):**
    1. **Content Fetching:** Invoke the `content_fetcher_agent` to search the internet and retrieve a comprehensive list of the 10 most recent and authoritative articles across AI, ML, and LLM.
    2. **Topic Analysis & Filtering:** Take the output from `content_fetcher_agent` (which will be in the `raw_fetched_articles` key) and pass it as input to the `topic_analyzer_agent`. This agent will perform duplicate removal, relevance ranking, and determine the main topics, choosing 5 topics that are highly relevant and engaging.
    3. **Newsletter Planning:** Take the output from `topic_analyzer_agent` (which will be in the `clustered_ranked_topics` key) and pass it as input to the `newsletter_planner_agent`. This agent will generate a plan for the newsletter.
    4. **Newsletter Writing:** Take the output from `newsletter_planner_agent` (which will be in the `newsletter_outline_plan` key) and pass it as input to the `newsletter_writer_agent`. This agent will write a short, synthesized article (1-3 paragraphs) for each planned section, adhering strictly to the source material.
    5. **Final Output:** After the `newsletter_writer_agent` has finished, take its output (from the `final_newsletter_draft_markdown` key) and present it directly to the user as the final response.

    **Rework Workflow:** If the user provides feedback, analyze it. If it's about content or tone, you should start from step 1 (content_fetcher_agent) or step 2 (topic_analyzer_agent) or step 3 (newsletter_planner_agent) or step 4 (newsletter_writer_agent) based on the nature of the request. 
    If it is about articles itself, you should start from step 1 (content_fetcher_agent) but with new instructions based on the feedback.
    If it is about prioritization and relevance, you should start from step 2 (topic_analyzer_agent) using the output from `content_fetcher_agent` (in the `raw_fetched_articles` key) but with new instructions based on the feedback.
    If it is about structure, you should start from step 3 (newsletter_planner_agent) using the output from `topic_analyzer_agent` (in the `clustered_ranked_topics` key) but with new instructions based on the feedback.
    If it's about article specific content, you should start from step 4 (newsletter_writer_agent) using the output from `newsletter_planner_agent` (in the `newsletter_outline_plan` key) but with new instructions based on the feedback. Do not re-fetch articles unless explicitly asked to.
    
    **IMPORTANT**: Your final response to the user MUST be ONLY the markdown content of the newsletter. Do NOT include the `[TRACE]` prefix or any other conversational text in your final output.
    You MUST use the `trace` tool to log the start and end of each sub-agent execution.
    Example: `trace(msg="Starting content_fetcher_agent")`
    Example: `trace(msg="Finished content_fetcher_agent")`

    Current date: {datetime.datetime.now().strftime("%Y-%m-%d")}
    """,
    sub_agents=[
        content_fetcher_agent,
        topic_analyzer_agent,
        newsletter_planner_agent,
        newsletter_writer_agent,
    ],
    tools=[FunctionTool(trace)],
    # The output key can be used to pass the final content status back to the Streamlit app
    output_key="final_content_markdown",
)

root_agent = newsletter_creator_agent