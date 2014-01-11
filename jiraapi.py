class JiraAPI:
	"""implements a connection to a JIRA server"""
	def __init__(self, url ):
		self.url = url

	class JiraLinkType:
		"""connects this issue to another"""
		def __init__( self, linktype, linkissue ):
			self.type=linktype
			self.issue=linkissue
		pass

	class JiraIssueType:
		"""represents a single JIRA issue"""
		def __init__( self, issuekey, issuelinks ):
			self.key = issuekey
			self.links = issuelinks
		pass

	import json

	def fetchIssuesFromProject( self, projectname ):
		"""given a project name, returns a list of issues in that project"""
		pass

	def fetchIssue( self, issuename ):
		"""given an issue name(ISSUE-n), returns that issue"""
		pass
	pass
