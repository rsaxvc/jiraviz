from jiraapi import JiraAPI

class JiraWalk:
	"""walk a Jira server collecting map of issues"""

	def expand( self ):
		"""expand graph by one link in all directions. Return true if done"""
		done = True

		thispass = self.todo
		self.todo = list()

		for node in thispass:
			i = self.j.fetchIssue( node )
			for link in i.links:
				if( link.key not in self.todo and link.key not in self.done and link.key not in thispass ):
					self.todo.append( link.key )

		self.done = self.done + thispass

		return len(self.todo) == 0

	def __init__(self, apiserver, entryPoint ):
		self.nodes = list()
		self.edges = list()

		self.todo = list()
		self.done = list()
		self.j = JiraAPI(apiserver)

		if( entryPoint.find('-') != -1 ):
			issue = self.j.fetchIssue(entryPoint)
			self.todo.append( issue.key )
		else:
			issues = self.j.fetchIssuesFromProject(entryPoint)
			for issue in issues:
				self.todo.append( issue.key )

		while( not self.expand() ):
			pass

		#compact data for API caller and destroy temporaries
		self.nodes = self.done
		del self.done
		del self.todo
		del self.j
