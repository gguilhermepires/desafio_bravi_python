# -*- coding: utf-8 -*-

"""
This module define all the api endpoints
"""

from flask_restful import Api


def create_api(app):
    """
    Used when creating a Flask App to register the REST API and its resources
    """
    from app import resources
    api = Api(app)

    api.add_resource(resources.HealthcheckResource, '/api/v1/healthcheck')


    api.add_resource(
        resources.ChessBoardResource,
        '/api/v1/chess/boards',
        '/api/v1/chess/boards/<int:board_id>'
    )


    api.add_resource(
        resources.PieceResource,
        '/api/v1/chess/pieces',
        '/api/v1/chess/pieces/<int:piece_id>'
    )

    api.add_resource(
        resources.ChessBoardPossibilitiesResource,
        '/api/v1/chess/boards/<int:board_id>/possibilities'
    )

