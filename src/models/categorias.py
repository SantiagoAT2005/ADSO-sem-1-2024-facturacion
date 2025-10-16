from sqlalchemy import Column, Date, Integer, String, Float, ForeignKey, Numeric
from src.models import Base, session


class Categorias(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True)
    nombre_categoria = Column(String(300), unique=True, nullable=False)

    def __init__(self,nombre_categoria):
        self.nombre_categoria = nombre_categoria

    def traer_categoria():   
        categorias = session.query(Categorias).all()
        return categorias 
    