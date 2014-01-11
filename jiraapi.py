class JiraAPI:
	import json

	class JiraLinkType:
		def __new__( self, linktype, linkissue ):
			self.type=linktype
			self.issue=linkissue
		pass

	class JiraIssueType:
		def  __new__( self, issuekey, issuelinks ):
			self.key = issuekey
			self.links = issuelinks
		pass

	def fetchIssuesFromProject( self, projectname ):
		pass
	def fetchIssue( self, issuename ):
		pass
	pass
