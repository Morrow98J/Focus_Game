# Jacob Morrow
# Date: Dec 1st, 2020
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
        if name.lower() == self._player1.get_name().lower():
            return self._player1
        if name.lower() == self._player2.get_name().lower():
            return self._player2
        # if name is incorrect
        return False

    def move_piece(self, name, coord0, coord1, amount):
        """move helper method
        :param: name: player's name
        :param: coord0: coordinates of stack to move
        :param: coord1: coordinates of position to move stack to
        :param: amount: amount of stack being moved"""
        player = self.get_player_from_name(name)
        return self._board.move_piece(player, coord0, coord1, amount)

    def show_pieces(self, coord):
        """show piece helper method
        :param: coord: (x,y) of tile on board"""
        return self._board.show_pieces(coord)

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
        player = self.get_player_from_name(name)
        return self._board.reserved_move(player, coord)


class Player:
    """Class representing a Player"""

    def __init__(self, name, piece, captured=0, reserve=0):
        """Initializes Player object
        :param: name: player's name
        :param: piece: player's piece
        :param: captured: player's total captured
        :param: reserve: player's total reserve"""
        self._name = name
        self._piece = piece
        self._captured = captured
        self._reserve = reserve

    def get_name(self):
        """Returns player’s name"""
        return self._name

    def get_piece(self):
        """Returns player’s piece"""
        return self._piece

    def get_captured(self):
        """Returns player’s captured"""
        return self._captured

    def get_reserve(self):
        """Returns player’s reserve"""
        return self._reserve

    def add_captured(self, amount):
        """Adds amount to player’s captured
        :param: amount: amount to be added to captured"""
        self._captured += amount

    def add_reserve(self, amount):
        """Adds amount to player’s reserve
        :param: amount: amount to be added to reserve"""
        self._reserve += amount


class Board:

    def __init__(self, p1, p2, turn=None):
        """Initializes private data members for board object
        :param: p1: player1 object
        :param: p2: player2 object
        :param: turn: current player to go"""
        self._players = p1, p2
        self._matrix = self.build_board(p1, p2)
        self.last_turn = turn

    @staticmethod
    def build_board(p1, p2):
        """Initializes 6x6 matrix of player objects
        :param: p1: player1 object
        :param: p2: player2 object"""
        matrix = [[[p1], [p1], [p2], [p2], [p1], [p1]] if row % 2 == 0 else [[p2], [p2], [p1], [p1], [p2], [p2]] for row
                  in range(6)]
        return matrix

    def show_pieces(self, coord):
        """Returns stack of pieces in list from matrix coord
        :param: coord: (x,y) of tile on board
        :return: matrix[x][y]"""
        x, y = coord[0], coord[1]
        pieces = []
        for player in self._matrix[x][y]:
            pieces.append(player.get_piece())
        return pieces

    def check_stack(self, player, x, y):
        """Removes stack pieces and updates player's
        captured & reserved accordingly
        :param: x: x coord of stack to check
        :param: x: x coord of stack to check"""
        to_check = self._matrix[x][y]
        self._matrix[x][y] = to_check[len(to_check) - 5:]

        for piece in to_check[:len(to_check) - 5]:
            if piece == player:
                player.add_reserve(1)
            else:
                player.add_captured(1)

    def move_piece(self, player, coord0, coord1, amount):
        """Moves an amount from the stack of pieces from coord0 to coord1 on matrix
        :param: player: player object
        :param: coord0: coordinates (x,y) of stack to move
        :param: coord1: coordinates (x,y) of position to move stack to
        :param: amount: amount of stack being moved"""
        x0, y0 = coord0[0], coord0[1]
        x1, y1 = coord1[0], coord1[1]
        tile = self._matrix[x0][y0]
        temp = tile[len(tile) - amount:]

        # if move is not horizontal or vertical
        if x0 != x1 and y0 != y1:
            return False
        # if move is not at stack amount
        if abs(x1 - x0) != amount and abs(y1 - y0) != amount:
            return False
        # if amount of stack moved is too much or not enough
        if len(tile) - amount < 0 or amount <= 0:
            return False
        # if not player's turn
        if self.last_turn == player:
            return False
        # if piece at top of stack isn't player's piece
        if tile[len(tile) - 1] != player:
            return False
        # if both coord out of bounds of board
        if 0 > x0 > 5 or 0 > y0 > 5 or 0 > x1 > 5 or 0 > y1 > 5:
            return False

        # move stack from coord0 to coord1
        self._matrix[x0][y0] = tile[:len(tile) - amount]
        self._matrix[x1][y1] += temp

        # if stack too large
        if len(self._matrix[x1][y1]) > 5:
            self.check_stack(player, x1, y1)

        # if game won
        if player.get_captured() == 6:
            return player.get_name() + ' Wins'

        self.last_turn = player
        return 'successfully moved'

    def reserved_move(self, player, coord):
        """Moves piece from player's reserve to coord
        :param: player: player object
        :param: coord: (x,y) of tile on board"""
        x, y = coord[0], coord[1]
        tile = self._matrix[x][y]

        # if player reserve empty
        if player.get_reserve() < 1:
            return False
        # if not player's turn
        if self.last_turn == player:
            return False
        # if out of bounds of board
        if 0 > x > 5 or 0 > y > 5:
            return False

        # add piece to stack on coord
        tile.append(player)
        player.add_reserve(-1)

        # if stack too large
        if len(tile) > 5:
            self.check_stack(player, x, y)
        # if game won
        if player.get_captured() == 6:
            return player.get_name() + ' Wins'

        self.last_turn = player
        return 'successfully moved'


if __name__ == "__main__":
    game = FocusGame(('jo', 'R'), ('ak', 'G'))
    print(game.show_captured('jo'), game.show_reserve('jo'))
    print(game.show_captured('ak'), game.show_reserve('ak'))
    print(game.move_piece('jo', (0, 1), (0, 2), 1))
    print(game.move_piece('ak', (0, 3), (0, 2), 1))
    print(game.move_piece('jo', (1, 2), (0, 2), 1))
    print(game.move_piece('ak', (2, 2), (1, 2), 1))
    print(game.move_piece('jo', (1, 3), (1, 2), 1))
    print(game.move_piece('Ak', (1, 1), (1, 2), 1))
    print(game.move_piece('jo', (0, 0), (0, 1), 1))
    print(game.move_piece('ak', (1, 2), (0, 2), 1))
    print(game.move_piece('jo', (1, 2), (0, 2), 1))
    print(game.move_piece('ak', (1, 2), (0, 2), 1))
    print(game.move_piece('jo', (0, 1), (0, 2), 1))
    print(game.move_piece('ak', (1, 4), (0, 4), 1))
    print(game.move_piece('jo', (0, 5), (0, 4), 1))
    print(game.move_piece('ak', (2, 3), (3, 3), 1))
    print(game.move_piece('jo', (0, 4), (0, 2), 2))
    print(game.move_piece('ak', (3, 3), (3, 2), 1))
    print(game.reserved_move('jo', (0, 2)))
    print(game.move_piece('ak', (3, 2), (1, 2), 2))
    print(game.reserved_move('jo', (0, 2)))
    print(game.move_piece('ak', (5, 1), (5, 0), 1))
    print(game.move_piece('jo', (4, 0), (5, 0), 1))
    print(game.move_piece('ak', (1, 2), (0, 2), 1))
    print(game.move_piece('jo', (5, 0), (2, 0), 3))
    print(game.move_piece('ak', (3, 0), (2, 0), 1))
    print(game.move_piece('jo', (2, 1), (2, 0), 1))
    print(game.move_piece('ak', (1, 0), (2, 0), 1))
    print(game.reserved_move('jo', (2, 0)))
    print(game.reserved_move('ak', (0, 3)))
    print(game.move_piece('jo', (2, 0), (2, 5), 5))
    print(game.move_piece('ak', (4, 2), (4, 3), 1))
    print(game.reserved_move('jo', (0, 2)))
    print(game.show_captured('jo'), game.show_reserve('jo'))
    print(game.show_captured('ak'), game.show_reserve('ak'))

    for i in range(6):
        for k in range(6):
            print(game.show_pieces((i, k)), (i, k), end="    ")
        print()
