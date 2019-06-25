import unittest
from unittest.mock import patch
from pulpopaul.controllers.team import get_teams, save_team, team, delete_team

class TeamControllerTestCase(unittest.TestCase):

	@patch('pulpopaul.controllers.team.Team')
	def getting_teams_test(self, mock_Team):
		mock_Team.query.assert_called_with()
		
	
		