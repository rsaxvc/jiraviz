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
import jiraapi
	#list of issues in project or user-selected issue
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
node_a = pydot.Node("JRA-1.thing1", style="filled", fillcolor="red")
node_b = pydot.Node("JRA-2.thing2", style="filled", fillcolor="green")
node_c = pydot.Node("JRA-3.thing3", style="filled", fillcolor="blue")

node_d = pydot.Node("JRA-4.thing4", style="filled", fillcolor="red")
node_e = pydot.Node("JRA-5.thing5", style="filled", fillcolor="green")

graph.add_node(node_a)
graph.add_node(node_b)
graph.add_node(node_c)

graph.add_node(node_d)
graph.add_node(node_e)

#add all the edges
graph.add_edge(pydot.Edge(node_a, node_b))
graph.add_edge(pydot.Edge(node_b, node_c))

graph.add_edge(pydot.Edge(node_d, node_e))
graph.add_edge(pydot.Edge(node_a, node_e))
graph.add_edge(pydot.Edge(node_c, node_e))

graph.write_png('example2_graph.png')
