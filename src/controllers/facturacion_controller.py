from src.app import app
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_controller import FlaskController
from src.models.facturacion import Facturas, DetalleFactura
from src.models.clientes import Clientes
from src.models.usuarios import Usuarios
from src.models.productos import Productos
from src.models import session, Base
from datetime import datetime
from decimal import Decimal


class FacturasController(FlaskController):
    
    @app.route('/crear_factura', methods=['POST', 'GET'])
    def crear_factura():
        if request.method == 'POST':
            cliente_id = request.form.get('cliente_id')
            usuario_id = request.form.get('usuario_id')
            observaciones = request.form.get('observaciones')
            
            # Generar número de factura automáticamente
            numero_factura = Facturas.generar_numero_factura()
            
            # Crear la factura
            factura = Facturas(
                numero_factura=numero_factura,
                cliente_id=cliente_id,
                usuario_id=usuario_id,
                observaciones=observaciones
            )
            
            Facturas.agregar_factura(factura)
            flash('Factura creada exitosamente', 'success')
            return redirect(url_for('agregar_detalles_factura', factura_id=factura.id))
        
        # Cargar datos para el formulario
        clientes = Clientes.obtener_clientes()
        usuarios = session.query(Usuarios).all()
        
        return render_template('formulario_crear_factura.html', 
                             titulo_pagina='Crear Factura',
                             clientes=clientes,
                             usuarios=usuarios)

    @app.route('/agregar_detalles_factura/<int:factura_id>', methods=['GET', 'POST'])
    def agregar_detalles_factura(factura_id):
        factura = Facturas.factura_por_id(factura_id)
        
        if not factura:
            flash('Factura no encontrada', 'error')
            return redirect(url_for('lista_facturas'))
        
        if request.method == 'POST':
            producto_id = request.form.get('producto_id')
            cantidad = float(request.form.get('cantidad'))
            
            # Obtener el producto para el valor unitario
            producto = Productos.producto_por_id(producto_id)
            
            if not producto:
                flash('Producto no encontrado', 'error')
                return redirect(url_for('agregar_detalles_factura', factura_id=factura_id))
            
            # Verificar stock disponible
            if cantidad > producto.cantida_stock:
                flash('Cantidad solicitada supera el stock disponible', 'error')
                return redirect(url_for('agregar_detalles_factura', factura_id=factura_id))
            
            # Crear detalle de factura
            detalle = DetalleFactura(
                factura_id=factura_id,
                producto_id=producto_id,
                cantidad=cantidad,
                valor_unitario=producto.valor_unitario
            )
            
            DetalleFactura.agregar_detalle(detalle)
            
            # Actualizar stock del producto
            producto.cantida_stock -= cantidad
            session.commit()
            
            # Recalcular totales de la factura
            factura.calcular_totales()
            
            flash('Producto agregado a la factura', 'success')
            return redirect(url_for('agregar_detalles_factura', factura_id=factura_id))
        
        # Cargar datos para el formulario
        productos = Productos.traer_productos()
        detalles = DetalleFactura.detalles_por_factura(factura_id)
        
        return render_template('agregar_detalles_factura.html',
                             titulo_pagina='Agregar Productos a Factura',
                             factura=factura,
                             productos=productos,
                             detalles=detalles)

    @app.route('/ver_facturas')
    def ver_facturas():
        facturas = Facturas.traer_facturas()
        return render_template('tabla_facturas.html', 
                             titulo_pagina='Lista de Facturas',
                             facturas=facturas)

    @app.route('/ver_factura/<int:id>')
    def ver_factura(id):
        factura = Facturas.factura_por_id(id)
        
        if not factura:
            flash('Factura no encontrada', 'error')
            return redirect(url_for('lista_facturas'))
        
        detalles = DetalleFactura.detalles_por_factura(id)
        
        return render_template('ver_factura.html',
                             titulo_pagina='Detalle de Factura',
                             factura=factura,
                             detalles=detalles)

    @app.route('/eliminar_factura/<int:id>')
    def eliminar_factura(id):
        factura = Facturas.factura_por_id(id)
        
        if not factura:
            flash('Factura no encontrada', 'error')
            return redirect(url_for('lista_facturas'))
        
        # Devolver el stock de los productos antes de eliminar
        for detalle in factura.detalles:
            producto = Productos.producto_por_id(detalle.producto_id)
            if producto:
                producto.cantida_stock += detalle.cantidad
        
        session.commit()
        
        Facturas.eliminar_factura(id)
        flash('Factura eliminada exitosamente', 'success')
        return redirect(url_for('lista_facturas'))

    @app.route('/anular_factura/<int:id>')
    def anular_factura(id):
        factura = Facturas.factura_por_id(id)
        
        if not factura:
            flash('Factura no encontrada', 'error')
            return redirect(url_for('lista_facturas'))
        
        if factura.estado == 'anulada':
            flash('La factura ya está anulada', 'warning')
            return redirect(url_for('lista_facturas'))
        
        # Devolver el stock de los productos
        for detalle in factura.detalles:
            producto = Productos.producto_por_id(detalle.producto_id)
            if producto:
                producto.cantida_stock += detalle.cantidad
        
        factura.estado = 'anulada'
        session.commit()
        
        flash('Factura anulada exitosamente', 'success')
        return redirect(url_for('lista_facturas'))

    @app.route('/eliminar_detalle_factura/<int:detalle_id>/<int:factura_id>')
    def eliminar_detalle_factura(detalle_id, factura_id):
        detalle = session.query(DetalleFactura).get(detalle_id)
        
        if not detalle:
            flash('Detalle no encontrado', 'error')
            return redirect(url_for('agregar_detalles_factura', factura_id=factura_id))
        
        # Devolver el stock del producto
        producto = Productos.producto_por_id(detalle.producto_id)
        if producto:
            producto.cantida_stock += detalle.cantidad
        
        DetalleFactura.eliminar_detalle(detalle_id)
        
        # Recalcular totales de la factura
        factura = Facturas.factura_por_id(factura_id)
        factura.calcular_totales()
        
        flash('Producto eliminado de la factura', 'success')
        return redirect(url_for('agregar_detalles_factura', factura_id=factura_id))

    @app.route('/finalizar_factura/<int:id>')
    def finalizar_factura(id):
        factura = Facturas.factura_por_id(id)
        
        if not factura:
            flash('Factura no encontrada', 'error')
            return redirect(url_for('lista_facturas'))
        
        if not factura.detalles:
            flash('No se puede finalizar una factura sin productos', 'error')
            return redirect(url_for('agregar_detalles_factura', factura_id=id))
        
        factura.estado = 'pagada'
        session.commit()
        
        flash('Factura finalizada exitosamente', 'success')
        return redirect(url_for('ver_factura', id=id))

    @app.route('/facturas_por_cliente/<int:cliente_id>')
    def facturas_por_cliente(cliente_id):
        facturas = Facturas.facturas_por_cliente(cliente_id)
        cliente = Clientes.obtener_cliente_por_id(cliente_id)
        
        return render_template('lista_facturas.html',
                             titulo_pagina=f'Facturas del Cliente',
                             facturas=facturas,
                             cliente=cliente)