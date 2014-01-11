#get all the arguments with argparse
import argparse
	#output image type
	#API url
	#jira-project or jira-issue
	#username?
	#password?
	#optional-goal-issue
	#colors?
	#output-filename?
	#output-resolution?

api_url = "jira.atlassian.com"
entry_point = "JRA"

#get all the data with JiraWalk
from jirawalk import JiraWalk

#start with project or user-selected issue
j = JiraWalk(api_url, entry_point)

#graph the graph with graphviz
import pydot	
# specify a directed-graph
graph = pydot.Dot(graph_type='digraph')

#add all the nodes
nodes = dict()
for issue in j.nodes:
	issuename = str(issue)
	nodes[issuename] = pydot.Node(issuename, style="filled" )
	graph.add_node(nodes[issuename])
	print issue

#add all the edges
for edge in j.edges:
	graph.add_edge( pydot.Edge(nodes[edge.tail], nodes[edge.head]) )

graph.write_svg(entry_point + '.svg')
