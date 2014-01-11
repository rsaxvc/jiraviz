class JiraAPI:
	def __init__(self, url ):
		self.url = url

	class JiraLinkType:
		def __init__( self, linktype, linkissue ):
			self.type=linktype
			self.issue=linkissue
		pass

	class JiraIssueType:
		def __init__( self, issuekey, issuelinks ):
			self.key = issuekey
			self.links = issuelinks
		pass

	import json

	def fetchIssuesFromProject( self, projectname ):
		pass
	def fetchIssue( self, issuename ):
		pass
	pass
