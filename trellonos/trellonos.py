import re

from board import Board


TRELLONOS_REGEX = re.compile('^<.+>$')


class Trellonos(object):

    def __init__(self, trello, github):
        self.__trello = trello
        self.__github = github

        self.__boards = {}

        for trello_board in trello.get_boards():
            board_name = trello_board['name']
            if re.search(TRELLONOS_REGEX, board_name):
                self.__boards[board_name[1:-1]] = Board(trello, trello_board)

    @property
    def boards(self):
        return self.__boards

    def process(self):
        for board_key in self.__boards:
            board = self.__boards[board_key]
            board.process(self.__github)