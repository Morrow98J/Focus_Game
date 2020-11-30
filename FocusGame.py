# Jacob Morrow
# Date: Dec 2nd, 2020
# Description: Program to play a two player game of das Spiel des Jahres 1981, Focus, also known as Domination.


class FocusGame:
    """
    Class representing 2 player game of Focus
    """

    def __init__(self, p1, p2):
        """Initializes player objects and board object
        :param p1: (name, piece)
        :param p2: (name, piece)"""
        self._player1 = Player(p1[0], p1[1])
        self._player2 = Player(p2[0], p2[1])
        self._board = Board(self._player1, self._player2)

    def get_player_from_name(self, name):
        """2 player helper method
        :param name: player's name
        :return player"""
        if name == self._player1.get_name():
            return self._player1
        else:
            return self._player2

    def move_piece(self, name, coord0, coord1, amount):
        """move helper method
        :param: name: player's name
        :param: coord0: coordinates of stack to move
        :param: coord1: coordinates of position to move stack to
        :param: amount: amount of stack being moved"""
        player = self.get_player_from_name(name)
        return self._board.move_piece(player, coord0, coord1, amount)

    def show_piece(self, coord):
        """show piece helper method
        :param: coord: (x,y) of tile on board"""
        return self._board.show_piece(coord)

    def show_captured(self, name):
        """show captured helper method
        :param: name: player’s name"""
        return self.get_player_from_name(name).get_captured()

    def show_reserve(self, name):
        """show reserve helper method
        :param: name: player’s name"""
        return self.get_player_from_name(name).get_reserve()

    def reserved_move(self, name, coord):
        """move reserve helper method
        :param: name: player’s name
        :param: coord: (x,y) of tile to move to"""
        pass


class Player:
    """Class representing a Player"""

    def __init__(self, name, piece, captured=0, reserve=0):
        """Initializes player from name"""
        self._name = name
        self._piece = piece
        self._captured = captured
        self._reserve = reserve

    def get_name(self):
        """Returns player’s name"""
        return self._name

    def get_piece(self):
        """Returns player’s piece char"""
        return self._piece

    def get_captured(self):
        """Returns player’s total captured"""
        return self._captured

    def get_reserve(self):
        """Returns player’s pieces in reserve"""
        return self._reserve

    def add_captured(self, amount):
        """Adds amount to player’s captured"""
        self._captured += amount

    def add_reserve(self, amount):
        """Adds amount to player’s reserve"""
        self._reserve += amount


class Board:

    def __init__(self, p1, p2, turn=None):
        """Initializes private data members for board object
        :param: p1: player1 object
        :param: p2: player2 object
        :param: turn: current player to go"""
        self._players = p1, p2
        self._matrix = self.build_board(p1, p2)
        self._turn = turn

    @staticmethod
    def build_board(p1, p2):
        """Initializes 6x6 matrix of player objects
        :param: p1: player1 object
        :param: p2: player2 object"""
        # even_row = [list(0), list(0), list(1), list(1), list(0), list(0)]
        # odd_row = [list(1), list(1), list(0), list(0), list(1), list(1)]
        matrix = [[[p1], [p1], [p2], [p2], [p1], [p1]] if row % 2 == 0 else [[p2], [p2], [p1], [p1], [p2], [p2]] for row
                  in range(6)]
        # matrix = [even_row if row % 2 == 0 else odd_row for row in range(6)]
        return matrix

    def get_other_player(self, player):
        """Returns opposing player object
        :param: player: player object
        :return: Other player object in _players"""
        if player == self._players[0]:
            return self._players[1]
        else:
            return self._players[0]

    def show_piece(self, coord):
        """Returns stack on coord on matrix
        :param: coord: (x,y) of tile on board
        :return: matrix[x][y]"""
        x, y = coord[0], coord[1]
        pieces = []
        for player in self._matrix[x][y]:
            pieces.append(player.get_piece())
        return pieces

    def move_piece(self, player, coord0, coord1, amount):
        """Moves amount total of stack of pieces from coord0 to coord1
        :param: player: player object
        :param: coord0: coordinates (x,y) of stack to move
        :param: coord1: coordinates (x,y) of position to move stack to
        :param: amount: amount of stack being moved"""
        x0, y0 = coord0[0], coord0[1]
        x1, y1 = coord1[0], coord1[1]
        tile = self._matrix[x0][y0]

        # if amount of stack moved is too much or not enough
        if len(tile) - amount < 0 or amount <= 0:
            return False

        # if not player's turn and first turn wasn't taken
        if self._turn == player and self._turn is not None:
            return False

        # if piece at top of stack isn't player's piece
        if tile[len(tile) - 1].get_piece() != player.get_piece():
            return False

        # if out of bounds of board
        if 0 > x0 > 5 or 0 > y0 > 5 or 0 > x1 > 5 or 0 > y1 > 5:
            return False

        temp = tile[len(tile) - amount:]
        self._matrix[x0][y0] = tile[:len(tile) - amount]
        self._matrix[x1][y1] += temp

        if len(self._matrix[x1][y1]) > 5:
            self.check_stack(player, x1, y1)
        self._turn = player
        return 'successfully moved'

    def check_stack(self, player, x, y):
        """checks stack of pieces and updates player's captured
        & reserved accordingly
        :param: x: x coord of stack to check
        :param: x: x coord of stack to check"""
        check = self._matrix[x][y]
        self._matrix[x][y] = check[len(check) - 5:]
        for piece in check[:len(check) - 5]:
            if piece.get_piece() == player.get_piece():
                player.add_reserve(1)
            else:
                player.add_captured(1)

    def reserved_move(self, player, coord):
        pass


game = FocusGame(('joe', 'r'), ('bob', 'g'))
print(game.show_captured('joe'))
print(game.show_captured('bob'))
print(game.move_piece('bob', (5, 0), (0, 0), 1))
print(game.move_piece('joe', (0, 1), (0, 0), 1))
print(game.move_piece('bob', (0, 2), (0, 3), 1))
print(game.move_piece('joe', (0, 0), (0, 3), 3))
print(game.show_captured('joe'))
print(game.show_reserve('joe'))
for i in range(6):
    for k in range(6):
        print(game.show_piece((i, k)), end="    ")
    print()

sr = 'abcdefg'
print(sr)
print(sr[:len(sr) - 1])
print(sr[len(sr) - 1:])
print(sr[:len(sr) - 5])
print(sr[len(sr) - 5:])
