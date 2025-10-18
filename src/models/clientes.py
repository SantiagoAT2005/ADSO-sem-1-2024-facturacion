from sqlalchemy import Column, Integer, String
from src.models import session, Base

class Clientes(Base):
    __tablename__ = "clientes"    
    id = Column(Integer, primary_key=True)
    numero_identificacion = Column(String(30), unique=True, nullable=False)
    nombre_completo = Column(String(200), nullable=False)
    email = Column(String(500), unique=True, nullable=False)
    telefono = Column(String(30), nullable=False)
    direccion = Column(String(300), nullable=False)
    
    def __init__(self, 
                 numero_identificacion, 
                 nombre_completo, 
                 email, telefono, 
                 direccion):
        self.numero_identificacion = numero_identificacion
        self.nombre_completo = nombre_completo
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
    
    def obtener_clientes():
        clientes = session.query(Clientes).all()
        return clientes 
    
    def obtener_cliente_por_id(id):
        cliente = session.query(Clientes).get(id)
        return cliente.to_dict()
    
    def obtener_cliente_por_numero_identificacion(numero_identificacion):
        cliente = session.query(Clientes).filter(Clientes.numero_identificacion == numero_identificacion).first()
        print(cliente)
        return cliente.to_dict()
