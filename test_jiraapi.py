from  jiraapi import JiraAPI

j = JiraAPI("jira.atlassian.com")
jissues = j.fetchIssuesFromProject("JRA")

print "Listing issues:"
for issue in jissues:
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
