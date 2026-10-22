from itertools import combinations
from typing import List, Dict, Any

def evaluar_restricciones(combo: tuple, cap_peso: float, cap_vol: float):
    """Verifica que no exceda las capacidades del vehiculo (Criterio 1)."""
    peso_total = sum(item['peso'] for item in combo)
    vol_total = sum(item['volumen'] for item in combo)
    es_valido = (peso_total <= cap_peso) and (vol_total <= cap_vol)
    return es_valido, peso_total, vol_total

def optimizar_asignacion_combinatoria(vehiculo: Dict[str, Any], pedidos: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Evalua combinaciones matematicas con itertools.combinations.
    Prioriza pedidos de la misma zona (Criterio 2).
    """
    cap_peso = float(vehiculo['cap_peso'])
    cap_vol = float(vehiculo['cap_vol'])

    if not pedidos:
        return {
            "vehiculo_id": vehiculo.get('id'),
            "placa": vehiculo.get('placa'),
            "zona_priorizada": None,
            "pedidos_asignados": [],
            "peso_total": 0.0,
            "volumen_total": 0.0,
            "cap_peso_max": cap_peso,
            "cap_vol_max": cap_vol
        }

    # Criterio 2: Agrupacion prioritaria por zonas
    pedidos_por_zona = {}
    for p in pedidos:
        zona = p.get('zona', 'General')
        pedidos_por_zona.setdefault(zona, []).append(p)

    mejor_combo = []
    mejor_peso = 0.0
    mejor_vol = 0.0
    zona_optima = None

    for zona, lista_pedidos in pedidos_por_zona.items():
        n = len(lista_pedidos)
        for r in range(1, n + 1):
            for combo in combinations(lista_pedidos, r):
                valido, p_tot, v_tot = evaluar_restricciones(combo, cap_peso, cap_vol)
                if valido:
                    if (len(combo) > len(mejor_combo)) or \
                       (len(combo) == len(mejor_combo) and p_tot > mejor_peso):
                        mejor_combo = list(combo)
                        mejor_peso = p_tot
                        mejor_vol = v_tot
                        zona_optima = zona

    return {
        "vehiculo_id": vehiculo.get('id'),
        "placa": vehiculo.get('placa'),
        "zona_priorizada": zona_optima,
        "pedidos_asignados": mejor_combo,
        "peso_total": round(mejor_peso, 2),
        "volumen_total": round(mejor_vol, 2),
        "cap_peso_max": cap_peso,
        "cap_vol_max": cap_vol
    }