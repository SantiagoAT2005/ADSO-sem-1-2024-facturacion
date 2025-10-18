from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from src.models import session, Base
from src.models.clientes import Clientes
from src.models.usuarios import Usuarios
from src.models.productos import Productos
from decimal import Decimal


class Facturas(Base):
    __tablename__ = 'facturas'
    
    id = Column(Integer, primary_key=True)
    numero_factura = Column(String(50), unique=True, nullable=False)
    fecha = Column(DateTime, default=datetime.now, nullable=False)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    subtotal = Column(Float(10, 2), nullable=False, default=0.0)
    iva = Column(Float(10, 2), nullable=False, default=0.0)
    total = Column(Float(10, 2), nullable=False, default=0.0)
    estado = Column(String(20), nullable=False, default='activa')  # activa, anulada, pagada
    observaciones = Column(Text, nullable=True)
    
    # Relaciones
    cliente = relationship("Clientes", foreign_keys=[cliente_id])
    usuario = relationship("Usuarios", foreign_keys=[usuario_id])
    detalles = relationship("DetalleFactura", back_populates="factura", cascade="all, delete-orphan")

    def __init__(self, numero_factura, cliente_id, usuario_id, subtotal=0.0, iva=0.0, total=0.0, estado='activa', observaciones=None):
        self.numero_factura = numero_factura
        self.cliente_id = cliente_id
        self.usuario_id = usuario_id
        self.subtotal = subtotal
        self.iva = iva
        self.total = total
        self.estado = estado
        self.observaciones = observaciones

    @staticmethod
    def traer_facturas():
        facturas = session.query(Facturas).all()
        return facturas
    
    @staticmethod
    def agregar_factura(factura):
        session.add(factura)
        session.commit()
        return factura
    
    @staticmethod
    def eliminar_factura(id):
        factura = session.query(Facturas).get(id)
        if factura:
            session.delete(factura)
            session.commit()
        return factura
    
    @staticmethod
    def factura_por_id(factura_id):
        return session.query(Facturas).get(factura_id)
    
    @staticmethod
    def facturas_por_cliente(cliente_id):
        return session.query(Facturas).filter(Facturas.cliente_id == cliente_id).all()
    
    @staticmethod
    def facturas_por_usuario(usuario_id):
        return session.query(Facturas).filter(Facturas.usuario_id == usuario_id).all()
    
    @staticmethod
    def generar_numero_factura():
        """Genera un número de factura único"""
        ultima_factura = session.query(Facturas).order_by(Facturas.id.desc()).first()
        if ultima_factura:
            ultimo_numero = int(ultima_factura.numero_factura.split('-')[1])
            nuevo_numero = ultimo_numero + 1
        else:
            nuevo_numero = 1
        return f"FAC-{nuevo_numero:06d}"

    def calcular_totales(self):
        """Calcula los totales de la factura basado en sus detalles"""
        self.subtotal = sum(detalle.subtotal for detalle in self.detalles)
        self.iva = self.subtotal * Decimal('0.19')
        self.total = self.subtotal + self.iva
        session.commit()


class DetalleFactura(Base):
    __tablename__ = 'detalle_factura'
    
    id = Column(Integer, primary_key=True)
    factura_id = Column(Integer, ForeignKey('facturas.id'), nullable=False)
    producto_id = Column(Integer, ForeignKey('productos.id'), nullable=False)
    cantidad = Column(Float(10, 2), nullable=False)
    valor_unitario = Column(Float(10, 2), nullable=False)
    subtotal = Column(Float(10, 2), nullable=False)
    
    # Relaciones
    factura = relationship("Facturas", back_populates="detalles")
    producto = relationship("Productos", foreign_keys=[producto_id])

    def __init__(self, factura_id, producto_id, cantidad, valor_unitario):
        self.factura_id = factura_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.valor_unitario = valor_unitario
        self.subtotal = float(cantidad) * float(valor_unitario)

    @staticmethod
    def agregar_detalle(detalle):
        session.add(detalle)
        session.commit()
        return detalle
    
    @staticmethod
    def eliminar_detalle(id):
        detalle = session.query(DetalleFactura).get(id)
        if detalle:
            session.delete(detalle)
            session.commit()
        return detalle
    
    @staticmethod
    def detalles_por_factura(factura_id):
        return session.query(DetalleFactura).filter(DetalleFactura.factura_id == factura_id).all()