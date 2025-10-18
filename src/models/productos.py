from sqlalchemy import Column, Integer, String, Float, ForeignKey
from src.models import session, Base
from src.models.categorias import Categorias 


class Productos(Base):
    __tablename__ = 'productos'
    id = Column(Integer, primary_key=True)
    descripcion = Column(String(300), unique=True, nullable=False)
    valor_unitario = Column(Float(10,8))
    unidad_medida = Column(String(3), nullable=False)
    cantida_stock = Column(Integer)
    categoria = Column(Integer, ForeignKey('categorias.id'), nullable=False)

    def __init__(self, descripcion, valor_unitario, unidad_medida, cantida_stock, categoria):
        self.descripcion = descripcion
        self.valor_unitario = valor_unitario
        self.unidad_medida = unidad_medida
        self.cantida_stock = cantida_stock
        self.categoria = categoria

    def traer_productos():
        productos =  session.query(Productos).all()
        return productos
    
    def agregar_producto(producto):
        producto = session.add(producto)
        session.commit()
        return producto
    
    def eliminar_producto(id):
        producto = session.query(Productos).get(id)        
        session.delete(producto)
        session.commit()
        return producto
    
    def producto_por_id(producto_id):
         return session.query(Productos).get(producto_id)

    