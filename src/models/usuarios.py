from sqlalchemy import Column, Integer, String
from src.models import session, Base

class Usuarios(Base):
    __tablename__ = "usuarios"    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    email = Column(String(500), unique=True, nullable=False)
    contraseña = Column(String(30), nullable=False)
    rol = Column(String(20), nullable=False)


    def __init__(self, 
                 nombre, 
                 email, 
                 contraseña, 
                 rol):
        self.nombre = nombre
        self.email = email
        self.contraseña = contraseña
        self.rol = rol
        
    
    def obtener_usuarios():
        clientes = session.query(Usuarios).all()
        return clientes 
