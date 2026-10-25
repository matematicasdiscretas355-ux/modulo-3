from combinatoria_service import optimizar_asignacion_combinatoria

def test_caso_prueba_03():
    print("==========================================================")
    print(" EJECUTANDO PRUEBA CP-03: Asignacion Combinatoria")
    print("==========================================================")

    vehiculo = {"id": 1, "placa": "ABC-123", "cap_peso": 500.0, "cap_vol": 10.0}
    pedidos = [
        {"id": "P-01", "peso": 300.0, "volumen": 1.0, "zona": "Norte"},
        {"id": "P-02", "peso": 300.0, "volumen": 1.0, "zona": "Norte"},
        {"id": "P-03", "peso": 300.0, "volumen": 1.0, "zona": "Norte"}
    ]

    resultado = optimizar_asignacion_combinatoria(vehiculo, pedidos)

    total_pedidos = len(resultado['pedidos_asignados'])
    peso_asignado = resultado['peso_total']

    print(f"Vehiculo: {resultado['placa']} (Capacidad: {resultado['cap_peso_max']} kg)")
    print(f"Pedidos asignados: {[p['id'] for p in resultado['pedidos_asignados']]}")
    print(f"Peso total cargado: {peso_asignado} kg")

    assert total_pedidos == 1, f"Error: Se debio asignar exactamente 1 pedido, asignados: {total_pedidos}"
    assert peso_asignado <= 500.0, f"Error: El peso {peso_asignado} supero la capacidad maxima de 500kg"

    print("\n-> Criterio 1: Suma de peso jamas supero la capacidad maxima nominal.")
    print("-> Resultado Esperado CP-03: Asigna maximo 1 pedido (300kg).")
    print("-> TEST CP-03 EXITOSO!")
    print("==========================================================")

if __name__ == '__main__':
    test_caso_prueba_03()