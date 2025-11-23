
import streamlit as st
import asyncio
import uuid
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from main_agent import root_agent
from google.genai import types as genai_types
from tools import save_draft_as_pdf # Import the function to generate HTML

from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="Newsletter Agent",
    page_icon="📰",
    layout="wide"
)

# ------------- Setup Agent + Session Layer ---------------- #
@st.cache_resource
def get_services():
    """Initialize agent runner and session storage once."""
    session_service = InMemorySessionService()

    session_id = "sess_" + str(uuid.uuid4())
    user_id = "user_streamlit"

    # create session asynchronously
    asyncio.run(
        session_service.create_session(
            app_name="app",
            user_id=user_id,
            session_id=session_id
        )
    )

    runner = Runner(
        agent=root_agent,
        app_name="app",
        session_service=session_service,
    )

    return runner, session_id, user_id


runner, session_id, user_id = get_services()


# ---------------- Streamlit UI ---------------- #
st.title("📰 Newsletter Agent")
st.write("Click the button below to start generating your newsletter automatically.")

# ------------- Session State Management ---------------- #

# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize app state for workflow control
# States: INITIAL, GENERATING, AWAITING_APPROVAL, REWORKING, APPROVED
if "app_state" not in st.session_state:
    st.session_state.app_state = "INITIAL"

# Store the latest newsletter draft
if "newsletter_draft" not in st.session_state:
    st.session_state.newsletter_draft = ""



# Display past conversation
for role, message in st.session_state.messages:
    st.chat_message(role).markdown(message)


# ---------------- Asynchronous Agent Runner ---------------- #
async def run_agent(user_input: str):
    """Runs the agent asynchronously and updates the UI."""
    # Set state to GENERATING or REWORKING
    if st.session_state.app_state == "INITIAL":
        st.session_state.app_state = "GENERATING"
    else:
        st.session_state.app_state = "REWORKING"

    # Display user message
    st.session_state.messages.append(("user", user_input))
    st.chat_message("user").markdown(user_input)

    # Prepare UI for agent response
    with st.chat_message("assistant"):
        stream_area = st.empty()
        if st.session_state.app_state == "GENERATING":
            stream_area.markdown("_Newsletter is being generated..._")
        else:
            stream_area.markdown("_Reworking the newsletter based on your feedback..._")

        # --- Main Agent Execution Loop ---
        final_text = ""  # To accumulate the full response

        trace_area = st.sidebar.expander("🛠 Execution Trace", expanded=True)
        trace_box = trace_area.empty()

        trace_logs = ""

        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=genai_types.Content(
                role="user",
                parts=[genai_types.Part.from_text(text=user_input)]
            ),
        ):

            # ---------- 1. Content Stream ----------
            if event.content and event.content.parts:
                text = event.content.parts[0].text or ""   # ensure it's a string
                # TRACE detection (safe check)
                if isinstance(text, str) and "[TRACE]" in text:
                    trace_logs += text + "\n"
                    trace_box.markdown(f"```\n{trace_logs}\n```")
                else: # Only update main display if it's not a trace
                    final_text += text
                    stream_area.markdown(final_text)

            # ---------- 2. Tool Events ----------
            if hasattr(event, "tool_event"):
                tool_name = event.tool_event.tool_name
                status = event.tool_event.status
                msg = f"[TRACE] Tool `{tool_name}` is {status}"

                trace_logs += msg + "\n"
                trace_box.markdown(f"```\n{trace_logs}\n```")

            # ---------- 3. Metadata Events ----------
            if hasattr(event, "metadata"):
                meta_text = str(event.metadata)

                if "[TRACE]" in meta_text or "agent" in meta_text.lower():
                    trace_logs += meta_text + "\n"
                    trace_box.markdown(f"```\n{trace_logs}\n```")

            # ---------- 4. Final Output (from output_key) ----------
            if hasattr(event, "metadata") and "output" in event.metadata:
                final_text = event.metadata["output"]

        # --- Post-Execution State Update ---
        st.session_state.newsletter_draft = final_text
        st.session_state.messages.append(("assistant", final_text))
        stream_area.markdown(final_text) # Display final result in the stream area
        st.session_state.app_state = "AWAITING_APPROVAL"
        st.rerun() # Rerun to show approval buttons


# ---------------- UI Interaction Logic ---------------- #

# --- 1. Initial State: Show Start Button ---
if st.session_state.app_state == "INITIAL":
    if st.button("🚀 Start Newsletter Creation"):
        asyncio.run(run_agent("Create today's newsletter."))

# --- 2. Awaiting Approval State: Show Buttons and Feedback Input ---
elif st.session_state.app_state == "AWAITING_APPROVAL":
    st.write("---")
    st.subheader("Review and Action")
    st.write("The draft is ready. Please review the newsletter above.")

    col1, col2 = st.columns(2)

    with col1:
        # Approval Button & Download Logic
        if st.button("✅ Approve and Download", use_container_width=True):
            st.session_state.app_state = "APPROVED"
            st.rerun()

    with col2:
        # The download button is shown in the APPROVED state
        pass

    # Feedback/Rework Input
    feedback = st.chat_input("Provide feedback for rework...")
    if feedback:
        rework_prompt = (
            "Please rework the previous newsletter draft based on the following feedback: "
            f"'{feedback}'. The original draft is:\n\n{st.session_state.newsletter_draft}"
        )
        asyncio.run(run_agent(rework_prompt))

# --- 3. Approved State: Show Download Button ---
elif st.session_state.app_state == "APPROVED":
    st.success("Newsletter Approved! 🎉")

    # Generate HTML content from the final markdown draft
    html_file = save_draft_as_pdf(st.session_state.newsletter_draft)

    st.download_button(
        label="📥 Download Newsletter as HTML",
        data=html_file["pdf_content"], # In tools.py, this is the HTML content in bytes
        file_name=html_file["filename"],
        mime="text/html",
    )

# --- 4. Generating/Reworking States: Show a spinner ---
elif st.session_state.app_state in ["GENERATING", "REWORKING"]:
    st.spinner(f"_{st.session_state.app_state}..._")
