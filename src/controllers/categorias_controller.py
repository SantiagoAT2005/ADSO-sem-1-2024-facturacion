from src.app import app
from flask import render_template, request, redirect, url_for
from flask_controller import FlaskController
from src.models.categorias import Categorias

class CategoriasController(FlaskController):
    @app.route('/ver_categorias')
    def obtener_lista_categorias():
        categorias = Categorias.obtener_categorias()
        return categorias

