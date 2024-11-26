from langchain_community.chat_models import ChatOpenAI  # Updated import
from langchain.agents import Tool, create_openai_functions_agent  # New agent constructor
from tools.table_tools import find_table_names
from tools.column_tools import find_columns_for_table
from tools.user_tools import find_users_in_table
from tools.tom_tools import find_tom_details
from config.settings import OPENAI_API_KEY


def initialize_llm():
    """
    Initializes the Language Model (LLM) using ChatOpenAI from langchain_community.

    Returns:
        ChatOpenAI: A GPT-powered model for handling agent reasoning and interactions.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OpenAI API key is missing. Set it in the .env file.")
    return ChatOpenAI(model="gpt-4", temperature=0, openai_api_key=OPENAI_API_KEY)


def define_tools():
    """
    Defines the tools for the agent, wrapping utility functions from the tools package.

    Returns:
        list[Tool]: A list of LangChain Tool objects.
    """
    return [
        Tool(
            name="Find Table Names",
            func=find_table_names,
            description="Identify all table names in the database using SQL injection."
        ),
        Tool(
            name="Find Columns for a Table",
            func=find_columns_for_table,
            description="Retrieve all column names for a specific table."
        ),
        Tool(
            name="Find Users in Table",
            func=find_users_in_table,
            description="Extract user IDs from a specific table and column."
        ),
        Tool(
            name="Find Tom's Details",
            func=find_tom_details,
            description="Extract details of the user 'Tom' from a specific table."
        ),
    ]


def initialize_agent_tools():
    """
    Initializes the agent using the new constructor for OpenAI Functions Agent.

    Returns:
        AgentExecutor: The LangChain agent for executing tasks.
    """
    llm = initialize_llm()
    tools = define_tools()

    # Use the latest OpenAI Functions-based agent
    agent = create_openai_functions_agent(llm=llm, tools=tools, verbose=True)
    return agent


def run_agent(objective: str):
    """
    Runs the agent with a given objective.

    Args:
        objective (str): The goal the agent should achieve.

    Returns:
        str: The final output or result from the agent.
    """
    agent = initialize_agent_tools()
    print(f"Running agent with objective: {objective}")
    # Use invoke instead of run (latest standard)
    result = agent.invoke({"input": objective})
    print(f"Agent's Result: {result}")
    return result
