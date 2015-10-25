#!/usr/bin/python
from  jiraapi import JiraAPI


#test config
j = JiraAPI("https://jira.atlassian.com", None, None ) #set up connection
issuename="CEP-154" #a single issue to test
projectname="CEP" #a project to iterate

print "Test:Fetching",issuename
i = j.fetchIssue(issuename)
if( i.key == issuename ):
	print "","(",i.status,":",i.priority,")",i
else:
	print "","Key Mismatch!", i.key, "vs", issuename

print "Test:Enumerate issues from",projectname
jissues = j.fetchIssuesFromProject(projectname)
for issue in jissues:
	i = j.fetchIssue(issue.key)
	if( issue.key == i.key ):
		print "","(",i.status,":",i.priority,")",i
	else:
		print "","Key Mismatch!", issue.key, "vs", i.key

	for l in i.links:
		print "","",l

print "Test:Fetching enumerated issues individually from",projectname
for issue in jissues:
	i = j.fetchIssue(issue.key)
	print "","(",i.status,":",i.priority,")",i
	for l in i.links:
		print "","",l
