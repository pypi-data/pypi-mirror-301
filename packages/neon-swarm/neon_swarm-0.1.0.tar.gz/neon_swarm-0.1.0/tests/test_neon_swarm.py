import unittest
from unittest.mock import patch, MagicMock
from src.neon_swarm import neon_agent_init
from swarm import Agent

class TestNeonSwarm(unittest.TestCase):

    @patch('src.neon_swarm.main.get_current_user_info')
    @patch('src.neon_swarm.main.list_projects')
    def test_neon_agent_init(self, mock_list_projects, mock_get_current_user_info):
        # Mock the return values of the API calls
        mock_get_current_user_info.return_value = {
            "name": "Test User",
            "email": "test@example.com",
            "id": "user123",
            "last_name": "Tester",
            "plan": "free"
        }
        mock_list_projects.return_value = {
            "projects": [
                {
                    "id": "project123",
                    "name": "Test Project",
                    "region_id": "aws-us-east-2",
                    "pg_version": "14",
                    "org_id": "org123"
                }
            ]
        }

        # Call the function we're testing
        print("Calling neon_agent_init...")
        agent, context_variables = neon_agent_init()
        print(f"neon_agent_init returned: agent={agent}, context_variables={context_variables}")

        # Assert that the function returns the expected types
        self.assertIsInstance(agent, Agent)
        self.assertIsInstance(context_variables, dict)

        # Assert that the context variables contain the expected keys
        self.assertIn("user_info", context_variables)
        self.assertIn("user_projects", context_variables)

        # Assert that the context variables contain the expected mock data
        expected_user_info = f"""Here is what you know about the user's info:
        {mock_get_current_user_info.return_value}
        """
        self.assertEqual(context_variables["user_info"], expected_user_info)

        expected_user_projects = f"""Here is what you know about the user's projects:
        {mock_list_projects.return_value}
        """
        self.assertEqual(context_variables["user_projects"], expected_user_projects)

        # Assert that the mocked functions were called
        mock_get_current_user_info.assert_called_once()
        mock_list_projects.assert_called_once()

        # Print the call counts for both mocked functions
        print(f"mock_get_current_user_info call count: {mock_get_current_user_info.call_count}")
        print(f"mock_list_projects call count: {mock_list_projects.call_count}")

        # You can add more specific assertions here based on your needs

if __name__ == '__main__':
    unittest.main()
