from jiraapi import JiraAPI

class JiraWalk:
	"""walk a Jira server collecting map of issues"""
	class Edge:
		def __init__( self, blocked, blocked_by ):
			self.head = blocked_by
			self.tail = blocked

		def __eq__( self, other ):
			return self.head == other.head and self.tail == other.tail

		def __str__( self ):
			return self.head + " is blocked by " + self.tail

	def expand( self ):
		"""expand graph by one link in all directions. Return true if done"""
		done = True

		thispass = self.todo
		self.todo = dict()

		for nodekey in thispass:
			node = thispass[nodekey]
			for link in node.links:
				if( link.key not in self.todo and link.key not in self.done and link.key not in thispass ):
					self.todo[link.key]=self.j.fetchIssue( link.key )

				if( link.type == "is blocked by" ):
					e = self.Edge( link.key, node.key )
				elif( link.type == "blocking" ):
					e = self.Edge( node.key, link.key )
				else:
					continue

				if( e not in self.edges ):
					self.edges.append( e )

		self.done.update( thispass )
		return len(self.todo) == 0

	def __init__(self, apiserver, entryPoints, username, password, filter):
		self.edges = list()

		self.todo = dict()
		self.done = dict()
		self.j = JiraAPI(apiserver, username, password)

		issues = list()
		for entryPoint in entryPoints.split(','):
			if( entryPoint.find('-') != -1 ):
				issues.append( self.j.fetchIssue(entryPoint) )
			else:
				issues = issues + self.j.fetchIssuesFromProject(entryPoint)

			for issue in issues:
				self.todo[issue.key] = issue

		#each execution of this loop will expand
		#the graph by one edge in all directions
		while( not self.expand() ):
			pass

		#compact data for API caller and destroy temporaries
		for nodekey in self.done:
			del self.done[nodekey].links
		self.nodes = self.done
		del self.done
		del self.todo
		del self.j
