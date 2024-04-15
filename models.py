from typing import Optional
import os
from dotenv import load_dotenv
from sqlmodel import Field, SQLModel, create_engine, Session, select

load_dotenv()


class UserAccount(SQLModel, table=True):
    __tablename__ = 'UserAccount'
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str


# on crée la Table dans la BDD 'andv'
engine = create_engine(os.environ['DATABASE_URL'], pool_pre_ping=True)
SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    def delete_users():
        """automatic deletion"""
        with Session(engine) as session:
            statement = select(UserAccount).where(UserAccount.id != 'toto')
            results = session.exec(statement)
            users = results.all()

            for user in users:
                session.delete(user)
                session.commit()
    delete_users()
