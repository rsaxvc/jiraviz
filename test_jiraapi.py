from  jiraapi import JiraAPI

j = JiraAPI("https://jira.atlassian.com", None, None )
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
