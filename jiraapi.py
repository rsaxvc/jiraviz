import requests
import json

class JiraAPI:
	"""implements a connection to a JIRA server. Private functions start with _"""
	class IssueLink:
		"""connects this issue to another"""
		def __init__( self, inwardType, outwardType, inwardKey, outwardKey ):
			self.inwardType = inwardType
			self.outwardType = outwardType
			self.inwardKey = inwardKey
			self.outwardKey = outwardKey

		def __str__( self ):
			return self.inwardKey + " " + self.outwardType + " " + self.outwardKey

		def __eq__( self, other ):
			return self.inwardKey == other.inwardKey \
				and self.outwardKey == other.outwardKey \
				and self.inwardType == other.inwardType \
				and self.outwardType == other.outwardType

	class Issue:
		"""represents a single JIRA issue"""
		def __init__( self, key, links, status, summary, priority, assignee, labels ):
			self.key = key
			self.links = links
			self.summary = summary
			self.status = status
			self.priority = priority
			self.assignee = assignee
			self.labels = labels

		def __str__( self ):
			return self.key + ":" + self.summary

	def __init__(self, baseurl, username, password ):
		self.session = requests.Session()
		if( username and password ):
			self.session.auth = (username, password)
		self.baseurl = baseurl
		self.ara_throttle = 20 #angry Ron avoider

	def _packIssue( self, jissue ):
		"""pack a JSON issue to an Issue"""
		jfields = jissue['fields']
		jlinks = jfields['issuelinks']
		links = list()
		for jlink in jlinks:
			jtype = jlink['type']
			linkname = jtype['name']
			if 'outwardIssue' in jlink:
				links.append( self.IssueLink(jtype['inward'],jtype['outward'],jissue['key'],jlink['outwardIssue']['key'] ) )
			elif 'inwardIssue' in jlink:
				links.append( self.IssueLink(jtype['inward'],jtype['outward'],jlink['inwardIssue']['key'],jissue['key'] ) )

		labels = jfields['labels']

		if( 'priority' in jissue['fields'] and jissue['fields']['priority'] != None ):
			prio = jissue['fields']['priority']['name']
		else:
			prio = ""

		if( 'assignee' in jissue['fields'] and jissue['fields']['assignee'] != None ):
			assignee = jissue['fields']['assignee']['displayName']
		else:
			assignee = ""

		return self.Issue(
			jissue['key'],
			links,
			jissue['fields']['status']['name'],
			jissue['fields']['summary'],
			prio,
			assignee,
			labels
			)

	def _jsonQuery( self, path ):
		query = self.baseurl + path
		r = self.session.get(query)
		if( r.status_code < 200 or r.status_code > 299 ):
			print "Warning:Unable to retrieve data from:",query
			return None
		elif( not r.headers['content-type'].startswith('application/json') ):
			print "Warning:Wrong application type fetched:",r.headers['content-type']," from:",query
			return None
		else:
			return json.loads(r.text)

	def _fetchIssueCountFromProject( self, projectname ):
		"""given a project name, returns number of issues in project"""
		j = self._jsonQuery( "/rest/api/latest/search?jql=project=" + projectname + "&maxResults=0" )
		if( j ):
			return j['total']
		return 0

	def _fetchSomeIssuesFromProject( self, projectname, min, max ):
		"""given a project name, returns some of the issues from that project"""
		issues = list()
		j = self._jsonQuery( "/rest/api/latest/search?jql=project=" + projectname + "&maxResults=" + str( max-min ) + "&startAt=" + str(min) )
		if( j ):
			jissues = j['issues']
			for jissue in jissues:
				issues.append( self._packIssue( jissue ) )
			return issues
		return ()

	def fetchIssuesFromProject( self, projectname ):
		"""given a project name, returns a list of issues in that project"""
		issuecount = self._fetchIssueCountFromProject( projectname )
		issues = list()
		start = 0
		while( start < issuecount ):
			end = start + self.ara_throttle
			issues += self._fetchSomeIssuesFromProject( projectname, start, end )
			start = start + self.ara_throttle
		return issues

	def fetchIssue( self, issuename ):
		"""given an issue name(ISSUE-n), returns that issue"""
		j = self._jsonQuery( "/rest/api/latest/issue/" + issuename + "?expand=links" )
		if( j ):
			return self._packIssue( j )
		return None
