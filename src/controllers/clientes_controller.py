from src.app import app
from flask import render_template, request, redirect, url_for
from flask_controller import FlaskController
from src.models.clientes import Clientes
from src.models import session, Base

class ClientesController(FlaskController):
    @app.route('/crear_cliente', methods=['POST','GET'])
    def crear_cliente():    
        if request.method == 'POST':
            numero_identificacion = request.form.get('numero_identificacion')                
            nombre = request.form.get('nombre')    
            email = request.form.get('email')    
            telefono = request.form.get('telefono')    
            direccion = request.form.get('direccion')    
            cliente = Clientes(numero_identificacion,nombre,email,telefono,direccion)
            session.add(cliente)
            session.commit()
            return redirect(url_for('ver_clientes'))
        return render_template('formulario_cliente.html', titulo_pagina = 'Crear Cliente')

    @app.route('/ver_clientes')
    def ver_clientes():
        clientes = session.query(Clientes).all()
        return render_template('lista_clientes.html', clientes=clientes)

    @app.route('/eliminar_cliente/<id>')
    def eliminar_cliente(id):
        cliente = session.query(Clientes).get(id)
        session.delete(cliente)
        session.commit()
        return redirect(url_for('lista_clientes'))

    @app.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
    def editar_cliente(id):
        cliente = session.query(Clientes).get(id)

        if request.method == 'POST':
            cliente.numero_identificacion = request.form.get('numero_identificacion')
            cliente.nombre = request.form.get('nombre')
            cliente.email = request.form.get('email')
            cliente.telefono = request.form.get('telefono')
            cliente.direccion = request.form.get('direccion')
            
            
           
            session.commit()

            return redirect(url_for('ver_clientes'))

        return render_template('editar_cliente.html',
                            titulo='Editar Cliente',
                            cliente=cliente)




