#get all the arguments with argparse
import argparse
	#jira-project
	#username?
	#password?
	#optional-goal-issue
	#colors?

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
	#add all the nodes
	#add all the edges
