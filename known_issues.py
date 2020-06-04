#!/usr/bin/env python3

import requests
import io
import os
import sys
import json


# --- Helper funcs -----------------------------------------------
def get_board(projects, name):
    """ Given a return from projects
    https://developer.github.com/v3/projects/#list-organization-projects
    """
    for prj in projects:
        if prj['name'].lower() == name.lower():
            return prj

    #print(f'Error: no project board found matching "{name}"')
    sys.exit(1)


def get_issues(column):
    """ Given a list of cards, parse out a list of GH issues
    """
    open_issues = []
    extract_fields = (
        'number',
        'title',
        'url',
        'repository_url'
    )
    cards = requests.get(column['cards_url'], headers=headers).json()
    for crd in cards:
        if 'content_url' in crd:
            issue = requests.get(crd['content_url'], headers=headers).json()
            if issue['state'] == 'open':
                open_issues.append({k: issue[k] for k in issue if k in extract_fields})
    return open_issues


def get_project_board(gh_token, name):
    projects_url = 'https://api.github.com/orgs/OasisLMF/projects'
    open_issues = {}

    projects_list = requests.get(projects_url, headers=headers).json()
    issues_board = get_board(projects_list, name)
    issues_columns = requests.get(issues_board['columns_url'], headers=headers).json()

    for col in issues_columns:
        open_issues[col['name']] = get_issues(col)

    return open_issues


def create_markdown(issues_list, project_name, filename=None):
    # Project title
    string_buff = '\n'
    #string_buff = f'{project_name}\n'
    #string_buff += '=' * len(project_name) + '\n'

    # column header
    for board in issues_list:
        string_buff += f'\n### {board}\n'

        # Issue links
        for issue in issues_list[board]:
            repo = os.path.basename(issue['repository_url'])
            num = issue['number']
            url = 'https://github.com/' + '/'.join(issue['url'].split('/')[-4:])
            des = issue['title']
            string_buff += f'* [{repo} #{num}]({url}) - {des} \n'

    return string_buff



# --- main method ------------------------------------------------

if __name__ == "__main__":
    gh_token = sys.argv[1].strip()
    headers = {
        'Accept': 'application/vnd.github.inertia-preview+json',
        'Authorization': f'token {gh_token}'
    }

    project_board = 'known issues'
    project_issues = get_project_board(gh_token, project_board)
    print(create_markdown(project_issues, project_board))
