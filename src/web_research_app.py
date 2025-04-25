__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


import streamlit as st #type: ignore[import]
from datetime import datetime
import os
from langchain_openai import ChatOpenAI
from crewai_tools import SerperDevTool
import json

#This is a Streamlit app for the Web Research Agent. This creates a web interface for the Web Research Agent, 
#allowing users to input their research queries and view the results in a user-friendly format.

step_names = ["Analysing User Query...,","Searching the Web...","Scraping websites...", "Gathering collected data...", "Analysing data for accuracy...", "Generating final report..."]

#sidebar for API keys
st.sidebar.text("Input API Keys")
open_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
serper_api_key = st.sidebar.text_input("Serper API Key", type="password")

#check if API keys are set
if open_api_key and isinstance(open_api_key, str) and len(open_api_key) > 0:
    os.environ["OPENAI_API_KEY"] = open_api_key

if serper_api_key and isinstance(serper_api_key, str) and len(serper_api_key) > 0:
    os.environ["SERPER_API_KEY"] = serper_api_key

if not open_api_key or not serper_api_key:
    st.sidebar.warning("Please enter your OpenAI and Serper API keys to proceed.")

elif open_api_key and serper_api_key:
    st.sidebar.success("API keys are set. You can now run the research agent.")
    #if the API keys are set, import the WebResearchAgent class
    from crew import WebResearchAgent # type: ignore[import]


st.title("🧠 Deep Research Agent")


query = st.text_area("Enter your research query here:", height=100, placeholder="e.g. How does sunlight affect plant growth? and what are its effect on global warming?")



#check if the OpenAI API key is valid
def check_api_validation(api_key: str) -> bool:
    """
    Check if the API key is valid.
    """
    #run a simple test to check if the API key is valid
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        openai_api_key=api_key,
    )
    try:
        result = llm.invoke("This is a Health check, simply respond with {\"status\": \"ok\"} and nothing else")
        #get content from the result
        status = json.loads(result.content)["status"]
        #convert the result to a dictionary and check for the status key

        if status == "ok":
            return True
        else:
            st.error("Invalid OpenAI API key. Please check your key.")
            return False
    except Exception as e:
        #st.error("Invalid OpenAI API key. Please check your key.")
        st.error(f"An error occurred while validating the API key: {e}")
        return False
    
#check if the Serper API key is valid
def check_serper_api_validation(api_key: str) -> bool:
    """
    Check if the Serper API key is valid.
    """
    #run a simple test to check if the API key is valid
    try:
        tool = SerperDevTool(
                search_url="https://google.serper.dev/scholar",
                n_results=2,
            )

        result = tool.run(search_query="ChatGPT")
            #check for 403 client error
        if result and isinstance(result, str) and "403" in result:
            st.error("Invalid Serper API key. Please check your key.")
            return False
        else:
            return True
    except Exception as e:
        st.error("Invalid Serper API key. Please check your key.")
        #st.error(f"An error occurred while validating the Serper API key: {e}")
        return False




    
#Execute the research agent when the button is clicked
if st.button("Deep Research"):

    api_ckeck = check_api_validation(open_api_key)
    serper_check = check_serper_api_validation(serper_api_key)

    if not api_ckeck or not serper_check:
        st.error("Please enter valid API keys for the given clients.")
        st.stop()

    #make sure the query is valid and assign it to the inputs dictionary
    if query and isinstance(query, str) and len(query) > 20:

        inputs = {
                'query': query,
                'current_year': str(datetime.now().year)
            }
    else:
        st.error("Please enter a valid query. The query should be at least 20 characters long.")
        st.stop()

    # Initialize the WebResearchAgent and its crew
    agent = WebResearchAgent()
    agent_crew = agent.crew()

    #A progress bar to show the progress of the research agent. Uses the task callback to update the progress bar.
    progress = st.progress(0)
    status = st.empty()
    step_counter = {"count": 0}
    total_steps = len(agent.tasks)

    # Define task callback
    def task_callback(task_name):
        step_counter["count"] += 1
        progress.progress(min(step_counter["count"],total_steps) / total_steps,text=f"🔄 Running : {step_counter["count"]}/{total_steps} - {step_names[min(step_counter["count"],total_steps - 1)]}")        #status.text(f"✅ Completed: {task_name}")
        #print(f"✅ Completed: {task_name}")

    # Assign callbacks
    agent_crew.task_callback = task_callback



    with st.spinner("Researching..."):
        try:
            if query:
                # Run the agent with the provided inputs
                result = agent_crew.kickoff(inputs=inputs)
                st.session_state['result'] = result
            else:
                st.error("Please enter a valid query.")
                result = None
        except Exception as e:
            st.error(f"An error occurred while running the crew: {e}")
            result = None


    # Display it in the Streamlit app
    st.title("🧠 Web Research Result")
    result = st.session_state.get('result', None)

    st.markdown(result, unsafe_allow_html=True)
