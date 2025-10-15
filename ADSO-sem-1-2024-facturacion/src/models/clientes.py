from sqlalchemy import Column, Date, Integer, String, Float, ForeignKey, Numeric
from src.models import Base, session
import datetime

class Clientes(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True)
    nombre_cliente = Column(String(300), nullable=False)
    fecha_cliente = Column(Date, nullable=False)
    tipo_identificacion = Column(String(15), nullable=False)
    identificacion_cliente = Column(String(20), unique=True, nullable=False)
    email_cliente = Column(String(100), unique=True, nullable=False)

    def __init__(self, nombre_cliente, fecha_nacimiento, tipo_identificacion, identificacion_cliente, email_cliente):
        self.nombre_cliente = nombre_cliente
        self.fecha_cliente = fecha_nacimiento
        self.tipo_identificacion = tipo_identificacion
        self.identificacion_cliente = identificacion_cliente
        self.email_cliente = email_cliente

    def crear_cliente(cliente):
        cliente = session.add(cliente)
        session.commit()
        return cliente    
    
    def traer_clientes():  
        clientes = session.query(Clientes).all()
        return clientes
    
    def as_dict(self):
        result = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)
            if isinstance(value, (datetime.date, datetime.datetime)):
                result[c.name] = value.strftime("%Y-%m-%d")
            else:
                result[c.name] = value
        return result
    
    def obtener_cliente_por_identificacion_cliente(identificacion_cliente):
        cliente = session.query(Clientes).filter(Clientes.identificacion_cliente == identificacion_cliente).first()
        print(cliente)
        return cliente.as_dict()
    
    @staticmethod
    def traer_cliente_por_id(id):
        return session.query(Clientes).filter_by(id=id).first()
    
    @staticmethod
    def crear_cliente(cliente):
        session.add(cliente)
        session.commit()
        return cliente
    
    @staticmethod
    def actualizar_cliente(cliente):
        session.commit()  
        return cliente
    
    @staticmethod
    def eliminar_cliente(id):
        cliente = session.query(Clientes).filter_by(id=id).first()
        if cliente:
            session.delete(cliente)
            session.commit()
            return True
        return False
    
    def obtener_cliente_por_documento_identidad(documento_identidad):
        cliente = session.query(Clientes).filter(Clientes.documento_identidad == documento_identidad).first()
        print(cliente)
        return cliente.as_dict()


