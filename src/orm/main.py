from sqlalchemy import String, Integer, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from src.common.helpers import print_menu

engine = create_engine("mysql+pymysql://student:studentpwd@db:3306/boutikpro_ccf")


class Base(DeclarativeBase):
    pass


class Client(Base):
    __tablename__ = "client"
    id_client: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom: Mapped[str] = mapped_column(String(50))
    prenom: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100))


if __name__ == "__main__":
    print_menu("Mode SQLAlchemy ORM")
    print("Fichier à compléter : src/orm/main.py")
    print("Commande d'exécution : python -m src.orm.main")
    print()
    with Session(engine) as session:
        for client in session.query(Client).order_by(Client.id_client).all():
            print(client.id_client, client.nom, client.prenom, client.email)
    print("
Compléter ce fichier pour réaliser le CRUD demandé.")
