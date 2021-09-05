from app.domain import services
from app import repositories, domain


class Piece(domain.Entity):
    repository = repositories.Piece

    @property
    def id(self):
        return self.db_instance.id

    @property
    def name(self):
        return self.db_instance.name

    @property
    def color(self):
        return self.db_instance.color

    @property
    def type(self):
        return self.db_instance.type

    @classmethod
    def create(cls, payload):
        piece = cls.create_new_with_prepare(payload)
        piece.save()
        return piece

    @classmethod
    def get_by_id(cls, piece_id):
        return cls.create_with_instance(repositories.Piece.get(piece_id))

    @classmethod
    def get_pieces(cls):
        pieces_db = repositories.Piece.list_all()
        pieces = []
        for piece_db in pieces_db:
            pieces.append(cls.create_with_instance(piece_db).as_dict())
        return pieces

    @classmethod
    def get_by_id(cls, piece_id):
        return cls.create_with_instance(repositories.Piece.get(piece_id))

    def update_with_payload(self, payload):
        self.db_instance.name = payload['name']
        self.db_instance.color = payload['color']
        self.db_instance.type = payload['type']
        self.db_instance.rules = payload['rules']
        self.save()

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'type': self.type
        }


class Board(domain.Entity):
    repository = repositories.ChessBoard

    def __init__(self, db_instance):
        super(Board, self).__init__(db_instance)

    @property
    def id(self):
        return self.db_instance.id

    @property
    def name(self):
        return self.db_instance.name

    @property
    def positions(self):
        return self.db_instance.positions

    @classmethod
    def create(cls, payload):
        board = cls.create_new_with_prepare(payload)
        board.save()
        return board

    @classmethod
    def get_by_id(cls, board_id):
        return cls.create_with_instance(repositories.ChessBoard.get(board_id))

    def update_with_payload(self, payload):
        self.db_instance.name = payload['name']
        self.db_instance.positions = payload['positions']
        self.save()

    @classmethod
    def get_boards(cls):
        boards_db = repositories.ChessBoard.list_all()
        boards = []
        for board_db in boards_db:
            boards.append(cls.create_with_instance(board_db).as_dict())
        return boards

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'positions': self.positions
        }


class Chess(object):

    @classmethod
    def create(cls):
        return cls()

    def create_chessboard(self, payload):
        if payload['positions'] == '':
            board = {}
            length_row = 9
            length_col = 9
            for i in range(1, length_row):
                for j in range(1, length_col):
                    letter = services.Match.get_letter(j)
                    board[f"{i}{letter}"] = 0
            payload['positions'] = board

        return Board.create({
            'name': payload['name'],
            'positions': payload.get('positions', {}),
        })

    def create_piece(self, payload):
        return Piece.create({
            'name': payload['name'],
            'color': payload['color'],
            'type': payload['type'],
        })

    def get_pieces(self):
        return Piece.get_pieces()

    def get_one_piece(self, piece_id):
        return Piece.get_by_id(piece_id)

    def update_one_piece(self, piece_id, payload):
        piece = Piece.get_by_id(piece_id)
        piece.update_with_payload(payload)
        return piece

    def get_one_board(self, board_id):
        return Board.get_by_id(board_id)

    def get_boards(self):
        return Board.get_boards()

    def update_board(self, board_id, payload):
        board = Board.get_by_id(board_id)
        board.update_with_payload(payload)
        return board

    def get_board_possibility(self, board_id, payload):
        board = Board.get_by_id(board_id)
        piece = Piece.get_by_id(payload['piece_id'])
        location = payload['location']
        result = {}

        possibilities = services.Match.analize_possibily(piece, location, board.positions)
        for location_turn02 in possibilities:
            possibility = services.Match.analize_possibily(piece, location_turn02, board.positions)
            result[location_turn02] = possibility
        return result





