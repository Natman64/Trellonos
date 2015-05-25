import re

from trellotools import Trello
from githubtools import GithubManager
from board import Board


TRELLONOS_REGEX = re.compile('^<.+>$')


class Trellonos(object):
    """ Top-level container of Trello data and core processor """

    def __init__(self, trello, github):
        self.__trello = trello
        self.__github = github

        self.__boards = {}

        meta_boards = {}
        non_meta_boards = {}

        # Iterate and initialize board objects from subscribed Trello boards
        for trello_board in trello.get_boards():
            board_name = trello_board['name']

            # Look for metaboards to find subscribed boards
            if re.search(TRELLONOS_REGEX, board_name):
                # Strip board name of tags before mapping
                board_key = board_name[1:-1]

                meta_boards[board_key] = trello_board
            else:
                non_meta_boards[board_name] = trello_board

        # next construct board objects from normal boards and meta counterparts
        for board_name in meta_boards:
            normal_board = non_meta_boards[board_name]
            meta_board = meta_boards[board_name]

            board_object = Board(trello, normal_board, meta_board)

            self.__boards[board_name] = board_object

    @classmethod
    def from_environment_vars():
        trello = Trello.from_environment_vars()
        github = GithubManager.from_environment_vars()
        return Trellonos(trello, github)

    @property
    def boards(self):
        return self.__boards

    def process(self):
        """ Runs all Trellonos processing of open boards """
        for board_key in self.__boards:
            # Run each board's processing
            board = self.__boards[board_key]

            board.process(self.__github)
