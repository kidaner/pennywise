from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
import os

os.environ["OPENAI_API_KEY"]
os.environ["TAVILY_API_KEY"]

instructions = """You are an assistant."""
base_prompt = hub.pull("langchain-ai/openai-functions-template")
prompt = base_prompt.partial(instructions=instructions)
llm = ChatOpenAI(temperature=0)
tavily_tool = TavilySearchResults()
tools = [tavily_tool]
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
)

result = agent_executor.invoke({"input": "price of tuna avocado sushi at Kroger in Cincinnati?"})
output = result.get('output')
print(output)