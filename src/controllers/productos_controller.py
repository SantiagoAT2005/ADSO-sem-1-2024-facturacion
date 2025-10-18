from src.app import app
from flask import render_template, request, redirect, url_for
from flask_controller import FlaskController
from src.models.productos import Productos
from src.models.categorias import Categorias
from src.models import session, Base

class ProductosController(FlaskController):
    @app.route('/crear_producto', methods=['POST','GET'])
    def crear_producto():    
        if request.method == 'POST':
            descripcion = request.form.get('descripcion')                
            valor_unitario = request.form.get('valor_unitario')    
            unidad_medida = request.form.get('unidad_medida')    
            cantida_stock = request.form.get('cantida_stock')    
            categoria = request.form.get('categoria')    
            producto = Productos(descripcion,valor_unitario,unidad_medida,cantida_stock,categoria)
            Productos.agregar_producto(producto)
            return redirect(url_for('lista_productos'))
        categorias = Categorias.obtener_categorias()
        return render_template('formulario_crear_producto.html', titulo_pagina = 'Crear Producto', categorias=categorias)

    @app.route('/lista_productos')
    def lista_productos():
        productos = session.query(Productos).all()
        return render_template('lista_productos.html', productos=productos)
    
    @app.route('/eliminar_producto/<id>')
    def eliminar_producto(id):
        Productos.eliminar_producto(id)
        productos = Productos.obtener_productos()
        return render_template('tabla_productos.html', titulo_pagina = 'Ver Productos', productos=productos)

    @app.route('/editar_producto/<int:id>', methods=['GET', 'POST'])
    def editar_producto(id):
        producto = session.query(Productos).get(id)
        
        if request.method == 'POST':
           
            
            producto.descripcion = request.form.get('descripcion')
            producto.valor_unitario = request.form.get('valor_unitario')
            producto.unidad_medida = request.form.get('unidad_medida')
            producto.cantida_stock = request.form.get('cantida_stock')
            
            producto.categoria = request.form.get('categoria')
            
           
            session.commit()
            
            return redirect(url_for('lista_productos'))
        
        return render_template('editar_producto.html', 
                            titulo='Editar Producto', 
                            producto=producto)
        

