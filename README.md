# Desafio

API para analisar jogos de xadrez

# install database

    sudo su postgres
    psql
    CREATE ROLE teste SUPERUSER LOGIN PASSWORD 'teste';
    CREATE DATABASE teste;
    ALTER DATABASE teste OWNER TO teste;
    /connect teste;

# update database
    criar uma migrate
    python manage.py db makemigrations
    
    atualizar o banco
    load-env
    python manage.py db upgrade

# Docker

Para realizar o build 
    $ sudo docker build -t teste .

# testes
Os testes da API se encontram na pasta tests


# objetivos
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


