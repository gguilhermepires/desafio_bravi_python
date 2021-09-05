# -*- coding: utf-8 -*-
import json
import unittest
from unittest import mock

from app import initialize


class TestCase(unittest.TestCase):
    mock = mock
    app = initialize.web_app
    client = initialize.web_app.test_client()

    url = None
    payload = {}

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.payload = {}
        self.params = {}
        self.headers = {
            'Content-Type': 'application/json',
        }

    @property
    def response_get(self):
        return self.client.get(self.url, data=json.dumps(self.payload), headers=self.headers, query_string=self.params)

    @property
    def response_post(self):
        return self.client.post(self.url, data=json.dumps(self.payload), headers=self.headers, query_string=self.params)

    @property
    def response_post_upload(self):
        return self.client.post(self.url, data=self.payload, headers={'Content-Type': 'multipart/form-data'})

    @property
    def response_put(self):
        return self.client.put(self.url, data=json.dumps(self.payload), headers=self.headers)

    @property
    def response_delete(self):
        return self.client.delete(self.url)

    def create_board(self):
        self.url = f'/api/v1/chess/boards'
        self.payload = {
            "name": "board teste 2",
            "positions": ""
        }
        return self.response_post

    def create_piece(self):
        self.url = f'/api/v1/chess/pieces'
        self.payload = {
            "name": "piece teste",
            "color": "WHITE",
            "type": "KNIGHT"
        }
        return self.response_post

    def test_create_board(self):
        response = self.create_board()
        self.assertEqual(response.status_code, 201)
        print(response.json)

    def test_create_piece(self):
        response = self.create_piece()
        self.assertEqual(response.status_code, 201)
        print(response.json)

    def test_analize(self):
        response = self.create_board()
        if response.status_code == 201:
            board_id = response.json['id']

        response = self.create_piece()
        if response.status_code == 201:
            piece_id = response.json['id']

        location = '5d'
        self.url = f'/api/v1/chess/boards/{board_id}/possibilities'
        self.params = {
            'piece_id': piece_id,
            'location': location,
        }
        response = self.response_get

        self.assertEqual(response.status_code, 200)
        print(response.json)