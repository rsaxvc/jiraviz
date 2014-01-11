#get all the arguments with argparse
import argparse
	#API url
	#jira-project
	#username?
	#password?
	#optional-goal-issue
	#colors?
	#output-filename?

#get all the data with jiraapi
from  jiraapi import JiraAPI

#list of issues in project or user-selected issue
j = JiraAPI("jira.atlassian.com")
if( 0 ):
	#implement user-selected issues here
	jissues = j.fetchIssue("JRA-9")
else:
	jissues = j.fetchIssuesFromProject("JRA")

	#download entire graph
		#create a map of all isues we know about
		#For each link we don't have
			#download linked item, insert into map
		#repeat until we have all issues

#graph the graph with graphviz
import pydot	
# specify a directed-graph
graph = pydot.Dot(graph_type='digraph')

#add all the nodes
nodes = list()
for issue in jissues:
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
