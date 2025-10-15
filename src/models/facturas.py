from sqlalchemy import Column, Date, Integer, String, Float, ForeignKey, Numeric
from src.models import Base, session
from src.models.categorias import Categorias
from sqlalchemy.orm import relationship


class Facturas(Base):
    __tablename__ = "Facturas"
    id = Column(Integer, primary_key=True)
    codigo = Column(String(20), unique=True, nullable=False)
    descripcion = Column(String(50), nullable=False)
    precio_unitario = Column(String(300), nullable=False)
    unidad_medida = Column(String(25), nullable=False)
    categoria = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    forma_pago_factura = Column(String(20), nullable=False)
    identificacion_cliente = Column(String(20), unique=True, nullable=False)
    nombre_cliente = Column(String(300), nullable=False)
    fecha_cliente = Column(Date, nullable=False)
    email_cliente = Column(String(100), unique=True, nullable=False)
    id_usuario = Column(String(100), unique=True, nullable=False)
    nombre_usuario = Column(String(100), nullable=False)
    identificacion_usuario = Column(String(100), nullable=False)
    rol_perfil = Column(String(20), nullable=False)
    email_usuario = Column(String(100), unique=True, nullable=False)

    categoria_rel = relationship("Categorias", backref="facturas")



    def __init__(self, codigo, descripcion, precio_unitario, unidad_medida, categoria, forma_pago_factura, identificacion_cliente, nombre_cliente,
                 fecha_cliente, email_cliente, id_usuario, nombre_usuario, identificacion_usuario, rol_perfil, email_usuario):
        self.codigo = codigo
        self.descripcion = descripcion
        self.precio_unitario = precio_unitario
        self.unidad_medida = unidad_medida
        self.categoria = categoria
        self.forma_pago_factura = forma_pago_factura
        self.identificacion_cliente = identificacion_cliente
        self.nombre_cliente = nombre_cliente    
        self.fecha_cliente = fecha_cliente
        self.email_cliente = email_cliente
        self.id_usuario = id_usuario        
        self.nombre_usuario = nombre_usuario
        self.identificacion_usuario = identificacion_usuario
        self.rol_perfil = rol_perfil
        self.email_usuario = email_usuario


    def crear_factura(factura):
        factura = session.add(factura)
        session.commit()
        return factura    
    
    def traer_facturas():  
        facturas = session.query(Facturas).all()
        return facturas
    
    @staticmethod
    def traer_factura_por_id(id):
        return session.query(Facturas).filter_by(id=id).first()
    
    @staticmethod
    def crear_factura(factura):
        session.add(factura)
        session.commit()
        return factura
    
    @staticmethod
    def actualizar_factura(factura):
        session.commit()  
        return factura
    
    @staticmethod
    def eliminar_factura(id):
        factura = session.query(Facturas).filter_by(id=id).first()
        if factura:
            session.delete(factura)
            session.commit()
            return True
        return False