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
		return issue.status == 'Resolved' or issue.status == 'Closed'

	def useIssue(self, issue):
		"""Decide if an issue should be further explored"""
		return not self.closed( issue )

	def useLink(self,link):
		"""Decide if a link should be further explored"""
		linkTypeFilter=["blocks","clones"]
		return link.outwardType in linkTypeFilter

class jiraDecorator:
	def closed(self, issue):
		return issue.status == 'Resolved' or issue.status == 'Closed'

	def getIssueVisuals(self, issue):
		"""calculate style+color of an issue"""

		color = "lightgreen"
		for link in issue.links:
			if( link.outwardKey == issue.key and not self.closed( j.nodes[link.inwardKey] ) ):
				color = "orange"
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
		return (color,style)

	def getLinkVisuals(self, link, inwardIssue, outwardIssue ):
		if( link.outwardType == "clones" ):
			return ('black', 'solid', 'none', 1 )
		else:
			return ('black', 'solid', 'forward', 3 )

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
for issuekey in j.nodes:
	issue = j.nodes[issuekey]

	nodeText = ""
	nodeText += issue.summary
	nodeText += "\\n" + issue.key+"("+issue.status+")["+issue.priority+"]"
	if( issue.assignee != "" ):
		nodeText += "\\n" + issue.assignee

	#escape the quotes for DOT parser
	nodeText = nodeText.replace("\"","\\\"")

	(fillcolor,style) = decorator.getIssueVisuals( issue )

	issues[issue.key] = pydot.Node(
		nodeText,
		style=style,
		color="black",
		URL="\"" + args.api + "/browse/" + issue.key + "\"",
		fillcolor=fillcolor
		)
	graph.add_node(issues[issue.key])
	print issue

#add all the edges
for link in j.links:
	(color,style,dir,width) = decorator.getLinkVisuals( link, j.nodes[link.inwardKey], j.nodes[link.outwardKey] )

	graph.add_edge( pydot.Edge( issues[link.inwardKey], issues[link.outwardKey], penwidth=width, style=style, dir=dir) )
	print link

graph.write(args.filename, format=args.filetype)
