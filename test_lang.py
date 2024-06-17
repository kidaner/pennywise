import os
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from config import NVIDIA_API_KEY

os.environ["TAVILY_API_KEY"] = "..."

def agent_grocery(city):

    tools = [TavilySearchResults(max_results=1)]

    prompt = hub.pull("hwchase17/react")

    llm = ChatNVIDIA(model="mistralai/mixtral-8x22b-instruct-v0.1", nvidia_api_key=NVIDIA_API_KEY, max_tokens=1024)

    agent = create_react_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    result = agent_executor.invoke({"input": f"What are major grocery stores in {city}?"})

    return result['output']
