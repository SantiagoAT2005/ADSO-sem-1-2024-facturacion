from flask import render_template, request, redirect, url_for, jsonify
from flask_controller import FlaskController
from src.models.clientes import Clientes
from src.app import app

class ClientesController(FlaskController):
    @app.route('/lista_cliente')
    def lista_cliente():
        clientes = Clientes.traer_clientes()
        return render_template('lista_cliente.html',titulo='Ver clientes', clientes = clientes)   

    @app.route('/formulario_cliente', methods=['GET', 'POST'])
    def formulario_cliente():
        if request.method == 'POST':
            nombre_cliente = request.form.get('nombre_cliente')
            fecha_cliente = request.form.get('fecha_cliente')
            tipo_identificacion = request.form.get('tipo_identificacion')
            identificacion_cliente = request.form.get('identificacion_cliente')
            email_cliente = request.form.get('email_cliente')

            cliente = Clientes(nombre_cliente, fecha_cliente, tipo_identificacion, identificacion_cliente, email_cliente)
            Clientes.crear_cliente(cliente)
            return redirect(url_for('lista_cliente'))
        
        return render_template('formulario_cliente.html',titulo='Crear cliente', cliente_almacenar=None)
    
    @app.route('/consultar_cliente_identificacion_cliente/<cliente>')
    def consultar_cliente_identificacion_cliente(cliente):
        cliente = Clientes.obtener_cliente_por_identificacion_cliente(cliente)
        return jsonify(cliente if cliente else {})
    
    @app.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
    def editar_cliente(id):
        cliente = Clientes.traer_cliente_por_id(id)

        if request.method == 'POST':
            cliente.nombre_cliente = request.form.get('nombre_cliente')
            cliente.fecha_cliente = request.form.get('fecha_cliente')
            cliente.tipo_identificacion = request.form.get('tipo_identificacion')
            cliente.identificacion_cliente = request.form.get('identificacion_cliente')
            cliente.email_cliente = request.form.get('email_cliente')

            Clientes.actualizar_cliente(cliente)
            return redirect(url_for('lista_cliente'))

        return render_template('formulario_cliente.html',
                            titulo='Editar cliente',
                            cliente_almacenar=cliente)
    
    @app.route('/eliminar_cliente/<int:id>', methods=['POST'])
    def eliminar_cliente(id):
        Clientes.eliminar_cliente(id)
        return redirect(url_for('lista_cliente'))
    
    