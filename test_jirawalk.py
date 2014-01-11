#!/usr/bin/python
from  jirawalk import JiraWalk

print "Test:Walking project:JRA"
j = JiraWalk("https://jira.atlassian.com", "JRA", None, None)

print "","Printing nodes"
for node in j.nodes:
	print "","",node

print "","Printing edges"
for edge in j.edges:
	print "","",edge


print "Test:Walking issues starting with:JRA-A"
j = JiraWalk("https://jira.atlassian.com", "JRA-A", None, None)

print "","Printing nodes"
for node in j.nodes:
	print "","",node

print "","Printing edges"
for edge in j.edges:
	print "","",edge

