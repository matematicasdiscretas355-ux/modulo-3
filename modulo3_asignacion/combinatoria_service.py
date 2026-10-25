from itertools import combinations
from typing import List, Dict, Any

def evaluar_restricciones(combo: tuple, cap_peso: float, cap_vol: float):
    # Criterio 1: Capacidad nominal de peso y volumen
    peso_total = sum(item['peso'] for item in combo)
    vol_total = sum(item['volumen'] for item in combo)
    if peso_total > cap_peso or vol_total > cap_vol:
        return False, peso_total, vol_total
        
    # Criterio 2: Afinidad de zona única
    zonas = {item['zona'] for item in combo}
    if len(zonas) > 1:
        return False, peso_total, vol_total
        
    return True, peso_total, vol_total

def optimizar_asignacion_combinatoria(vehiculo: Dict[str, Any], pedidos: List[Dict[str, Any]]) -> Dict[str, Any]:
    cap_peso = float(vehiculo.get('cap_peso', 0.0))
    cap_vol = float(vehiculo.get('cap_vol', 0.0))
    placa = vehiculo.get('placa', '')

    if not pedidos:
        return {
            "vehiculo_id": vehiculo.get('id'),
            "placa": placa,
            "zona_priorizada": "N/A",
            "cap_peso": cap_peso,
            "cap_vol": cap_vol,
            "peso_total": 0.0,
            "volumen_total": 0.0,
            "pedidos_asignados": [],
            "combinaciones_evaluadas": 0
        }

    mejor_combo = []
    mejor_peso = 0.0
    mejor_vol = 0.0
    max_pedidos = 0
    total_evaluadas = 0

    for r in range(1, len(pedidos) + 1):
        for combo in combinations(pedidos, r):
            total_evaluadas += 1
            es_valido, p_total, v_total = evaluar_restricciones(combo, cap_peso, cap_vol)
            
            if es_valido:
                if (len(combo) > max_pedidos) or (len(combo) == max_pedidos and p_total > mejor_peso):
                    max_pedidos = len(combo)
                    mejor_peso = p_total
                    mejor_vol = v_total
                    mejor_combo = list(combo)

    zona_priorizada = mejor_combo[0]['zona'] if mejor_combo else "N/A"

    return {
        "vehiculo_id": vehiculo.get('id'),
        "placa": placa,
        "zona_priorizada": zona_priorizada,
        "cap_peso": int(cap_peso) if cap_peso.is_integer() else cap_peso,
        "cap_vol": int(cap_vol) if cap_vol.is_integer() else cap_vol,
        "peso_total": int(mejor_peso) if mejor_peso.is_integer() else round(mejor_peso, 2),
        "volumen_total": int(mejor_vol) if mejor_vol.is_integer() else round(mejor_vol, 2),
        "pedidos_asignados": mejor_combo,
        "combinaciones_evaluadas": total_evaluadas
    }