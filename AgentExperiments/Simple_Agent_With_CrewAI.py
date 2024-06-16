##--- Reference - https://github.com/jeffara/CrewAIAutonomousAgents ---##

from crewai import Agent, Task, Crew, Process
from langchain_community.llms import Ollama
import os
from dotenv import load_dotenv

load_dotenv(os.getcwd()+"/local.env")
## print(os.getcwd())

# model = Ollama(model = "llama3")
model = Ollama(base_url="http://localhost:11434",
                                 model="llama3",
                                 verbose=True
                                 )
is_verbose = True

email = "A great offer that gets you gold"

classifier = Agent(
    role = "email classifier",
    goal = "accurately classify emails based on their importance and tag them as : Important, casual or spam",
    backstory  = "You are a good classifier. Feel free to tag the emails appropriately and help the user classify emails",
    verbose = True,
    memory = True,
    allow_delegation = False,
    llm = model
)

responder = Agent(
    role = "email responder",
    goal = "respond to emails based on their importance. First respond to the Important ones, then the casual ones and ignore the spam emails",
    backstory  = "You are a good email responder who responds accurately and honestly. Your job is to help the user respond to the emails",
    verbose = True,
    memory = True,
    allow_delegation = False,
    llm = model
)

classify_email = Task(
    description = f"Classify the following email : '{email}'",
    agent = classifier,
    expected_output = "One of the three options: 'Important', 'Casual', or 'Spam'"
)

respond_email = Task(
    description = f"Respond to the email : '{email}'",
    agent = responder,
    expected_output = "A short response to the email"
)

crew = Crew(
    agents = [classifier, responder],
    tasks = [classify_email, respond_email],
    verbose = 2,
    process = Process.sequential
)

try:
    output = crew.kickoff()
    print(output)
except Exception as E:
        raise Exception(E) from E
