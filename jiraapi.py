import requests
import json

class JiraAPI:
	"""implements a connection to a JIRA server. Private functions start with _"""
	class IssueLink:
		"""connects this issue to another"""
		def __init__( self, type, key ):
			self.type=type
			self.key=key

		def __str__( self ):
			return self.type + " " + self.key

	class Issue:
		"""represents a single JIRA issue"""
		def __init__( self, key, links, status, summary, priority, assignee ):
			self.key = key
			self.links = links
			self.summary = summary
			self.status = status
			self.priority = priority
			self.assignee = assignee

		def __str__( self ):
			return self.key + ":" + self.summary

	def __init__(self, baseurl, username, password ):
		self.baseurl = baseurl
		self.username = username
		self.password = password
		self.ara_throttle = 20 #angry Ron avoider

	def _runQuery( self, queryurl ):
		"""fetch/execute a query, managing basic-auth as needed"""
		#print "Querying ",queryurl
		if self.username == None or self.password == None:
			r = requests.get(queryurl, verify=False)
		else:
			r = requests.get(queryurl, verify=False, auth=(self.username, self.password) )
		return r

	def _packIssue( self, jissue ):
		"""pack a JSON issue to an Issue"""
		jfields = jissue['fields']
		jlinks = jfields['issuelinks']
		links = list()
		for jlink in jlinks:
			if( jlink['type']['name'] == 'Blocker' ):
				#atlassian style
				if 'outwardIssue' in jlink:
					links.append( self.IssueLink("blocking",jlink['outwardIssue']['key'] ) )
				elif 'inwardIssue' in jlink:
					links.append( self.IssueLink("is blocked by",jlink['inwardIssue']['key'] ) )
			elif( jlink['type']['name'] == 'Blocking' ):
				#other style
				if 'outwardIssue' in jlink:
					links.append( self.IssueLink("is blocked by",jlink['outwardIssue']['key'] ) )
				elif 'inwardIssue' in jlink:
					links.append( self.IssueLink("blocking",jlink['inwardIssue']['key'] ) )

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
			assignee
			)

	def _fetchIssueCountFromProject( self, projectname ):
		"""given a project name, returns number of issues in project"""
		projectquery = self.baseurl + "/rest/api/latest/search?jql=project=" + projectname + "&maxResults=0";
		r = self._runQuery(projectquery)
		if( r.status_code < 200 or r.status_code > 299 ):
			print "Warning:Unable to retrieve data for",projectname
		elif( not r.headers['content-type'].startswith('application/json') ):
			print "Warning:Wrong application type fetched:",r.headers['content-type']
		else:
			j = json.loads(r.text)
			return j['total']
		return 0

	def _fetchSomeIssuesFromProject( self, projectname, min, max ):
		"""given a project name, returns some of the issues from that project"""
		issues = list()
		projectquery = self.baseurl + "/rest/api/latest/search?jql=project=" + projectname + "&maxResults=" + str( max-min ) + "&startAt=" + str(min)
		r = self._runQuery( projectquery )
		if( r.status_code < 200 or r.status_code > 299 ):
			print "Warning:Unable to retrieve data for",projectname
		elif( not r.headers['content-type'].startswith('application/json') ):
			print "Warning:Wrong application type fetched:",r.headers['content-type']
		else:
			j = json.loads( r.text )
			jissues = j['issues']
			for jissue in jissues:
				issues.append( self._packIssue( jissue ) )
		return issues

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
		projectquery = self.baseurl + "/rest/api/latest/issue/" + issuename + "?expand=links"
		r = self._runQuery(projectquery)
		if( r.status_code < 200 or r.status_code > 299 ):
			print "Warning:Unable to retrieve data for",issuename
		elif( not r.headers['content-type'].startswith('application/json') ):
			print "Warning:Wrong application type fetched:",r.headers['content-type']
		else:
			jissue = json.loads(r.text)
			return self._packIssue( jissue )
		return None
