from agent.agent_core import run_agent

if __name__ == "__main__":
    # Define the goal for the agent
    objective = """
    Find all table names, locate the table containing user data, extract user details, 
    and retrieve the password for the user 'Tom'.
    """
    print(f"Objective: {objective}")
    run_agent(objective)
