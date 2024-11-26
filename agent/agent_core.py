from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool
from tools.table_tools import find_table_names
from tools.column_tools import find_columns_for_table
from tools.user_tools import find_users_in_table
from tools.tom_tools import find_tom_details
from config.settings import OPENAI_API_KEY

def initialize_llm():
    """
    Initializes the Language Model with the specified API key and configuration.

    Returns:
        ChatOpenAI: An instance of the ChatOpenAI LLM.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OpenAI API Key is missing. Please set it in the .env file.")
    return ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)

def initialize_agent_tools():
    """
    Initializes the AI agent with the defined tools and language model.

    Returns:
        AgentExecutor: A LangChain agent ready to execute tasks.
    """
    # Initialize the LLM
    llm = initialize_llm()

    # Define tools
    tools = [
        Tool(
            name="Find Table Names",
            func=find_table_names,
            description="Finds table names in the database using blind SQL injection."
        ),
        Tool(
            name="Find Columns for Table",
            func=find_columns_for_table,
            description="Finds columns for a specific table in the database."
        ),
        Tool(
            name="Find Users in Table",
            func=find_users_in_table,
            description="Finds user IDs in a specific table and column."
        ),
        Tool(
            name="Find Tom's Details",
            func=find_tom_details,
            description="Finds details of the user 'Tom' from a specific table."
        ),
    ]

    # Initialize the agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    return agent

def run_agent(objective: str):
    """
    Executes the AI agent with the provided objective.

    Args:
        objective (str): The goal the agent should accomplish.

    Returns:
        str: The final result or output from the agent.
    """
    agent = initialize_agent_tools()
    print(f"Running agent with objective: {objective}")
    result = agent.run(objective)
    print(f"Agent's Result: {result}")
    return result
