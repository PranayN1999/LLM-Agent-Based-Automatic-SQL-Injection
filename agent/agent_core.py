from langchain_openai import ChatOpenAI
from langchain.agents import Tool, create_openai_functions_agent
from langchain.prompts.chat import ChatPromptTemplate
from config.settings import OPENAI_API_KEY

# Import utility functions
from tools.table_tools import find_table_names
from tools.column_tools import find_columns_for_table
from tools.user_tools import find_users_in_table
from tools.tom_tools import find_tom_details


def initialize_llm():
    """
    Initializes the Language Model (LLM) using ChatOpenAI from langchain_openai.

    Returns:
        ChatOpenAI: A GPT-powered model for handling agent reasoning and interactions.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OpenAI API key is missing. Set it in the .env file.")
    return ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=OPENAI_API_KEY)

def define_tools():
    """
    Defines the tools for the agent, wrapping utility functions from the tools package.

    Returns:
        list[Tool]: A list of LangChain Tool objects.
    """
    return [
        Tool(
            name="find_table_names",
            func=find_table_names,
            description="Identify all table names in the database."
        ),
        Tool(
            name="find_columns_for_table",
            func=find_columns_for_table,
            description="Retrieve all column names for a specific table."
        ),
        Tool(
            name="find_users_in_table",
            func=find_users_in_table,
            description="Extract user IDs from a specific table."
        ),
        Tool(
            name="find_tom_details",
            func=find_tom_details,
            description="Extract details of the user 'Tom' from the database."
        ),
    ]

def initialize_agent_tools():
    """
    Initializes the agent using the new constructor for an OpenAI-based agent.

    Returns:
        AgentExecutor: The LangChain agent for executing tasks.
    """
    llm = initialize_llm()
    tools = define_tools()

    # Dynamically generate tool descriptions
    tool_descriptions = "\n".join(
        [f"{tool.name}: {tool.description}" for tool in tools]
    )

    # Define the prompt template with the required {agent_scratchpad}
    prompt = ChatPromptTemplate.from_template(f"""
    You are an intelligent SQL agent tasked with performing the following steps:
    1. Find all table names.
    2. Identify the table containing user data.
    3. Extract user details from the database.
    4. Retrieve the password for the user 'Tom'.

    For every step, follow this reasoning process:
    - Thought: Explain what you're trying to do.
    - Action: Choose the appropriate tool and specify input.
    - Observation: Record the output from the tool.
    - Repeat until the objective is complete or a conclusion is reached.

    Tools available:
    {tool_descriptions}

    Current thoughts and actions:
    {{agent_scratchpad}}
    """)

    # Use the `create_openai_functions_agent` constructor
    agent = create_openai_functions_agent(
        llm=llm,
        tools=tools,
        prompt=prompt,
    )
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
    
    result = agent.invoke({"input": objective, "intermediate_steps": []})
    print(f"Agent's Result: {result}")
    return result

if __name__ == "__main__":
    objective = """
    Find all table names, locate the table containing user data, extract user details,
    and retrieve the password for the user 'Tom'.
    """
    run_agent(objective)
