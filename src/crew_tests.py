#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from crew import WebResearchAgent # type: ignore[import]

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This file is used to train and test the crew agent.
# It contains the main function that runs the crew agent and the functions to train, replay, and test the crew agent.
# this file is used for debugging and testing purposes.
# It is not intended to be used in production.

#When you execute these functions, MAKE SURE to set the environment variables for the OpenAI and Serper API keys.


# This function is used to train the crew agent on a specific topic and save the results to a file.
# run this function with the command: python crew_tests.py train <number_of_iterations> <filename>
# The number of iterations is the number of times the crew agent will run, and the filename is the name of the file where the results will be saved.
def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        WebResearchAgent().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


# This function is used to replay the crew execution from a specific task.
# run this function with the command: python crew_tests.py replay <task_id>
# to view the task_id, you can run the command: crewai log-tasks-outputs
# The task_id is the id of the task from which you want to replay the crew execution.
# This is useful for debugging and testing purposes.
def replay():
    """
    Replay the crew execution from a specific task.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    try:
        WebResearchAgent().crew().replay(task_id=sys.argv[1], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


# This function is used to test the crew execution and returns the results.
# run this function with the command: python crew_tests.py test <number_of_iterations> <openai_model_name>
# The number of iterations is the number of times the crew agent will run, and the openai_model_name is the name of the OpenAI model to be used.
# This is useful for testing the crew agent on different topics and configurations.
def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    try:
        WebResearchAgent().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")




# This function is used to test the crew agent on different obscure and difficult topics.
# run this function with the command: python crew_tests.py test_crew_agent
# The topics are defined in the topics list, and the crew agent will be tested on each topic.
def test_crew_agent():
    """
    Test the crew agent on different obscure and difficult topics.
    """
    topics = [
        "Quantum Computing",
        "Dark Matter and Dark Energy",
        "String Theory",
        "Consciousness and the Mind-Body Problem",
        "The Origin of Life on Earth",
        "The Multiverse Theory",
        "The Nature of Time",
        "The Fermi Paradox",
        "The Simulation Hypothesis",
        "The Search for Extraterrestrial Intelligence (SETI)"
    ]

    for topic in topics:
        inputs = {
            'query': f"What is the current state of research on {topic}?",
            'current_year': str(datetime.now().year)
        }
        
        try:
            WebResearchAgent().crew().kickoff(inputs=inputs)
        except Exception as e:
            raise Exception(f"An error occurred while running the crew: {e}")


