from flask import Flask, redirect, url_for
from database import inicializar_bd
from routes import modulo3_bp

app = Flask(__name__)
app.secret_key = "smartroute_secret_key_2026"

inicializar_bd()

# Registro del Blueprint
app.register_blueprint(modulo3_bp)

@app.route('/')
def home():
    return redirect(url_for('modulo3.vista_asignacion'))

if __name__ == '__main__':
    print("=" * 60)
    print(" SmartRoute Web - Módulo 3 listo para integración")
    print(" Accede a: http://127.0.0.1:5000/asignacion")
    print("=" * 60)
    app.run(debug=True, port=5000)