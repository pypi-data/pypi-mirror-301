import logging
logging.basicConfig(level=logging.INFO)
from .base import Base

class Board(Base):
	"""
	Class responsable for documentation boards in Jira
	"""
	ERROR = "OS error: {0}"

	def __init__(self, user, apikey, server):
		Base.__init__(self, user, apikey, server)

	def get_by_project_function(self, project, **kwargs):
		result = []
		boards = []
		
		try:
			
			function = kwargs["function"]

			logging.info("Start function: get_by_project_function")
			result = self.find_by_project(project['key'])
			for board in result:
				value = board.__dict__
				value['project'] = project
				boards.append(value)
				if function is not None:
					function (data=value, topic=kwargs["topic"], extra_data=kwargs["extra_data"])
				
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Boards")
		return boards

	def find_by_project(self, project_key):
		"""
		Responsible for finding all project's boards that user has access

		Arguments:

			project_key {String} -- project_key of Jira

		Returns:
		
			List -- List of all boards from the given project
			
		"""
		try:
			logging.info("Start function: find_by_project")
			return self.jira.boards(projectKeyOrID=project_key)
			logging.info("End funcion: find_by_project")
		except Exception as e:
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__)

	def find_by_id(self, board_id):
		"""
		Responsible for a board with given id

		Arguments:

			board_id {String} -- board_id of Jira

		Returns:
		
			Board/None -- Board if found
			
		"""
		try:
			logging.info("Start function: find_by_id")
			boards = self.jira.boards()
			if boards is None:
				return None
			for board in boards:
				if board.id == board_id:
					return board
			logging.info("End funcion: find_by_id")
		except Exception as e:
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__)

	

