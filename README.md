# Desafio

API para analisar jogos de xadrez.

# Postman

Coleção com exemplos de consumo da api (teste.postman_collection.json)


# Install database

    sudo su postgres
    psql
    CREATE ROLE teste SUPERUSER LOGIN PASSWORD 'teste';
    CREATE DATABASE teste;
    ALTER DATABASE teste OWNER TO teste;
    /connect teste;

# Update database
    
    atualizar o banco
    load-env
    python manage.py db upgrade

# Docker

docker-compose up

# Objetivos

1) registration of chess pieces (type/name and color)
 
   Send post to endpoint /api/v1/chess/pieces
    {
        "name":"piece teste",
        "color": "WHITE",
        "type":  "PAWN"
    }
   
    return 
   {
        "id": 10,
        "name": "piece teste",
        "color": "WHITE",
        "type": "KNIGHT"
    }
   
2)given a location on a coordinate chosen by the user and the piece id (if it is a knight, find out all possible locations where the knight can move in 2 turns.)
   
    send get to endpoint /api/v1/chess/boards/:boardId/possibilities?pieceId=10&location=5d

    return
    {
        "7c": [
            "8a",
            "8e",
            "6a",
            "6e",
            "5b",
            "5d"
        ],
        "7e": [
            "8c",
            "8g",
            "6c",
            "6g",
            "5d",
            "5f"
        ],
        "6b": [
            "8a",
            "8c",
            "7d",
            "5d",
            "4a",
            "4c"
        ],
        "6f": [
            "8e",
            "8g",
            "7d",
            "7h",
            "5d",
            "5h",
            "4e",
            "4g"
        ],
        "4b": [
            "6a",
            "6c",
            "5d",
            "3d",
            "2a",
            "2c"
        ],
        "4f": [
            "6e",
            "6g",
            "5d",
            "5h",
            "3d",
            "3h",
            "2e",
            "2g"
        ],
        "3c": [
            "5b",
            "5d",
            "4a",
            "4e",
            "2a",
            "2e",
            "1b",
            "1d"
        ],
        "3e": [
            "5d",
            "5f",
            "4c",
            "4g",
            "2c",
            "2g",
            "1d",
            "1f"
        ]
    }

# Endpoits úteis

Criar tabuleiro

POST - /api/v1/chess/boards
{
    "name":"board teste 2",
    "positions": "",
    "configuration": {
        "col_length":9,
        "row_length":9
    }
}

