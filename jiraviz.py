#!/usr/bin/python

#get all the arguments with argparse
import argparse
parser = argparse.ArgumentParser(description='Scrape JIRA issue dependencies and graph them')
parser.add_argument(
	"--api",
	help="API target, like http://jira.atlassian.com (no trailing slash)",
	default="http://jira.atlassian.com"
	)
parser.add_argument(
	"--entrypoint",
	help="Entry point, comma-separated list of JIRA issues or projects",
	default="CWD-3051,WBS-4,JRA-30423"
	)
parser.add_argument("--username", help="username of scraper user")
parser.add_argument("--password", help="password of dedicated scraper user")
parser.add_argument("--filename", help="output filename, defaults to <entrypoint>.svg")
parser.add_argument("--filetype", help="usually guessed from filename, can be set to svg/dia/ps/png/..?")
parser.add_argument(
	"--title",
	help="Graph title",
	default="graph"
	)
args = parser.parse_args()

if args.filename:
	if not args.filetype:
		import os.path
		args.filetype = os.path.splitext(args.filename)[1][1:]
else:
	if not args.filetype:
		args.filetype = "svg"
	args.filename = args.entrypoint + "." + args.filetype

class jiraFilter:
	def closed(self, issue):
		return issue.status == 'Resolved' or issue.status == 'Closed' or issue.status == 'Done'

	def useIssue(self, issue):
		"""Decide if an issue should be further explored"""
		return not self.closed( issue )

	def useLink(self,link):
		"""Decide if a link should be further explored"""
		linkTypeFilter=["blocks","relates to"]
		return link.outwardType in linkTypeFilter

class jiraDecorator:
	def closed(self, issue):
		return issue.status == 'Resolved' or issue.status == 'Closed'

	def getIssueVisuals(self, issue):
		"""calculate style+color of an issue"""
		r = {}

		r["color"] = "black"

		#compute color - orange if blocked
		r["fillcolor"] = "green"
		for link in issue.links:
			if( link.outwardKey == issue.key ):
				if( link.inwardKey in j.issues and not self.closed( j.issues[link.inwardKey] ) ):
					if( link.outwardType == "blocks" ):
						r["fillcolor"] = "orange"
						break

		#compute issue style
		style = "\"filled,"
		if( self.closed( issue ) ):
			style += "solid"
		else:
			if( issue.assignee == "" ):
				style += "dotted"
			else:
				style += "bold"
		style += "\""
		r["style"] = style
		return r

	def getLinkVisuals(self, link, inwardIssue, outwardIssue ):
		simpleLinkTypes = ["relates to"]
		r = {}
		r["color"] = "black"
		r["style"] = "solid"
		r["tooltip"] = link.outwardType
		if( link.outwardType in simpleLinkTypes ):
			r["dir"] = "none"
			r["penwidth"] = 1
			r["constraint"] = "false"
		else:
			r["dir"] = "forward"
			r["penwidth"] = 2
		return r

#get all the data with JiraWalk
from jirawalk import JiraWalk

#start with project or user-selected issue
j = JiraWalk(args.api, args.entrypoint, args.username, args.password, jiraFilter() )

#graph the graph with graphviz
import pydot	
# specify a directed-graph
graph = pydot.Dot(
	graph_type='digraph',
	labelloc="t",
	label='\"' + args.title + '\"',
	rankdir='LR',
	remincross="True"
	)

#add all the issues
issues = dict()
decorator = jiraDecorator()
for issuekey in j.issues:
	issue = j.issues[issuekey]

	nodeText = ""
	nodeText += issue.summary
	nodeText += "\\n" + issue.key+"("+issue.status+")["+issue.priority+"]"
	if( issue.assignee != "" ):
		nodeText += "\\n" + issue.assignee

	#escape the quotes for DOT parser
	nodeText = nodeText.replace("\"","\\\"")

	issues[issue.key] = pydot.Node(
		nodeText,
		URL="\"" + args.api + "/browse/" + issue.key + "\"",
		**decorator.getIssueVisuals( issue )
		)
	graph.add_node(issues[issue.key])
	print issue

#add all the edges
for link in j.links:
	print link
	graph.add_edge( pydot.Edge( issues[link.inwardKey], issues[link.outwardKey],
		**decorator.getLinkVisuals( link, j.issues[link.inwardKey], j.issues[link.outwardKey] ) ) )

graph.write(args.filename, format=args.filetype)
