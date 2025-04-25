# WebResearchAgent Crew

Welcome to the WebResearchAgent Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Demo

You can check out a live demo of the project here: [Demo](https://web-researcher-agent-4zl5a9hlrbzvk5vodfb7pj.streamlit.app/)

## Installation

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```
Then Clone the directory and intstall the dependencies
```bash
git clone https://github.com/xezbeth/Web-Researcher-Agent.git
cd Web Research Agent
pip install -r requirements.txt
```
## Running the Project

Now run the streamlit app
```bash
cd src
streamlit run web_research_app.py
```
If you want to run some test on the individual units check out src/crew_tests.py

Make sure to add the OpenAI and Serper API keys in the streamlit app

## Support

For support, questions, or feedback regarding the WebResearchAgent Crew or crewAI.
- Check out the [documentation](documentation/docs.md)
