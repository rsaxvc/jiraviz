#!/usr/bin/python

#get all the arguments with argparse
import argparse
parser = argparse.ArgumentParser(description='Scrape JIRA issue dependencies and graph them')
parser.add_argument("--api", help="API target, like http://jira.atlassian.com (no trailing slash)")
parser.add_argument("--entrypoint", help="Entry point, comma-separated list of JIRA issues or projects")
parser.add_argument("--username", help="username of scraper user")
parser.add_argument("--password", help="password of dedicated scraper user")
args = parser.parse_args()

if not args.api:
	args.api = "http://jira.atlassian.com"
	print "using default API server:",args.api

if not args.entrypoint:
	args.entrypoint = "CWD-3051,WBS-4"
	print "using demo API entrypoints:",args.entrypoint

#still need to add
	#output image type
	#optional-goal-issue
	#colors?
	#output-filename?
	#output-resolution?
	#max-fetch-glob - in case of angry jira server admin

#get all the data with JiraWalk
from jirawalk import JiraWalk

#start with project or user-selected issue
j = JiraWalk(args.api, args.entrypoint, args.username, args.password)

#graph the graph with graphviz
import pydot	
# specify a directed-graph
graph = pydot.Dot(graph_type='digraph',rankdir='LR')

#add all the nodes
nodes = dict()
for issue in j.nodes:
	nodes[issue.key] = pydot.Node(issue.summary, style="filled" )
	graph.add_node(nodes[issue.key])
	print issue

#add all the edges
for edge in j.edges:
	graph.add_edge( pydot.Edge(nodes[edge.tail], nodes[edge.head]) )

graph.write_svg(args.entrypoint + '.svg')
