from sqlalchemy import Column, Date, Integer, String, Float, ForeignKey, Numeric
from src.models import Base, session

class Usuarios(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    nombre_usuario = Column(String(100), nullable=False)
    id_usuario = Column(String(100), unique=True, nullable=False)
    identificacion_usuario = Column(String(100), nullable=False)
    rol_perfil = Column(String(20), nullable=False)
    email_usuario = Column(String(100), unique=True, nullable=False)

    def __init__(self,nombre_usuario,id_usuario,identificacion_usuario,rol_perfil,email_usuario):
        self.nombre_usuario = nombre_usuario
        self.id_usuario = id_usuario
        self.identificacion_usuario = identificacion_usuario
        self.rol_perfil = rol_perfil
        self.email_usuario = email_usuario  

    def crear_usuario(usuario):
        usuario = session.add(usuario)
        session.commit()
        return usuario  
    
    def traer_usuarios():
        usuarios = session.query(Usuarios).all()
        return usuarios
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def obtener_usuario_por_id_usuario(id_usuario):
        usuario = session.query(Usuarios).filter(Usuarios.id_usuario == id_usuario).first()
        print(usuario)
        return usuario.as_dict()
    
    @staticmethod
    def traer_usuario_por_id(id):
        return session.query(Usuarios).filter_by(id=id).first()
    
    @staticmethod
    def crear_usuario(usuario):
        session.add(usuario)
        session.commit()
        return usuario
    
    @staticmethod
    def actualizar_usuario(usuario):
        session.commit()  
        return usuario
    
    @staticmethod
    def eliminar_usuario(id):
        usuario = session.query(Usuarios).filter_by(id=id).first()
        if usuario:
            session.delete(usuario)
            session.commit()
            return True
        return False

    