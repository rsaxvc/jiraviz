#get all the arguments with argparse
import argparse
	#API url
	#jira-project
	#username?
	#password?
	#optional-goal-issue
	#colors?
	#output-filename?

#get all the data with JiraWalk
from  jirawalk import JiraWalk

#start with project or user-selected issue
j = JiraWalk("jira.atlassian.com", "JRA")

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

graph.write_png('example2_graph.png')
