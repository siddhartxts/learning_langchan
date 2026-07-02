from dotenv import load_dotenv

load_dotenv()
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch






llm = ChatOpenAI(model="gpt-4o", temperature=0, max_tokens=1000)
tools = [TavilySearch()]
agent = create_agent(model=llm, tools=tools)




def main():
    print("Hello from langchain-course-main!")
    result = agent.invoke({"messages":HumanMessage(content="search for 3 job postings for an ai engineer using langchain in the bay area on linkedin and list their details")})
    print(result)



if __name__ == "__main__":
    main()
