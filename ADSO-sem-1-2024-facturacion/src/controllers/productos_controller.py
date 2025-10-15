from flask import redirect, render_template, request, url_for
from flask_controller import FlaskController
from src.models.productos import Productos
from src.models.categorias import Categorias
from src.app import app

class ProductosController(FlaskController):
    @app.route('/lista_productos')
    def lista_productos():
        productos = Productos.traer_productos()
        return render_template('lista_productos.html',titulo='Ver productos', productos = productos)

    @app.route('/formulario_producto', methods=['GET', 'POST'])
    def formulario_producto():
        categorias = Categorias.traer_categoria()
        if request.method == 'POST':
            codigo = request.form.get('codigo')
            descripcion = request.form.get('descripcion')
            cantidad_inventario = request.form.get('cantidad_inventario')
            precio_unitario = request.form.get('precio_unitario')
            unidad_medida = request.form.get('unidad_medida')
            categoria = request.form.get('categoria')
            
            producto_almacenar = Productos(codigo,descripcion,cantidad_inventario,precio_unitario,unidad_medida,categoria)
            producto_repetido = Productos.traer_producto_por_descripcion(descripcion)
            
            if producto_repetido:
                return render_template('formulario_producto.html'
                                    ,titulo='Crear un producto'
                                    ,errorProducto = "La descripción ya existe"
                                    ,categorias = categorias
                                    ,producto_almacenar = producto_almacenar)
            
            producto_repetido_codigo = Productos.traer_producto_por_codigo(codigo)

            if producto_repetido_codigo:
                return render_template('formulario_producto.html'
                ,titulo='Crear un producto'
                ,errorCodigo="El código ya existe"
                ,categorias=categorias
                ,producto_almacenar=producto_almacenar)
            
            try:
                Productos.crear_producto(producto_almacenar)
                return redirect(url_for('lista_productos'))
            except:            
                return render_template('formulario_producto.html',titulo='Error al registrar en la base de datos',categorias = categorias) 
                
           
        return render_template('formulario_producto.html',titulo='Crear un producto',categorias = categorias, producto_almacenar=None)
    
    @app.route('/consultar_producto_codigo/<codigo>')
    def consultar_producto_codigo(codigo):
        producto = Productos.obtener_producto_por_codigo(codigo)
        return producto

    @app.route('/editar_producto/<int:id>', methods=['GET', 'POST'])
    def editar_producto(id):
        producto = Productos.traer_producto_por_id(id)
        categorias = Categorias.traer_categoria()

        if request.method == 'POST':
            producto.codigo = request.form.get('codigo')
            producto.descripcion = request.form.get('descripcion')
            producto.cantidad_inventario = request.form.get('cantidad_inventario')
            producto.precio_unitario = request.form.get('precio_unitario')
            producto.unidad_medida = request.form.get('unidad_medida')
            producto.categoria = request.form.get('categoria')

            Productos.actualizar_producto(producto)
            return redirect(url_for('lista_productos'))

        return render_template('formulario_producto.html',
                            titulo='Editar producto',
                            producto_almacenar=producto,
                            categorias=categorias)


    @app.route('/eliminar_producto/<int:id>', methods=['POST'])
    def eliminar_producto(id):
        Productos.eliminar_producto(id)
        return redirect(url_for('lista_productos'))