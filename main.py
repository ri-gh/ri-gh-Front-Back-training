from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from starlette import status
from sqlmodel import Session, select
from models import UserAccount, engine
import re

load_dotenv()

app = FastAPI()

origins = [os.environ['FRONTEND_URL1'], os.environ['FRONTEND_URL2']]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/message")
async def get_message():
    return {"message": "Bonjour depuis le Backend FastAPI en Python!"}


# @app.post("/post/infos")
# async def post_display_infos(data: dict):
#     """
#     Args:
#         data (dict): données reçues du front

#     Returns:
#         toutes les valeurs du dictionnaire et ses clés
#     """
#     for key in data:
#         print(key + ': ' + data[key])
#     return data

@app.post("/create_account")
async def create_user_account(data: dict):
    for key in data:
        print(key + ': ' + data[key])

    # vérification du format de l'email
    if not re.match(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$", data['email']):
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f'L\'adresse e-mail "{data['email']}" n\'est pas au bon format, merci de modifier',
        )
    # vérification si l'username n'existe pas déjà en BDD
    with Session(engine) as session:
        statement = select(UserAccount)    # equivalent au SELECT de SQL
        results = session.exec(statement)
        users = results.all()

        # verifie si le user existe deja dans la base de donnees
        for user in users:
            if data['username'] in user.username:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f'Le nom d\'utilisateur {data['username']} existe déjà, merci de modifier',
                )
        # vérification si email existant
            elif data['email'] in user.email:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f'L\'email "{data["email"]}" a déjà un compte utilisateur'
                )

        new_user = UserAccount(username=data['username'].strip(), email=data['email'], password=data['password'])
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

    return data
