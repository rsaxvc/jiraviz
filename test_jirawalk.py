#!/usr/bin/python
from  jirawalk import JiraWalk

print "Test:Walking issues starting with:WBS"
j = JiraWalk("https://jira.atlassian.com", "WBS", None, None)

print "","Printing nodes"
for node in j.nodes:
	print "","",node

print "","Printing edges"
for edge in j.edges:
	print "","",edge


print "Test:Walking issues starting with:JRA-9"
j = JiraWalk("https://jira.atlassian.com", "JRA-9", None, None)

print "","Printing nodes"
for node in j.nodes:
	print "","",node

print "","Printing edges"
for edge in j.edges:
	print "","",edge

