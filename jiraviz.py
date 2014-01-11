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
nodes = list()
for issue in j.nodes:
	nodes.append( pydot.Node(str(issue), style="filled" ) )
	print issue

for node in nodes:
	graph.add_node(node)

#add all the edges
#until we have actual edge data, just hook them all together
for node in nodes:
	for othernode in nodes:
		graph.add_edge(pydot.Edge(node, othernode ) )

graph.write_png('example2_graph.png')
