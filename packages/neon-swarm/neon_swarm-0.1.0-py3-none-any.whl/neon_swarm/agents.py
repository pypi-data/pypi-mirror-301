from swarm import Agent
from .tools import get_current_user_info, list_projects, execute_sql, fetch_database_schema, list_projects_with_details, get_project, create_project, delete_project, get_connection_uri, create_project_branch, list_project_branches, get_project_branch, delete_project_branch

def triage_instructions(context_variables):
    user_info = context_variables.get("user_info", None)
    user_projects = context_variables.get("user_projects", None)
    return f"""You are to triage a users request, and call a tool to transfer to the right intent.
    Once you are ready to transfer to the right intent, call the tool to transfer to the right intent.
    You dont need to know specifics, just the topic of the request.
    When you need more information to triage the request to an agent, ask a direct question without explaining why you're asking it.
    Do not share your thought process with the user! Do not make unreasonable assumptions on behalf of user.
    If the user intent is to query the database, you need to get the connection URI first using the get_connection_uri tool.
    The customer context is here: {user_info}, and their projects are here: {user_projects}"""

def sql_executor_instructions(context_variables):
    return f"""
    You are a PostgresSQL query executor. You are given a user query, a connection URI, or the correct SQL query to execute.
    If you don't have a the SQL query, you need to generate it using the transfer_to_query_generator tool.
    If you have a SQL query, you need to execute it using the execute_sql tool.
    You need to execute the query, and return the results.
    Mask the connection URI from the user, unless the user asks for it.
    """

def sql_generator_instructions(context_variables):
    return f"""
    You are a PostgresSQL query generator. You are given a database schema and a user query, and you need to generate the correct SQL query to execute.
    Once you have the connection URI, you need to use the fetch_database_schema tool to get the database schema.
    Once you have the database schema, you need to generate the correct SQL query to execute.
    """

def transfer_to_neon_agent():
    """
    Transfer to the Neon Agent.
    """
    return neon_agent

def transfer_to_query_executor():
    """
    Transfer to the SQL Executor agent.
    """
    return sql_executor

def transfer_to_query_generator():
    """
    Transfer to the SQL Generator agent.
    """
    return sql_generator


neon_agent = Agent(
    name="Neon Agent",
    instructions=triage_instructions,
    functions=[
        transfer_to_query_executor,
        list_projects_with_details,
        get_project,
        create_project,
        delete_project,
        get_connection_uri,
        create_project_branch,
        list_project_branches,
        get_project_branch,
        delete_project_branch
    ],
)

sql_executor = Agent(
    name="SQL Executor",
    instructions=sql_executor_instructions,
    functions=[transfer_to_query_generator, transfer_to_neon_agent, execute_sql],
)

sql_generator = Agent(
    name="SQL Generator",
    instructions=sql_generator_instructions,
    functions=[transfer_to_query_executor, fetch_database_schema],
)