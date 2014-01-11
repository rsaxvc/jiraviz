class JiraAPI:
	"""implements a connection to a JIRA server"""
	def __init__(self, url ):
		self.url = url

	class JiraLinkType:
		"""connects this issue to another"""
		def __init__( self, linktype, linkissue ):
			self.type=linktype
			self.issue=linkissue

	class JiraIssueType:
		"""represents a single JIRA issue"""
		def __init__( self, issuekey, issuelinks ):
			self.key = issuekey
			self.links = issuelinks

		def __str__( self ):
			return self.key

	import json

	def fetchIssuesFromProject( self, projectname ):
		"""given a project name, returns a list of issues in that project"""
		l = list()
		l.append( self.JiraIssueType( "JRA-1", list() ) )
		l.append( self.JiraIssueType( "JRA-2", list() ) )
		l.append( self.JiraIssueType( "JRA-3", list() ) )
		return l

	def fetchIssue( self, issuename ):
		"""given an issue name(ISSUE-n), returns that issue"""
		#mockup
		return self.JiraIssueType( issuename, list() )
