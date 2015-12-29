from jiraapi import JiraAPI

class JiraWalk:
	"""walk a Jira server collecting map of issues"""

	def expand( self ):
		"""expand graph by one link in all directions. Return true if done"""
		done = True

		thispass = self.todo
		self.todo = dict()

		for nodekey in thispass:
			node = thispass[nodekey]
			for link in node.links:
				if( self.filter.useLink( link ) ):
					if( link.inwardKey not in self.todo and link.inwardKey not in self.done and link.inwardKey not in thispass ):
						self.todo[link.inwardKey] = self.j.fetchIssue( link.inwardKey )
					elif( link.outwardKey not in self.todo and link.outwardKey not in self.done and link.outwardKey not in thispass ):
						self.todo[link.outwardKey] = self.j.fetchIssue( link.outwardKey )

					if( link not in self.links ):
						self.links.append( link )

		self.done.update( thispass )
		return len(self.todo) == 0

	def __init__(self, apiserver, entryPoints, username, password, filter):
		self.links = list()

		self.todo = dict()
		self.done = dict()
		self.j = JiraAPI(apiserver, username, password)
		self.filter = filter

		issues = list()
		for entryPoint in entryPoints.split(','):
			if( entryPoint.find('-') != -1 ):
				i = self.j.fetchIssue(entryPoint)
				if( self.filter.useIssue( i ) ):
					issues.append( i )
			else:
				for i in self.j.fetchIssuesFromProject(entryPoint):
					if( self.filter.useIssue( i ) ):
						issues.append( i )

			for issue in issues:
				self.todo[issue.key] = issue

		#each execution of this loop will expand
		#the graph by one link in all directions
		while( not self.expand() ):
			pass

		#compact data for API caller and destroy temporaries
#		for nodekey in self.done:
#			del self.done[nodekey].links
		self.nodes = self.done
		del self.done
		del self.todo
		del self.j
