import logging
logging.basicConfig(level=logging.INFO)
from .base import Base

class Backlog(Base):
	"""
	Class responsable for documentation backlogs in Jira
	"""
	ERROR = "OS error: {0}"

	def __init__(self, user, apikey, server):
		Base.__init__(self, user, apikey, server)

	def get_by_project_function(self, project, **kwargs):
		result = []
		issues = []
		
		try:
			
			function = kwargs["function"]

			logging.info("Start function: get_by_project_function")
			result = self.find_by_project(project['key'])
			for issue in result:
				value = issue.__dict__
				value['project'] = project
				issues.append(value)
				if function is not None:
					function (data=value, topic=kwargs["topic"], extra_data=kwargs["extra_data"])
				
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Issues")
		return issues

	def find_by_project(self, project_key): 
		"""
		Responsible for retreving information about backlog

		Arguments:

			project_key {String} -- project_key of Jira

		Returns:
		
			List -- List of all issues from project

		"""
		try:
			logging.info("Start function: find_by_project")
			return self.jira.search_issues('project='+project_key)
			logging.info("End function: find_by_project")
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

    




