#! /usr/bin/env python

import os

from trellotools import Trello
from githubtools import GithubManager
from trellonos import Trellonos

# Construct a Trello wrapper using environment variable settings
api_key = os.environ['TRELLONOS_API_KEY']
token = os.environ['TRELLONOS_TOKEN']
trello = Trello(api_key, token)

# Construct a Github wrapper using environment variable settings
username = os.environ['GITHUB_USER']
password = os.environ['GITHUB_PASSWORD']
github = GithubManager(username, password)

# Construct a Trellonos object using this components
trellonos = Trellonos(trello, github)

board = trellonos.boards['Planner']
board.create_list("Test")

new_list = board.lists['Test']
print(new_list)

new_list.archive(trello)
print(new_list.name in board.lists)
print(new_list.name in board.closed_lists)
