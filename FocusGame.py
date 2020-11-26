# Jacob Morrow
# Date: Dec 2nd, 2020
# Description: Program to play a two player game of das Spiel des Jahres 1981, Focus, also known as Domination.


class FocusGame:
    """
    Class representing 2 player game of Focus
    """

    def __init__(self, p1, p2):
        """
        Initializes player objects and board object
        :param p1: (name, piece)
        :param p2: (name, piece)
        """
        self._player1 = self.Player(p1[0], p1[1])
        self._player2 = self.Player(p2[0], p2[1])
        self._board = self.Board(p1[1], p2[1])
        self.show_board()

    def get_player_from_name(self, name):
        """2 player helper method
        :param name: player's name
        :return player"""
        if name == self._player1.get_name():
            return self._player1
        else:
            return self._player2

    def move_piece(self, name, coord0, coord1, amount):
        player = self.get_player_from_name(name)
        return self._board.move_piece(player, coord0, coord1, amount)

    def show_piece(self, coord):
        return self._board.show_piece(coord)

    def show_captured(self, name):
        return self.get_player_from_name(name).get_captured()

    def show_reserve(self, name):
        return self.get_player_from_name(name).get_reserve()

    def show_board(self):
        for row in self._board.get_board():
            print(row)

    class Player:
        """Class representing a Player"""

        def __init__(self, name, piece, captured=0, reserve=0):
            """Initializes player from name"""
            self._name = name
            self._piece = piece
            self._captured = captured
            self._reserve = reserve

        def get_name(self):
            return self._name

        def get_piece(self):
            return self._piece

        def get_captured(self):
            return self._captured

        def get_reserve(self):
            return self._reserve

        def add_captured(self, amount):
            self._captured += amount

        def add_reserve(self, amount):
            self._reserve += amount

    class Board:

        def __init__(self, p1, p2, turn=None):
            self._matrix = self.build_board(p1, p2)
            self._turn = turn

        @staticmethod
        def build_board(p1, p2):
            even_row = [list(p1), list(p1), list(p2), list(p2), list(p1), list(p1)]
            odd_row = [list(p2), list(p2), list(p1), list(p1), list(p2), list(p2)]
            matrix = [[p1, p1, p2, p2, p1, p1] if row % 2 == 0 else [p2, p2, p1, p1, p2, p2] for row in range(6)]
            # matrix = [even_row if row % 2 == 0 else odd_row for row in range(6)]
            return matrix

        def get_board(self):
            return self._matrix

        def show_piece(self, coord):
            x, y = coord[0], coord[1]
            return self._matrix[x][y]

        def move_piece(self, player, coord0, coord1, amount):
            x0, y0 = coord0[0], coord0[1]
            x1, y1 = coord1[0], coord1[1]
            tile = self._matrix[x0][y0]

            if self._turn != player and self._turn is not None:
                return 'not your turn'

            if 5 < x0 < 0 or 0 > y0 > 5 or 5 < x1 < 0 or 0 > y1 > 5:
                return 'invalid location'

            if len(tile) - amount < 0 or amount <= 0:
                return 'invalid number of pieces'

            temp = tile[len(tile) - amount:]
            self._matrix[x0][y0] = tile[:len(tile) - amount]
            self._matrix[x1][y1] += temp

            if len(self._matrix[x1][y1]) > 5:
                pass

            return 'successfully moved'


game = FocusGame(('ricky', 'r'), ('bobby', 'g'))
print(game.show_captured('ricky'))
print(game.show_captured('bobby'))
print(game.move_piece('ricky', (0, 0), (0, 2), 1))
print(game.move_piece('ricky', (0, 0), (0, 2), 1))
for i in range(6):
    for k in range(6):
        print(game.show_piece((i, k)), end="    ")
    print()

sr = 'abcdefg'
print(sr[:len(sr) - 1])
print(sr[len(sr) - 1:])
print(sr[:len(sr)-5])
