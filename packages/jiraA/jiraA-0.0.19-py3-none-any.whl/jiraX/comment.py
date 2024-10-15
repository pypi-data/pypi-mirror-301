import logging
logging.basicConfig(level=logging.INFO)
from .base import Base

class Comment(Base):
	"""
	Class responsable for documentation comments in Jira
	"""
	ERROR = "OS error: {0}"

	def __init__(self, user, apikey, server):
		Base.__init__(self, user, apikey, server)
		
	def find_by_issue(self, issue_object): 
		"""
		Responsible for finding all comments from an issue

		Arguments:

			issue_object {Issue} -- issue of Jira

		Returns:
		
			List -- List of all comments from this issue
			
		"""
		try:
			logging.info("Start function: find_by_issue")
			comments = self.jira.comments(issue_object)
			if comments is not None:
				return comments
			return []
			logging.info("End function: find_by_issue")
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

	def get_by_project_function(self, project, **kwargs):
		result = []
		comments = []
		
		try:
			
			function = kwargs["function"]

			logging.info("Start function: get_by_project_function")
			result = self.find_by_project(project['key'])
			for comment in result:
				value = comment.__dict__
				value['project'] = project
				comments.append(value)
				if function is not None:
					function (data=value, topic=kwargs["topic"], extra_data=kwargs["extra_data"])
				
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Comments")
		return comments

	def find_by_project(self, project_key):
		"""
		Responsible for retrieving all comments from issues in a project

		Arguments:

			project_key {String} -- project_key of Jira

		Returns:

			List -- List of all comments from the given project

		"""
		try:
			logging.info("Start function: find_by_project")
			issues = self.jira.search_issues(f'project={project_key}', maxResults=100)
			all_comments = []
			for issue in issues:
				comments = self.find_by_issue(issue)
				all_comments.extend(comments)
			logging.info("End function: find_by_project")
			return all_comments
		except Exception as e:
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__)
			return []
