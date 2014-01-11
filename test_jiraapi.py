from  jiraapi import JiraAPI

j = JiraAPI("jira.atlassian.com")
j.fetchIssuesFromProject("JRA")
j.fetchIssue("JRA-9")
