from flask import Flask, redirect, url_for
from database import inicializar_bd
from routes import modulo3_bp

app = Flask(__name__)
app.secret_key = "clave_secreta_modulo_3_desarrollo"

app.register_blueprint(modulo3_bp)

@app.route('/')
def index():
    return redirect(url_for('modulo3.vista_asignacion_combinatoria'))

if __name__ == '__main__':
    inicializar_bd()
    print("==========================================================")
    print(" SmartRoute Web - Modulo 3: Asignacion Combinatoria")
    print(" Servidor corriendo en: http://127.0.0.1:5000/asignacion")
    print("==========================================================")
    app.run(debug=True, port=5000)