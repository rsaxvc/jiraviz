from  jirawalk import JiraWalk

j = JiraWalk("jira.atlassian.com", "JRA")

print "Printing nodes"
for node in j.nodes:
	print "",node

print "Printing edges"
for edge in j.edges:
	print "",edge

