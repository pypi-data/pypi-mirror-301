"""
Neon API Specifications

This module provides a set of functions to interact with the Neon API.
It includes operations for managing projects, branches, and retrieving connection URIs.

The module uses environment variables for API key management and implements
error handling and response processing for API calls.

Dependencies:
- requests: For making HTTP requests to the Neon API
- os: For environment variable handling
- dotenv: For loading environment variables from a .env file

Usage:
Ensure you have set up your Neon API key in your environment variables or .env file.
Then, you can import and use the functions provided in this module to interact with your Neon projects.
"""

import os
import requests
import logging
import psycopg2
from psycopg2 import sql
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

NEON_API_KEY = os.getenv("NEON_API_KEY")

# Base URL for the Neon API
BASE_URL = "https://console.neon.tech/api/v2"

def handle_response(response):
    """
    Handle the API response, raising exceptions for HTTP errors and returning JSON content.

    Args:
        response (requests.Response): The response object from the API call.

    Returns:
        dict: The JSON content of the response.

    Raises:
        requests.exceptions.HTTPError: If the API call was unsuccessful.
    """
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTPError: {e}")
        logger.error(f"Response status code: {response.status_code}")
        return {"error": f"HTTPError: {e}"}
    logger.info(f"Response status code: {response.status_code}")
    return response.json()

def list_projects():
    """
    List all projects for the authenticated user with selected details.

    Returns:
        dict: A dictionary containing the list of projects with id, name, region, org id, and PostgreSQL version.
    """
    url = f"{BASE_URL}/projects"
    headers = {
        "Authorization": f"Bearer {NEON_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    full_response = handle_response(response)
    
    filtered_projects = []
    for project in full_response.get("projects", []):
        filtered_project = {
            "id": project.get("id"),
            "name": project.get("name"),
            "region_id": project.get("region_id"),
            "pg_version": project.get("pg_version"),
            "org_id": project.get("org_id")
        }
        filtered_projects.append(filtered_project)
    
    return {"projects": filtered_projects}

def list_projects_with_details():
    """
    List all projects for the authenticated user with details.

    Returns:
        dict: A dictionary containing the list of projects with details.
    """
    url = f"{BASE_URL}/projects"
    headers = {
        "Authorization": f"Bearer {NEON_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return handle_response(response)

def get_project(project_id: str):
    """
    Get details of a specific project.

    Args:
        project_id (str): The ID of the project to retrieve.

    Returns:
        dict: A dictionary containing the project details.
    """
    url = f"{BASE_URL}/projects/{project_id}"
    headers = {
        "Authorization": f"Bearer {NEON_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return handle_response(response)

def create_project(name, region_id, pg_version=16):
    """
    Create a new project with the specified parameters.

    Args:
        name (str, optional): The name of the project.
        region_id (str, optional): The ID of the region for the project.
        pg_version (str, optional): The PostgreSQL version for the project. Defaults to 16.

    Returns:
        dict: A dictionary containing the details of the created project.
    """
    url = f"{BASE_URL}/projects"
    headers = {
        "Authorization": f"Bearer {NEON_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "project": {
            "pg_version": pg_version,
            "name": name,
            "region_id": region_id
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    return handle_response(response)

def delete_project(project_id):
    """
    Delete a specified project.

    This function deletes the specified project and all its associated resources,
    including endpoints, branches, databases, and users. This action is permanent
    and cannot be undone.

    Args:
        project_id (str): The ID of the project to be deleted.

    Returns:
        dict: A dictionary containing the response from the API.

    Raises:
        Exception: If there's an error in the API request or response.
    """
    url = f"{BASE_URL}/projects/{project_id}"
    headers = {
        "Authorization": f"Bearer {NEON_API_KEY}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.delete(url, headers=headers)
        return handle_response(response)
    except Exception as e:
        print(f"An error occurred while deleting the project: {str(e)}")
        raise


def get_connection_uri(project_id: str, database_name: str = "neondb", role_name: str = "neondb_owner", branch_id: str = None, endpoint_id: str = None, pooled: bool = None):
    """
    Get the connection URI for a specific database in a project.

    Args:
        project_id (str): The ID of the project.
        database_name (str, optional): The name of the database. Defaults to "neondb".
        role_name (str, optional): The name of the role. Defaults to "neondb_owner".
        branch_id (str, optional): The ID of the branch.
        endpoint_id (str, optional): The ID of the endpoint.
        pooled (bool, optional): Whether to use connection pooling.

    Returns:
        dict: A dictionary containing the connection URI.
    """
    url = f"{BASE_URL}/projects/{project_id}/connection_uri"
    headers = {
        "Authorization": f"Bearer {NEON_API_KEY}",
        "Content-Type": "application/json"
    }
    params = {
        "database_name": database_name,
        "role_name": role_name
    }
    if branch_id is not None:
        params["branch_id"] = branch_id
    if endpoint_id is not None:
        params["endpoint_id"] = endpoint_id
    if pooled is not None:
        params["pooled"] = str(pooled).lower()

    try:
        response = requests.get(url, headers=headers, params=params)
        return handle_response(response)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

def create_project_branch(project_id, parent_id=None, name=None, endpoint_type=None):
    """
    Create a new branch in a project.

    Args:
        project_id (str): The ID of the project.
        parent_id (str, optional): The ID of the parent branch.
        name (str, optional): The name of the new branch.
        endpoint_type (str, optional): The type of endpoint for the branch.

    Returns:
        dict: A dictionary containing the details of the created branch.
    """
    url = f"{BASE_URL}/projects/{project_id}/branches"
    headers = {
        "Authorization": f"Bearer {NEON_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"branch": {}}
    if parent_id is not None:
        payload["branch"]["parent_id"] = parent_id
    if name is not None:
        payload["branch"]["name"] = name
    if endpoint_type is not None:
        payload["endpoints"] = [{"type": endpoint_type}]
    
    response = requests.post(url, headers=headers, json=payload)
    return handle_response(response)

def list_project_branches(project_id):
    """
    List all branches in a project.

    Args:
        project_id (str): The ID of the project.

    Returns:
        dict: A dictionary containing the list of branches.
    """

    url = f"{BASE_URL}/projects/{project_id}/branches"
    headers = {
        "Authorization": f"Bearer {NEON_API_KEY}"
    }
    
    response = requests.get(url, headers=headers)
    return handle_response(response)

def get_project_branch(project_id, branch_id):
    """
    Get details of a specific branch in a project.

    Args:
        project_id (str): The ID of the project.
        branch_id (str): The ID of the branch.

    Returns:
        dict: A dictionary containing the branch details.
    """
    url = f"{BASE_URL}/projects/{project_id}/branches/{branch_id}"
    headers = {
        "Authorization": f"Bearer {NEON_API_KEY}"
    }
    
    response = requests.get(url, headers=headers)
    return handle_response(response)

def delete_project_branch(project_id, branch_id):
    """
    Delete a specific branch in a project.

    Args:
        project_id (str): The ID of the project.
        branch_id (str): The ID of the branch to delete.

    Returns:
        dict: A dictionary containing the result of the deletion operation.
    """
    url = f"{BASE_URL}/projects/{project_id}/branches/{branch_id}"
    headers = {
        "Authorization": f"Bearer {NEON_API_KEY}"
    }
    
    response = requests.delete(url, headers=headers)
    return handle_response(response)

def get_current_user_info():
    """
    Get current user details from the Neon API.

    This function retrieves specific information about the current Neon user account,
    including name, email, id, last name, and plan.

    Returns:
        dict: A dictionary containing the current user's information with the following keys:
              'name', 'email', 'id', 'last_name', and 'plan'.

    Raises:
        Exception: If there's an error in the API request or response.
    """
    url = f"{BASE_URL}/users/me"
    headers = {
        "Authorization": f"Bearer {NEON_API_KEY}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        user_info = handle_response(response)
        
        filtered_info = {
            'name': user_info.get('name'),
            'last_name': user_info.get('last_name'),
            'email': user_info.get('email'),
            'id': user_info.get('id'),
            'plan': user_info.get('plan')
        }
        
        if filtered_info['id']:
            logger.info(f"Successfully retrieved user info. User ID: {filtered_info['id']}")
        else:
            logger.warning("User ID not found in the response")
        
        return filtered_info
    except Exception as e:
        logger.error(f"An error occurred while getting user info: {str(e)}")
        raise

def execute_sql(connection_uri, sql_query):
    """
    Execute SQL on a Neon project.

    Args:
        connection_uri (str): The connection URI for the Neon project.
        sql (str): The SQL query to execute.

    Returns:
        dict: A dictionary containing the result of the SQL execution.
    """

    try:
        conn = psycopg2.connect(connection_uri, sslmode='require')
        cur = conn.cursor()
     
        # Execute the query
        cur.execute(sql.SQL(sql_query))
        
        # If the query is a SELECT statement, fetch the results
        if sql_query.strip().lower().startswith("select"):
            results = cur.fetchall()
        else:
            # Commit the transaction for non-SELECT queries
            conn.commit()
            results = []

        # Close the cursor and connection
        cur.close()
        
        return results
    except Exception as e:
        logger.error(f"An error occurred while executing SQL query: {str(e)}")
        raise

def fetch_database_schema(connection_uri):
    """
    Fetch the schema of the database.

    Args:
        neon_api_key (str): The Neon API key for authentication.
        database_url (str): The connection URL for the PostgreSQL database.

    Returns:
        list: A list of dictionaries containing table names and their column information.

    Raises:
        Exception: If there's an error connecting to the database or executing the query.
    """
    schema_query = """
    SELECT 
        table_name, 
        column_name, 
        data_type, 
        is_nullable
    FROM 
        information_schema.columns
    WHERE 
        table_schema = 'public'
    ORDER BY 
        table_name, ordinal_position;
    """

    try:
        results = execute_sql(connection_uri, schema_query)
        
        schema = {}
        for row in results:
            table_name, column_name, data_type, is_nullable = row
            if table_name not in schema:
                schema[table_name] = []
            schema[table_name].append({
                "column_name": column_name,
                "data_type": data_type,
                "is_nullable": is_nullable
            })

        return [{"table_name": table, "columns": columns} for table, columns in schema.items()]
    except Exception as e:
        logger.error(f"An error occurred while fetching database schema: {str(e)}")
        raise