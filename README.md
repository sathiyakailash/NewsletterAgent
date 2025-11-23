## Project Overview - AutoNewsGen: Autonomous Enterprise Newsletter Planning & Generation Agent

# 1. Overview
AutoNewsGen is a multi-agent AI system designed to automate the end-to-end creation of organizational newsletters. It gathers relevant content from the internet, internal repositories, knowledge bases, and organizational communications; analyzes and prioritizes the most important items; generates a structured newsletter; formats it for publication; and routes it to the Media Manager for final approval before distribution.

Built using modular agent components, AutoNewsGen combines information retrieval, text generation, knowledge integration, workflow orchestration, and human-in-the-loop governance. The system is scalable—initially tailored for AI newsletters but expandable to any department (HR, Finance, Delivery, Accounts, Projects, etc.). It reduces manual effort, streamlines communication cycles, and ensures consistent, high-quality newsletters across the enterprise.

# 2. Problem Statement
Timely and informative newsletters are essential for organizational communication, yet producing them is labor-intensive and inconsistent. The current process requires manually browsing external news, reviewing internal documents, extracting updates from emails and project channels, drafting summaries, refining copy, formatting layouts, and coordinating approvals. This fragmented workflow often leads to delays, duplicated effort, and inconsistent quality.

In our organization, producing an AI-focused newsletter is particularly challenging due to the speed of technological change and the volume of updates. Internal teams frequently miss important news, and subject matter experts have limited time to summarize or polish content. Without an automated, scalable system, maintaining a regular and high-quality newsletter cadence is difficult.

# 3. Solution Summary

AutoNewsGen addresses these challenges through an autonomous, multi-agent workflow:

- **Content Sourcing**: Fetches AI-related (AI, LLM and Machine Learning) updates from the internet, RSS feeds, internal knowledge bases, shared mailboxes, project updates, and organizational communications. For this project, the internet is the primary source of content.
- **Relevance & Topic Analysis**: Clusters, filters, and ranks content to identify the most significant items for the current cycle.
- **Newsletter Planning**: Generates a structured outline including sections, key themes, and article groupings.
- **Content Generation**: Writes polished summaries, insights, commentary, and calls-to-action using configurable tone and style guidelines.
- **Final output**: Produces a final newsletter in Markdown/HTML, ready for front-end application distribution.
- **Approval Workflow**: Routes the draft to the Manager for review and revision before publication. Allows the user to provide feed back specific to any of the steps involved.

This design ensures automation where appropriate while maintaining human oversight for accuracy, tone, and brand compliance.

# 4. Architecture

AutoNewsGen follows a modular, extensible architecture similar to modern agent frameworks. The various components in the architecture are explained below.

**app.py** : The streamlit application defines a function run_agent that takes a query as input and returns a response from the AI Assistant. It creates a unique session ID, sets up the Google AI Assistant with a session service, and runs the root agent with the query. It then saves the draft as a HtML once the user approves the content.
**main_agent.py** : The main orchestrator Agent that coordinates all sub-agents in sequence: fetch → analyze → plan → generate → approval → publish.  

**sub_agents:** A collection of specialized agents with their respective actions they perform. 

**1. content_fetcher.py:** It retrieves news from internet (and possibly from RSS feeds, AI blogs, tech sites in future) and normalizes data into a common schema

**2. topic_analyzer.py:**  Does embedding-based clustering,. Duplicate removal and Relevance ranking (importance, freshness, internal priority flags)

**3. newsletter_planner.py:** a. Generates a structured outline and groups related articles

**4. newsletter_writer.py:** Generates polished summaries, insights, expert commentary and create a well formed and structured newsletter (future scope: Using org-specific writing tone from config)

**5. tools.py:** Defines specialized tools like save_draft_as_pdf to save the content of the newsletter post approval and internet_search custom tool for internet search for newsletter content.

# 5. Value Delivered

**1. Significant Time Savings:** Manual newsletter development often takes hours or days each cycle. AutoNewsGen reduces work by more than 70% through autonomous searching, planning, writing and formatting.

**2. Consistency and Quality:** AI-driven generation ensures consistent structure, tone, and content quality. The editor module enforces writing guidelines and corporate style.

**3. Multi-Source Intelligence:** AutoNewsGen integrates external news, internal documentation, project updates, and organizational communications—centralizing all relevant material.

**4. Scalable Across Departments:** With modular configuration and adjustable source lists, the system can support: 

- AI newsletters
- Department-specific updates (HR, Finance, Delivery)
- Account and client-specific reports
- Project highlight digests

**5. Human-in-the-Loop Governance:** Media Manager approval ensures brand alignment, fact accuracy, and communication compliance.
 
# 6. Key Learnings Demonstrated

This project implements a **multi-agent system** composed of sequential LLM-powered agents (content search → topic analyzer → content planner → newsletter writer). It uses a combination of **built-in tools (e.g., internet_search) and custom tools (e.g., save_draft_as_pdf)** to gather and process information. The Streamlit application incorporates **session/state management using an InMemorySessionService** to preserve intermediate outputs and manage the user-approval flow. Throughout the workflow, agents exchange and refine information, demonstrating effective context engineering. Additionally, the project includes **observability** features through integrated logging and tracing to monitor agent behavior and system performance.

# 7. Conclusion 

AutoNewsGen provides a powerful, extensible solution for enterprise newsletter automation. By combining autonomous content gathering, intelligent relevance assessment, structured planning, high-quality text generation, and human-supervised publishing, it transforms a traditionally manual and inconsistent process into a streamlined, repeatable workflow.

Its modular architecture ensures the system can grow beyond AI content to support any department or project across the organization. With built-in memory, evaluation, and human approval, AutoNewsGen aligns with enterprise communication needs while preserving reliability and control.

This project demonstrates the practical application of agentic AI systems in an enterprise setting—showing how multi-agent orchestration and automation can materially improve communication efficiency, content quality, and organizational visibility.