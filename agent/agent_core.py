from langchain_openai import ChatOpenAI
from langchain.agents import Tool, create_openai_functions_agent
from langchain.prompts.chat import ChatPromptTemplate
from config.settings import OPENAI_API_KEY

# Import utility functions
from tools.table_tools import find_table_names_tool
from tools.column_tools import find_columns_for_table_tool
from tools.user_tools import find_users_in_table_tool
from tools.tom_tools import find_tom_details_tool


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
            func=find_table_names_tool,
            description=(
                "Purpose: Retrieves all table names from the database using blind SQL injection.\n"
                "This tool handles the injection process and all interactions with the server.\n"
                "Inputs: None (any provided input will be ignored).\n"
                "Outputs: A list of all table names present in the database.\n"
                "Usage: Use this tool when you need to discover which tables exist in the database."
            ),
        ),
        Tool(
            name="find_columns_for_table",
            func=find_columns_for_table_tool,
            description=(
                "Purpose: Retrieves all column names for a specified table using blind SQL injection.\n"
                "This tool handles the injection process and all interactions with the server.\n"
                "Inputs: 'table_name' (string) — the name of the table.\n"
                "Outputs: A list of column names for the given table.\n"
                "Usage: Use this tool after identifying a table to find out what data it contains."
            ),
        ),
        Tool(
            name="find_users_in_table",
            func=find_users_in_table_tool,
            description=(
                "Purpose: Extracts all values from a specified column in a given table using blind SQL injection.\n"
                "This tool handles the injection process and all interactions with the server.\n"
                "Inputs:\n"
                "- 'table_name' (string) — the name of the table.\n"
                "- 'column_name' (string) — the name of the column from which to extract values.\n"
                "Outputs: A list of values from the specified column.\n"
                "Usage: Use this tool when you suspect a table and column may contain usernames or other relevant data."
            ),
        ),
        Tool(
            name="find_tom_details",
            func=find_tom_details_tool,
            description=(
                "Purpose: Retrieves all column values for the user 'Tom' from a specified table using blind SQL injection.\n"
                "This tool handles the injection process and all interactions with the server.\n"
                "Inputs:\n"
                "- 'table_name' (string) — the name of the table where 'Tom' is located.\n"
                "- 'column_list' (list of strings) — the columns from which to retrieve data.\n"
                "Outputs: A dictionary of column names and their corresponding values for the user 'Tom'.\n"
                "Usage: Use this tool after confirming that 'Tom' exists in a table to extract his details and find his password."
            ),
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
    prompt = ChatPromptTemplate.from_template(
        f"""
      You are an intelligent security agent working on a WebGoat page that has two sections: a login page and a register page.
      Your objective is to perform a blind SQL injection to retrieve the password for the user "Tom". You have no prior knowledge of the database schema, tables, columns, or data.
      You discovered that there is a vulnerable field in the register page. Using this vulnerability, you have created Python scripts that can interact with the database.
      These Python scripts are classified as tools, which you will use to find Tom's password.

      Tools available:
      {tool_descriptions}

      These tools are already configured with the server URL and session cookies, so you do not need to pass them as arguments.
      Each tool has a specific purpose as mentioned in its description. Use these tools strategically to find the password of the user "Tom".

      For each step, follow this reasoning process:
      - Thought: Explain what you're trying to do.
      - Action: Choose the appropriate tool and specify the input.
      - Observation: Record the output from the tool.
      - Repeat this process until you find Tom's password or reach a conclusion.

      Current thoughts and actions:
      {{agent_scratchpad}}
      """
    )

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
