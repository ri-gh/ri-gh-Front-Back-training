from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session, select


class UserAccount(SQLModel, table=True):
    __tablename__ = 'UserAccount'
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str


# on crée la Table dans la BDD 'andv'
engine = create_engine("postgresql://postgres:ANDV-93$rg@localhost:5432/andv")
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
