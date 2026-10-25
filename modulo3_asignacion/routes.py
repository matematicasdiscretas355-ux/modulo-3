from flask import Blueprint, render_template, request, jsonify
from database import get_db
from combinatoria_service import optimizar_asignacion_combinatoria

modulo3_bp = Blueprint('modulo3', __name__)

@modulo3_bp.route('/asignacion', methods=['GET'])
def vista_asignacion():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, placa, cap_peso, cap_vol FROM vehiculos WHERE estado = 'Disponible'")
    vehiculos = cursor.fetchall()
    
    cursor.execute("SELECT id, peso, volumen, zona, estado FROM pedidos WHERE estado = 'Pendiente'")
    pedidos = cursor.fetchall()
    
    conn.close()
    return render_template('modulo3/asignacion.html', vehiculos=vehiculos, pedidos=pedidos)

@modulo3_bp.route('/asignacion/calcular', methods=['POST'])
def api_calcular_asignacion():
    data = request.get_json()
    vehiculo_id = data.get('vehiculo_id')
    pedidos_ids = data.get('pedidos_ids', [])
    
    if not vehiculo_id or not pedidos_ids:
        return jsonify({"error": "Debe seleccionar un vehículo y al menos un pedido"}), 400
        
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, placa, cap_peso, cap_vol FROM vehiculos WHERE id = ?", (vehiculo_id,))
    v_row = cursor.fetchone()
    
    if not v_row:
        conn.close()
        return jsonify({"error": "Vehículo no encontrado"}), 404
        
    vehiculo = {
        'id': v_row[0],
        'placa': v_row[1],
        'cap_peso': float(v_row[2]),
        'cap_vol': float(v_row[3])
    }
    
    placeholders = ','.join(['?'] * len(pedidos_ids))
    cursor.execute(f"SELECT id, peso, volumen, zona FROM pedidos WHERE id IN ({placeholders})", pedidos_ids)
    p_rows = cursor.fetchall()
    conn.close()
    
    pedidos = [
        {
            'id': row[0],
            'peso': float(row[1]),
            'volumen': float(row[2]),
            'zona': row[3]
        }
        for row in p_rows
    ]
    
    resultado = optimizar_asignacion_combinatoria(vehiculo, pedidos)
    return jsonify(resultado)