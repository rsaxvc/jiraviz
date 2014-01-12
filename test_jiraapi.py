#!/usr/bin/python
from  jiraapi import JiraAPI

j = JiraAPI("https://jira.atlassian.com", None, None )

w9 = j.fetchIssue("WBS-9")
print "WBS-9:",w9

jissues = j.fetchIssuesFromProject("WBS")

print "Listing issues:"
for issue in jissues:
	print issue
	i = j.fetchIssue(issue.key)
	print "",i
	for l in i.links:
		print "","",l

print "Fetching issues individually:"
for issue in jissues:
	i = j.fetchIssue(issue.key)
	print "",i
	for l in i.links:
		print "","",l
