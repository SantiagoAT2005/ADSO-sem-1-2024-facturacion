from flask import render_template, request, redirect, url_for
from flask_controller import FlaskController
from src.models.facturas import Facturas
from src.models.categorias import Categorias
from src.app import app

class FacturasController(FlaskController):  
    @app.route('/lista_factura')
    def lista_factura():
        facturas = Facturas.traer_facturas()
        return render_template('lista_factura.html',titulo='Facturas', facturas = facturas)   

    @app.route('/formulario_factura', methods=['GET', 'POST'])
    def formulario_factura():
        categorias = Categorias.traer_categoria()
        if request.method == 'POST':
            codigo = request.form.get('codigo')
            descripcion = request.form.get('descripcion')
            precio_unitario = request.form.get('precio_unitario')
            unidad_medida = request.form.get('unidad_medida')
            categoria = request.form.get('categoria')
            forma_pago_factura = request.form.get('forma_pago_factura')
            identificacion_cliente = request.form.get('identificacion_cliente')
            nombre_cliente = request.form.get('nombre_cliente')
            fecha_cliente = request.form.get('fecha_cliente')   
            email_cliente = request.form.get('email_cliente')
            id_usuario = request.form.get('id_usuario')
            nombre_usuario = request.form.get('nombre_usuario')
            identificacion_usuario = request.form.get('identificacion_usuario')
            rol_perfil = request.form.get('rol_perfil')
            email_usuario = request.form.get('email_usuario')

            factura = Facturas(codigo, descripcion, precio_unitario, unidad_medida, categoria, forma_pago_factura
                                , identificacion_cliente, nombre_cliente, fecha_cliente, email_cliente
                                , id_usuario, nombre_usuario, identificacion_usuario, rol_perfil, email_usuario)
            
            Facturas.crear_factura(factura)
            return redirect(url_for('lista_factura'))
            
        return render_template('formulario_factura.html',titulo='Crear factura', factura_almacenar=None, categorias = categorias)
    
    @app.route('/editar_factura/<int:id>', methods=['GET', 'POST'])
    def editar_factura(id):
        factura = Facturas.traer_factura_por_id(id)
        categorias = Categorias.traer_categoria()

        if request.method == 'POST':
            factura.codigo = request.form.get('codigo')
            factura.descripcion = request.form.get('descripcion')
            factura.precio_unitario = request.form.get('precio_unitario')
            factura.unidad_medida = request.form.get('unidad_medida')
            factura.categoria = request.form.get('categoria')
            factura.forma_pago_factura = request.form.get('forma_pago_factura')
            factura.identificacion_cliente = request.form.get('identificacion_cliente')
            factura.nombre_cliente = request.form.get('nombre_cliente')
            factura.fecha_cliente = request.form.get('fecha_cliente')   
            factura.email_cliente = request.form.get('email_cliente')
            factura.id_usuario = request.form.get('id_usuario')
            factura.nombre_usuario = request.form.get('nombre_usuario')
            factura.identificacion_usuario = request.form.get('identificacion_usuario')
            factura.rol_perfil = request.form.get('rol_perfil')
            factura.email_usuario = request.form.get('email_usuario')


            Facturas.actualizar_factura(factura)
            return redirect(url_for('lista_factura'))

        return render_template('formulario_factura.html',
                            titulo='Editar factura',
                            factura_almacenar=factura,
                            categorias=categorias)


    @app.route('/eliminar_factura/<int:id>', methods=['POST'])
    def eliminar_factura(id):
        Facturas.eliminar_factura(id)
        return redirect(url_for('lista_factura'))
    