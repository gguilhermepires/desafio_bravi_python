# -*- coding: utf-8 -*-
import re
from functools import wraps
from flask import request, g, Response
from flask_restful import Resource
from app.domain.chessGame import Chess


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authenticated = getattr(g, 'authenticated', False)
        if not authenticated:
            return Response('{"result": "Not Authorized"}', 401, content_type='application/json')
        return f(*args, **kwargs)
    return decorated_function


def not_allowed(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return Response('{"result": "Method not allowed"}', 405, content_type='application/json')
    return decorated_function


class ResourceBase(Resource):
    def __init__(self):
        self.me = Chess.create()

    @property
    def integrator(self):
        integrator = getattr(g, 'laboratory', None)
        integrator['embassy_token'] = request.headers.get('EMBASSY-TOKEN', '')
        integrator['embassy_profile'] = request.headers.get('EMBASSY-PROFILE', '')
        return integrator

    @property
    def authenticated(self):
        return getattr(g, 'authenticated', None)

    @staticmethod
    def camel_to_snake(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    @staticmethod
    def snake_to_camel(name):
        result = []
        for index, part in enumerate(name.split('_')):
            if index == 0:
                result.append(part.lower())
            else:
                result.append(part.capitalize())
        return ''.join(result)

    def transform_key(self, data, method):
        if isinstance(data, dict):
            return {method(key): self.transform_key(value, method) for key, value in data.items()}
        if isinstance(data, list):
            for index, item in enumerate(data):
                if isinstance(item, dict):
                    data[index] = {method(key): self.transform_key(value, method) for key, value in item.items()}
        return data

    @property
    def payload(self):
        payload = {}
        if request.method != 'GET' and request.json:
            payload.update(self.transform_key(request.json, self.camel_to_snake))
        if request.form:
            payload.update(self.transform_key(request.form, self.camel_to_snake))
        if request.args:
            payload.update(self.transform_key(request.args, self.camel_to_snake))
        return payload

    @property
    def cookies(self):
        username = request.cookies.get('inceresUserName', None)
        token = request.cookies.get('inceresUserToken', 'null')
        profile_key = request.cookies.get('inceresProfileKey', 'null')
        return {'inceresUserName': username, 'inceresUserToken': token, 'inceresProfileKey': profile_key}

    def return_ok(self):
        return {"result": "OK"}, 200

    def return_not_authorized(self):
        return {"result": "Not Authorized"}, 401

    def return_not_found(self):
        return {"result": "Not Found"}, 404

    def return_not_allowed(self):
        return {"result": "Method Not Allowed"}, 405

    def return_bad_request(self, message):
        return {"result": "Bad Request", "message": message}, 400

    def response(self, data_dict, code=200):
        return self.transform_key(data_dict, self.snake_to_camel), code

    def response_with_error(self, data_dict, status_code=500, extra=None):
        if extra is None:
            extra = {}
        return self.response(data_dict), status_code


class HealthcheckResource(ResourceBase):
    def get(self):
        """
            .. iheader::

            .. iendpoint::
                '/api/blueprints/<int:blueprint_id>/assembly-lines/<int:assembly_line_id>/workstations', '/api/blueprints/<int:blueprint_id>/assembly-lines/<int:assembly_line_id>/workstations/<int:workstation_id>'

            .. ireturn_example::
                {
                    "result": "OK"
                }
        """
        return self.return_ok()


class ChessBoardResource(ResourceBase):

    def get(self, board_id=None):
        try:
            if board_id:
                return self.response(self.me.get_one_board(board_id).as_dict())
            boards = self.me.get_boards()
            return self.response(boards)
        except Exception as ex:
            return self.response_with_error({'exception': str(ex)})

    def post(self):
        try:
            board = self.me.create_chessboard(self.payload)
            return self.response(board.as_dict(), 201)
        except KeyError as ex:
            return self.return_bad_request(f'You must send all parameters. Parameter {ex} not found.')

        except Exception as ex:
            return self.response_with_error({'exception': str(ex)})

    def put(self, board_id):
        try:
            return self.response(self.me.update_board(board_id, self.payload).as_dict())
        except Exception as ex:
            return self.response_with_error({'exception': str(ex)})


class ChessBoardPossibilitiesResource(ResourceBase):

    def get(self, board_id=None):
        try:
            teste = self.me.get_board_possibility(board_id, self.payload)
            return self.response(teste)
        except Exception as ex:
            return self.response_with_error({'exception': str(ex)})


class PieceResource(ResourceBase):

    def get(self, piece_id=None):
        try:
            if piece_id:
                return self.response(self.me.get_one_piece(piece_id).as_dict())
            return self.response(self.me.get_pieces())
        except Exception as ex:
            return self.response_with_error({'exception': str(ex)})

    def post(self):
        try:
            return self.response(self.me.create_piece(self.payload).as_dict(), 201)
        except Exception as ex:
            return self.response_with_error({'exception': str(ex)})

    def put(self, piece_id):
        try:
            return self.response(self.me.update_one_piece(piece_id, self.payload).as_dict())
        except Exception as ex:
            return self.response_with_error({'exception': str(ex)})