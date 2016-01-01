from jiraapi import JiraAPI

class JiraWalk:
	"""walk a Jira server collecting map of issues"""

	def expand( self ):
		"""expand graph by one link in all directions. Return true if done"""
		done = True

		thispass = self.todo
		self.todo = dict()

		for issueKey in thispass.keys():
			issue = thispass[issueKey]
			link_list = issue.links
			for link in link_list:
				if( link.inwardKey == issueKey ):
					otherKey = link.outwardKey
				else:
					otherKey = link.inwardKey

				if( otherKey in self.todo ):
					otherIssue = self.todo[otherKey]
				elif( otherKey in self.done ):
					otherIssue = self.done[otherKey]
				elif( otherKey in self.skipped ):
					continue
				elif( otherKey in thispass ):
					otherIssue = thispass[otherKey]
				else:
					otherIssue = self.j.fetchIssue( otherKey )
					if( self.filter.useIssue( otherIssue ) ):
						self.todo[otherKey] = otherIssue
					else:
						self.skipped[otherKey] = otherIssue
						continue

				if( link not in self.links ):
					if( self.filter.useLink( link ) ):
						self.links.append( link )

		self.done.update( thispass )
		return len(self.todo) == 0

	def __init__(self, apiserver, entryPoints, username, password, filter):
		self.links = list()

		self.todo = dict()
		self.done = dict()
		self.skipped = dict()
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
			if( self.filter.useIssue( issue ) ):
				self.todo[issue.key] = issue
			else:
				self.skipped[issue.key] = issue

		#each execution of this loop will expand
		#the graph by one link in all directions
		while( not self.expand() ):
			pass

		#compact data for API caller and destroy temporaries
#		for issueKey in self.done:
#			del self.done[issueKey].links
		self.issues = self.done
		del self.done
		del self.skipped
		del self.todo
		del self.j
