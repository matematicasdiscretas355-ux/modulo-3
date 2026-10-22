from flask import Blueprint, render_template, request, jsonify
from functools import wraps
from database import get_db
from combinatoria_service import optimizar_asignacion_combinatoria

modulo3_bp = Blueprint('modulo3', __name__, template_folder='templates', static_folder='static')

TOKEN_ACCESO_SEGURO = "Bearer SMART_ROUTE_AUTH_TOKEN_2026"

def validar_token_acceso(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token != TOKEN_ACCESO_SEGURO:
            return jsonify({"error": "Acceso no autorizado: Token invalido o ausente."}), 401
        return f(*args, **kwargs)
    return decorador

@modulo3_bp.route('/asignacion', methods=['GET'])
def vista_asignacion_combinatoria():
    conn = get_db()
    vehiculos = conn.execute("SELECT * FROM vehiculos WHERE estado = 'Disponible'").fetchall()
    pedidos = conn.execute("SELECT * FROM pedidos WHERE estado = 'Pendiente'").fetchall()
    conn.close()
    return render_template('modulo3/asignacion.html', vehiculos=vehiculos, pedidos=pedidos)

@modulo3_bp.route('/asignacion/api/calcular', methods=['POST'])
@validar_token_acceso
def api_calcular_asignacion():
    data = request.get_json() or {}
    vehiculo_id = data.get('vehiculo_id')
    pedidos_ids = data.get('pedidos_ids', [])

    if not vehiculo_id or not pedidos_ids:
        return jsonify({"error": "Debe enviar vehiculo_id y la lista pedidos_ids."}), 400

    conn = get_db()
    cursor = conn.cursor()

    vehiculo_row = cursor.execute("SELECT * FROM vehiculos WHERE id = ?", (vehiculo_id,)).fetchone()
    if not vehiculo_row:
        conn.close()
        return jsonify({"error": "El vehiculo no existe."}), 404

    placeholders = ','.join(['?'] * len(pedidos_ids))
    pedidos_rows = cursor.execute(
        f"SELECT * FROM pedidos WHERE id IN ({placeholders}) AND estado = 'Pendiente'",
        pedidos_ids
    ).fetchall()

    vehiculo_dict = dict(vehiculo_row)
    pedidos_list = [dict(p) for p in pedidos_rows]

    resultado = optimizar_asignacion_combinatoria(vehiculo_dict, pedidos_list)

    if resultado['pedidos_asignados']:
        for p in resultado['pedidos_asignados']:
            cursor.execute("UPDATE pedidos SET estado = 'Asignado', vehiculo_id = ? WHERE id = ?", (vehiculo_id, p['id']))
        cursor.execute("UPDATE vehiculos SET estado = 'Asignado' WHERE id = ?", (vehiculo_id,))
        conn.commit()

    conn.close()
    return jsonify(resultado), 200

@modulo3_bp.route('/asignacion/reiniciar-datos', methods=['POST'])
def reiniciar_datos_prueba():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE pedidos SET estado = 'Pendiente', vehiculo_id = NULL")
    cursor.execute("UPDATE vehiculos SET estado = 'Disponible'")
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Datos restaurados a Pendiente y Disponible."})