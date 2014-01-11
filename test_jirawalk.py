from  jirawalk import JiraWalk

print "Test:Walking project:JRA"
j = JiraWalk("jira.atlassian.com", "JRA")

print "","Printing nodes"
for node in j.nodes:
	print "","",node

print "","Printing edges"
for edge in j.edges:
	print "","",edge


print "Test:Walking issues starting with:JRA-A"
j = JiraWalk("jira.atlassian.com", "JRA-A")

print "","Printing nodes"
for node in j.nodes:
	print "","",node

print "","Printing edges"
for edge in j.edges:
	print "","",edge

