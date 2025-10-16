from flask import render_template, request, redirect, url_for
from flask_controller import FlaskController
from src.models.usuarios import Usuarios
from src.app import app

class UsuariosController(FlaskController):
    @app.route('/lista_usuario')    
    def lista_usuario():
        usuarios = Usuarios.traer_usuarios()
        return render_template('lista_usuario.html',titulo='Ver usuarios', usuarios = usuarios)

    @app.route('/formulario_usuario', methods=['GET', 'POST'])
    def formulario_usuario():
        if request.method == 'POST':
            nombre_usuario = request.form.get('nombre_usuario')
            id_usuario = request.form.get('id_usuario')
            identificacion_usuario = request.form.get('identificacion_usuario')
            rol_perfil = request.form.get('rol_perfil')
            email_usuario = request.form.get('email_usuario')

            usuario = Usuarios(nombre_usuario, id_usuario, identificacion_usuario, rol_perfil, email_usuario)
            Usuarios.crear_usuario(usuario)
            return redirect(url_for('lista_usuario'))

        return render_template('formulario_usuario.html',titulo='Crear usuario', usuario_almacenar=None)

    @app.route('/consultar_usuario_id_usuario/<id_usuario>')
    def consultar_usuario_id_usuario(id_usuario):
        usuario = Usuarios.obtener_usuario_por_id_usuario(id_usuario)
        return usuario   

    @app.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
    def editar_usuario(id):
        usuario = Usuarios.traer_usuario_por_id(id)

        if request.method == 'POST':
            usuario.nombre_usuario = request.form.get('nombre_usuario')
            usuario.id_usuario = request.form.get('id_usuario')
            usuario.identificacion_usuario = request.form.get('identificacion_usuario')
            usuario.rol_perfil = request.form.get('rol_perfil')
            usuario.email_usuario = request.form.get('email_usuario')

            Usuarios.actualizar_usuario(usuario)
            return redirect(url_for('lista_usuario'))

        return render_template('formulario_usuario.html',
                            titulo='Editar usuario',
                            usuario_almacenar=usuario)


    @app.route('/eliminar_usuario/<int:id>', methods=['POST'])
    def eliminar_usuario(id):
        Usuarios.eliminar_usuario(id)
        return redirect(url_for('lista_usuario'))