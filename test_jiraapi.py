from  jiraapi import JiraAPI

j = JiraAPI("jira.atlassian.com")
jissues = j.fetchIssuesFromProject("JRA")

for issue in jissues:
	print issue

j.fetchIssue("JRA-9")
