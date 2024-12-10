from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)


# Function that initializes the db and creates the tables
def db_init(app):
    db.init_app(app)

    # Creates the logs tables if the db doesnt already exist
    with app.app_context():
        db.create_all()

        from db import db



class Img(Base):
    __tablename__ = "img"
    id: Mapped[int] = mapped_column(primary_key=True)
    img: Mapped[int] = mapped_column(db.LargeBinary, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(db.Text, nullable=False)
    mimetype: Mapped[str] = mapped_column(db.Text, nullable=False)