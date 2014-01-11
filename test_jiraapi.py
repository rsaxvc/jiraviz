from  jiraapi import JiraAPI

j = JiraAPI()
j.fetchIssuesFromProject("JRA")
j.fetchIssue("JRA-9")
