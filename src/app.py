from flask import Flask
from src.models import Base, engine
from flask_controller import FlaskControllerRegister


app = Flask(__name__)

app.secret_key = "mi llaveria"
app.debug = True

register = FlaskControllerRegister(app)
register.register_package('src.controllers')

Base.metadata.create_all(engine)

if __name__ == '__main__':
    app.run(debug=True)



