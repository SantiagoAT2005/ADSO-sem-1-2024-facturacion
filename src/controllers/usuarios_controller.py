from src.app import app
from flask import render_template, request, redirect, url_for
from flask_controller import FlaskController
from src.models.usuarios import Usuarios
from src.models import session, Base

class UsuariosController(FlaskController):
    @app.route('/crear_usuario', methods=['POST','GET'])
    def crear_usuario():    
        if request.method == 'POST':
                        
            nombre = request.form.get('nombre')    
            email = request.form.get('email')    
            contraseña = request.form.get('contraseña')    
            rol = request.form.get('rol')    
            usuario = Usuarios(nombre,email,contraseña,rol)
            session.add(usuario)
            session.commit()
            return redirect(url_for('ver_usuarios'))
        return render_template('formulario_usuario.html', titulo_pagina = 'Crear Usuario')

    @app.route('/ver_usuarios')
    def ver_usuarios():
        usuarios = session.query(Usuarios).all()
        return render_template('lista_usuarios.html', usuarios=usuarios)

    @app.route('/eliminar_usuario/<id>')
    def eliminar_usuario(id):
        usuario = session.query(Usuarios).get(id)
        session.delete(usuario)
        session.commit()
        return redirect(url_for('ver_usuarios'))

    @app.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
    def editar_usuario(id):
        usuario = session.query(Usuarios).get(id)

        if request.method == 'POST':
            usuario.nombre = request.form.get('nombre')
            usuario.email = request.form.get('email')
            usuario.contraseña = request.form.get('contraseña')
            usuario.rol = request.form.get('rol')


           
            session.commit()

            return redirect(url_for('ver_usuarios'))

        return render_template('editar_usuario.html',
                            titulo='Editar Usuario',
                            usuario=usuario)




