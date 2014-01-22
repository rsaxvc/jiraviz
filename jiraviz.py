#!/usr/bin/python

#get all the arguments with argparse
import argparse
parser = argparse.ArgumentParser(description='Scrape JIRA issue dependencies and graph them')
parser.add_argument("--api", help="API target, like http://jira.atlassian.com (no trailing slash)")
parser.add_argument("--entrypoint", help="Entry point, comma-separated list of JIRA issues or projects")
parser.add_argument("--username", help="username of scraper user")
parser.add_argument("--password", help="password of dedicated scraper user")
parser.add_argument("--filename", help="output filename, defaults to <entrypoint>.svg")
parser.add_argument("--filetype", help="usually guessed from filename, can be set to svg/dia/ps/png/..?")
parser.add_argument("--title", help="Graph title")
args = parser.parse_args()

if not args.title:
	args.title = ""

if not args.api:
	args.api = "http://jira.atlassian.com"
	print "using default API server:",args.api

if not args.entrypoint:
	args.entrypoint = "CWD-3051,WBS-4,JRA-30423"
	print "using demo API entrypoints:",args.entrypoint

if args.filename:
	if not args.filetype:
		import os.path
		args.filetype = os.path.splitext(args.filename)[1][1:]
else:
	if not args.filetype:
		args.filetype = "svg"
	args.filename = args.entrypoint + "." + args.filetype

def closed(status):
	return status == 'Resolved' or status == 'Closed'

def getNodeVisuals(node, edges):
	"""calculate style+color of a node"""

	blocked = False
	for edge in j.edges:
		if( edge.head == node.key and not closed( j.nodes[edge.tail].status ) ):
			blocked = True
			break

	if( closed(node.status) ):
		color = "lightgray"
	elif( blocked ):
		if( "Optional" in node.labels ):
			color = "orange"
		else:
			color = "orangered"
	else:
		if( "Optional" in node.labels ):
			color = "greenyellow"
		else:
			color = "green"

	#compute node style
	style = "\"filled,"
	if( "Milestone" in node.labels ):
		shape = "Mcircle"
	elif( closed( node.status ) ):
		style += "solid"
		shape = "oval"
	else:
		if( node.assignee == "" ):
			style += "dotted"
			shape = "oval"
		else:
			style += "bold"
			shape = "oval"
	style += "\""
	return (color,style,shape)

#get all the data with JiraWalk
from jirawalk import JiraWalk

#start with project or user-selected issue
j = JiraWalk(args.api, args.entrypoint, args.username, args.password)

#graph the graph with graphviz
import pydot	
# specify a directed-graph
graph = pydot.Dot(
	graph_type='digraph',
	labelloc="t",
	label=args.title,
	rankdir='LR'
	)

#add all the nodes
nodes = dict()
for issuekey in j.nodes:
	issue = j.nodes[issuekey]

	nodeText = ""
	nodeText += issue.summary
	nodeText += "\\n" + issue.key+"("+issue.status+")["+issue.priority+"]"
	if( issue.assignee != "" ):
		nodeText += "\\n" + issue.assignee

	#escape the quotes for DOT parser
	nodeText = nodeText.replace("\"","\\\"")

	(fillcolor,style,shape) = getNodeVisuals( issue, j.edges )

	nodes[issue.key] = pydot.Node(
		nodeText,
		style=style,
		color="black",
		URL="\"" + args.api + "/browse/" + issue.key + "\"",
		fillcolor=fillcolor,
		shape=shape
		)
	graph.add_node(nodes[issue.key])
	print issue

#add all the edges
for edge in j.edges:
	graph.add_edge( pydot.Edge(nodes[edge.tail], nodes[edge.head], penwidth="3") )

graph.write(args.filename, format=args.filetype)
