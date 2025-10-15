from sqlalchemy import Column, Date, Integer, String, Float, ForeignKey, Numeric
from src.models import Base, session
from src.models.categorias import Categorias   
from sqlalchemy.orm import relationship 

class Productos(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True)
    codigo = Column(String(9), unique=True, nullable=False) 
    descripcion = Column(String(300), unique=True, nullable=False) 
    cantidad_inventario = Column(Numeric(10,2))
    precio_unitario = Column(Numeric(10,2))
    unidad_medida = Column(String(3), nullable=False)
    categoria = Column(Integer, ForeignKey("categorias.id"), nullable=False)

    categoria_rel = relationship("Categorias", backref="productos")

    def __init__(self,codigo,descripcion,cantidad_inventario,precio_unitario,unidad_medida,categoria):
        self.codigo = codigo
        self.descripcion = descripcion
        self.cantidad_inventario = cantidad_inventario
        self.precio_unitario = precio_unitario
        self.unidad_medida = unidad_medida
        self.categoria = categoria

    def crear_producto(producto):
        session.add(producto)
        session.commit()
        return producto
    
    def traer_productos():  
        productos = session.query(Productos).all()
        return productos
    
    def traer_producto_por_descripcion(descripcion):
        producto = session.query(Productos).filter(Productos.descripcion  == descripcion).first()  
        return producto
    
    def traer_producto_por_codigo(codigo):
        producto = session.query(Productos).filter(Productos.codigo == codigo).first()
        return producto
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def obtener_producto_por_codigo(codigo):
        producto = session.query(Productos).filter(Productos.codigo == codigo).first()
        print(producto)
        return producto.as_dict()
    
    @staticmethod
    def traer_producto_por_id(id):
        return session.query(Productos).filter_by(id=id).first()
    
    @staticmethod
    def crear_producto(producto):
        session.add(producto)
        session.commit()
        return producto
    
    @staticmethod
    def actualizar_producto(producto):
        session.commit()  
        return producto
    
    @staticmethod
    def eliminar_producto(id):
        producto = session.query(Productos).filter_by(id=id).first()
        if producto:
            session.delete(producto)
            session.commit()
            return True
        return False
