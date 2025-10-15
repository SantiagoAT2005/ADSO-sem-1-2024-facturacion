from flask import flask, render_template

app= flask(__name__)

if __name__== "__main__":
    app.run(debug=True)

    @app.route("/")
    def index():
        return render_template("index-html" ,titulo="Bienvenido a la aplicación de facturación")
    
    @app.route("/Lista_productos")
    def Lista_productos():
        return render_template("Lista_productos.html",titulo="Ver productos")
    
    @app.route("/formulario_producto")
    def formulario_producto():
        return render_template("formulario_producto.html",titulo="Crear un producto")