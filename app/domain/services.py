# -*- coding: utf-8 -*-
from importlib import import_module
import app
import random
import string
from app.infrastructure import exceptions


class Service(object):
    _domain = None

    @app.ClassProperty
    def domain(cls):
        if cls._domain is None:
            raise exceptions.InvalidDomain('You should use a specific service implementation')
        return import_module(cls._domain)


class Match(object):

    @classmethod
    def _random_char(cls, y):
        return ''.join(random.choice(string.ascii_letters) for x in range(y))

    @classmethod
    def get_letter(cls, number):
        if number == 1:
            return 'a'
        if number == 2:
            return 'b'
        if number == 3:
            return 'c'
        if number == 4:
            return 'd'
        if number == 5:
            return 'e'
        if number == 6:
            return 'f'
        if number == 7:
            return 'g'
        if number == 8:
            return 'h'
        return cls._random_char(2)

    @classmethod
    def _get_letter_number(cls, number):
        if number == 'a':
            return 1
        if number == 'b':
            return 2
        if number == 'c':
            return 3
        if number == 'd':
            return 4
        if number == 'e':
            return 5
        if number == 'f':
            return 6
        if number == 'g':
            return 7
        if number == 'h':
            return 8

    @classmethod
    def _get_knight_moviments(cls, row, col, limits):
        moviments = []
        default = ''
        knight_01 = default
        knight_02 = default
        knight_03 = default
        knight_04 = default
        knight_05 = default
        knight_06 = default
        knight_07 = default
        knight_08 = default

        if row + 2 < limits['limit_up_row'] and col - 1 > limits['limit_left_col']:
            knight_01 = f'{row + 2}{cls.get_letter(col -1)}'
        if row + 2 < limits['limit_up_row'] and col + 1 < limits['limit_right_col']:
            knight_02 = f'{row + 2}{cls.get_letter(col + 1)}'

        if row + 1 < limits['limit_up_row'] and col - 2 > limits['limit_left_col']:
            knight_03 = f'{row + 1}{cls.get_letter(col - 2)}'
        if row + 1 < limits['limit_up_row'] and col + 2 < limits['limit_right_col']:
            knight_04 = f'{row + 1}{cls.get_letter(col + 2)}'

        if row - 1 > limits['limit_down_row'] and col - 2 > limits['limit_left_col']:
            knight_05 = f'{row - 1}{cls.get_letter(col - 2)}'
        if row - 1 > limits['limit_down_row'] and col + 2 < limits['limit_right_col']:
            knight_06 = f'{row - 1}{cls.get_letter(col + 2)}'

        if row - 2 > limits['limit_down_row'] and col - 1 > limits['limit_left_col']:
            knight_07 = f'{row - 2}{cls.get_letter(col -1 )}'
        if row - 2 > limits['limit_down_row'] and col + 1 < limits['limit_right_col']:
            knight_08 = f'{row - 2}{cls.get_letter(col + 1)}'

        moviments.append({'kinight_01': knight_01})
        moviments.append({'kinight_02': knight_02})
        moviments.append({'kinight_03': knight_03})
        moviments.append({'kinight_04': knight_04})
        moviments.append({'kinight_05': knight_05})
        moviments.append({'kinight_06': knight_06})
        moviments.append({'kinight_07': knight_07})
        moviments.append({'kinight_08': knight_08})
        return moviments

    @classmethod
    def _get_moviments(cls, position, piece_type, configuration):
        row = int(position[0])
        col = cls._get_letter_number(position[1])
        limits = {
            'limit_up_row': configuration['row_length'] if 'row_length' in configuration else 9,
            'limit_down_row': 0,
            'limit_right_col': configuration['col_length'] if 'col_length' in configuration else 9,
            'limit_left_col': 0
        }

        if piece_type == "KNIGHT":
            return cls._get_knight_moviments(row, col, limits)

        raise exceptions.PieceTypeInvalid(f'Could not find movement for type {piece_type}')

    @classmethod
    def _get_possibilities(cls, moviments, piece, board):
        piece_type = piece.type
        if piece_type == "KNIGHT":
            return cls._get_possibilities_for_knight(moviments, piece, board)
        raise exceptions.PieceTypeInvalid(f'Could not find possibility for Piece type({piece_type}).')

    @classmethod
    def _get_possibilities_for_knight(cls, moviments, piece, board):
        possibilities = []
        for moviment in moviments:
            position = cls._extract_position(moviment)
            if position == '':
                continue
            if board[position] == 0:
                possibilities.append(position)
            elif board[position] != piece.color:
                possibilities.append(position)

        return possibilities

    @classmethod
    def _extract_position(cls, moviment):
        return list(moviment.values())[0]

    @classmethod
    def analize_possibily(cls, piece, location, board):
        possibilities = []
        positions = board.positions
        piece_type = piece.type
        if piece_type == 'KNIGHT':
            moviments = cls._get_moviments(location, piece_type, board.configuration)
            possibilities = cls._get_possibilities(moviments, piece, positions)
        return possibilities


class Log(Service):
    _domain = 'app.domain.chessGame'

    @classmethod
    def create(cls):
        return cls()

    @classmethod
    def create_log(cls, payload):
        try:
            mod = import_module(cls._domain)
            return mod.Log.create({
                'data': payload
            })
        except Exception as ex:
            print(ex)
    #
    # @classmethod
    # def create_piece(cls, payload):
    #     return cls.domain.Piece.create({
    #         'name': payload['name'],
    #         'color': payload['color'],
    #         'type': payload['type'],
    #     })
    #
    # @classmethod
    # def get_pieces(cls):
    #     return cls.domain.Piece.get_pieces()
    #
    # @classmethod
    # def get_piece_by_id(cls, piece_id):
    #     return cls.domain.Piece.get_by_id(piece_id)
    #
    # @classmethod
    # def update_one_piece(cls, piece_id, payload):
    #     piece = cls.domain.Piece.get_by_id(piece_id)
    #     piece.update_with_payload(payload)
    #     return piece
    #
    # @classmethod
    # def get_boards(cls):
    #     return cls.domain.Board.get_boards()
    #
    # @classmethod
    # def get_board_by_id(cls, board_id):
    #     return cls.domain.Board.get_by_id(board_id)
    #
    # @classmethod
    # def update_one_board(cls, board_id,payload):
    #     board = cls.domain.Board.get_by_id(board_id)
    #     board.update_with_payload(payload)
    #     return board
