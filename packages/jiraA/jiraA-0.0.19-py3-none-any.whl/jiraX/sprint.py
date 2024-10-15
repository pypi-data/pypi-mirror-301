import logging
logging.basicConfig(level=logging.INFO)
from .base import Base

class Sprint(Base):
	"""
	Class responsable for documentation sprints in Jira
	"""

	def __init__(self, user, apikey, server):
		Base.__init__(self, user, apikey, server)
		
	def find_by_board(self, board_id):
		"""
		Responsible for finding all project's sprints that user has access

		Arguments:

			board_id {Number} -- board_id of Jira

		Returns:
		
			List -- List of all sprints of the given board

		"""
		try:
			logging.info("Start function: find_by_board")
			return self.jira.sprints(board_id)
			logging.info("End funcion: find_by_board")
		except Exception as e: 
			logging.info("O quadro não aceita sprints")
			# logging.error("OS error: {0}".format(e))
			# logging.error(e.__dict__)
	
	def find_by_id(self, sprint_id):
		"""
		Responsible for finding sprints with it's id

		Arguments:

			sprint_id {String} -- sprint_id of Jira

		Returns:
		
			Sprint/None -- Sprint if found

		"""
		try:
			logging.info("Start function: find_by_id")
			return self.jira.sprint(sprint_id)			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__)

	
	def get_by_project_function(self, project, **kwargs):
		result = []
		sprints = []
		
		try:
			
			function = kwargs["function"]

			logging.info("Start function: get_by_project_function")
			result = self.find_by_project(project['key'])
			for sprint in result:
				value = sprint.__dict__
				value['project'] = project
				sprints.append(value)
				if function is not None:
					function (data=value, topic=kwargs["topic"], extra_data=kwargs["extra_data"])
				
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Sprints")
		return sprints
	
	def find_by_project(self, project_key):
		"""
		Responsible for finding all project's sprints that user has access
	
		Arguments:
	
			project_key {String} -- project_key of Jira
	
		Returns:
		
			List -- List of all sprints of the given project
	
		"""
		try:
			logging.info("Start function: find_by_project")
			sprints = []
			boards = self.jira.boards(projectKeyOrID=project_key)
			for board in boards:
				sprints.extend(self.jira.sprints(board.id))
			logging.info("End function: find_by_project")
			return sprints
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__)
	

		