class JiraAPI:
	class JiraLinkType:
		"""connects this issue to another"""
		def __init__( self, linktype, linkissue ):
			self.type=linktype
			self.key=linkissue

		def __str__( self ):
			return self.type + " " + self.key

	class JiraIssueType:
		"""represents a single JIRA issue"""
		def __init__( self, issuekey, issuelinks ):
			self.key = issuekey
			self.links = issuelinks

		def __str__( self ):
			return self.key

	"""implements a connection to a JIRA server"""
	def __init__(self, url ):
		self.url = url

		#here be dummy data
		self.issues = list()

		#some independent issues
		self.issues.append( self.JiraIssueType( "JRA-1", list() ) )
		self.issues.append( self.JiraIssueType( "JRA-2", list() ) )
		self.issues.append( self.JiraIssueType( "JRA-3", list() ) )

		blocking_A = self.JiraLinkType( "is blocking", "JRA-A" )
		blocking_B = self.JiraLinkType( "is blocking", "JRA-B" )
		blocking_C = self.JiraLinkType( "is blocking", "JRA-C" )
		blocking_Z = self.JiraLinkType( "is blocking", "JRA-Z" )
		blocked_by_A = self.JiraLinkType( "is blocked by", "JRA-A" )
		blocked_by_B = self.JiraLinkType( "is blocked by", "JRA-B" )
		blocked_by_C = self.JiraLinkType( "is blocked by", "JRA-C" )

		self.issues.append( self.JiraIssueType( "JRA-A", [blocking_Z, blocked_by_B, blocked_by_C] ) )
		self.issues.append( self.JiraIssueType( "JRA-B", [blocking_Z, blocking_A] ) )
		self.issues.append( self.JiraIssueType( "JRA-C", [blocking_Z, blocking_A] ) )

		self.issues.append( self.JiraIssueType( "JRA-Z", [blocked_by_A,blocked_by_B,blocked_by_C] ) )

	import json

	def fetchIssuesFromProject( self, projectname ):
		"""given a project name, returns a list of issues in that project"""
		#mockup
		return self.issues

	def fetchIssue( self, issuename ):
		"""given an issue name(ISSUE-n), returns that issue"""
		#mockup
		links = list()
		for issue in self.issues:
			if( issue.key == issuename ):
				return issue
		return None
