import math
from generadores import gen_vehiculos, gen_reportes
from geometria import   A1, A2, EP1, EP2, MAPA_LIMITES, RUTAS


def evento_incidente():
    """Genera un incidente aleatorio en A1 o A2 con coordenadas válidas dentro del área."""
    # Elegir zona aleatoriamente
    for _ in range(100):
        rand_zona = gen_reportes.aleatorio()
    zona_incidente = A1 if rand_zona < 0.5 else A2
    
    
    

    if zona_incidente.tipo == "triangulo":
        # Generar punto aleatorio dentro del triángulo usando coordenadas baricéntricas
        vertices = zona_incidente.parametros["vertices"]
        x_coord, y_coord = _generar_punto_en_triangulo(vertices)

    elif zona_incidente.tipo == "semicirculo":
        # Generar punto aleatorio en semicírculo con apertura hacia ABAJO
        centro_x, centro_y = zona_incidente.parametros["centro"]
        radio = zona_incidente.parametros["radio"]
        
        # Radio aleatorio (distribución uniforme en área)
        r = radio * math.sqrt(gen_reportes.aleatorio())
        
        # Ángulo de π a 2π (semicírculo inferior: 180° a 360°)
        angulo = math.pi * (1 + gen_reportes.aleatorio())
        
        x_coord = centro_x + r * math.cos(angulo)
        y_coord = centro_y + r * math.sin(angulo)

    else:
        raise ValueError(f"Tipo de área desconocido: {zona_incidente.tipo}")

    print(f"[EV_INCIDENTE] Generado en {zona_incidente.nombre:<3} | Coordenadas: ({x_coord:.2f}, {y_coord:.2f})")

    return {
        "zona": zona_incidente.nombre,
        "x": x_coord,
        "y": y_coord
    }


def _generar_punto_en_triangulo(vertices):
    """
    Genera un punto aleatorio uniformemente distribuido dentro de un triángulo.
    Usa coordenadas baricéntricas.
    """
    v1, v2, v3 = vertices
    
    # Generar dos números aleatorios
    r1 = gen_reportes.aleatorio()
    r2 = gen_reportes.aleatorio()
    
    # Transformación para distribución uniforme en triángulo
    sqrt_r1 = math.sqrt(r1)
    
    # Coordenadas baricéntricas
    a = 1 - sqrt_r1
    b = sqrt_r1 * (1 - r2)
    c = sqrt_r1 * r2
    
    # Punto resultante
    x = a * v1[0] + b * v2[0] + c * v3[0]
    y = a * v1[1] + b * v2[1] + c * v3[1]
    
    return x, y


def evento_llegada_vehiculo(vehiculo, incidente):
    """Simula la llegada de un vehículo al punto del incidente."""
    print(f"[EV_LLEGADA_VEHICULO] {vehiculo['nombre']} llegó al incidente en zona {incidente['zona']}.")

    # Probabilidad 60% de contacto exitoso
    contacto_exitoso = gen_vehiculos.aleatorio() < 0.6
    
    if contacto_exitoso:
        print("Contacto exitoso. Iniciando traslado al punto de evacuación correspondiente.")
        estacion = evento_fin_traslado_ep(vehiculo, incidente)
        return {"vehiculo": vehiculo["nombre"], "resultado": "EXITO", "ep": estacion}
    else:
        print("Contacto fallido. Usuario no encontrado. Retornando a ruta de patrulla.")
        vehiculo["estado"] = "PATRULLANDO"
        return {"vehiculo": vehiculo["nombre"], "resultado": "FALLO"}


def evento_fin_traslado_ep(vehiculo, incidente):
    """Evento que marca el fin del traslado hacia una estación EP."""
    # Si el incidente fue en A1 → llevar a EP2
    # Si el incidente fue en A2 → llevar a EP1
    estacion_destino = EP2 if incidente["zona"] == "A1" else EP1

    print(f"[EV_FIN_TRASLADO_EP] {vehiculo['nombre']} completó traslado hacia {estacion_destino['nombre']}.")
    vehiculo["estado"] = "DISPONIBLE"

    return estacion_destino["nombre"]


def evento_tick_patrulla(vehiculo):
    """
    Actualiza la posición de un vehículo durante la patrulla.
    Usa límites correctos del mapa y movimiento más realista.
    """
    # Movimiento aleatorio pero contenido
    delta_x = (gen_vehiculos.aleatorio() - 0.5) * 2  # Entre -1 y 1
    delta_y = (gen_vehiculos.aleatorio() - 0.5) * 2  # Entre -1 y 1
    
    # Velocidad variable entre 2.5 y 7.5 km/tick
    velocidad = 5 * (0.5 + gen_vehiculos.aleatorio())

    # Actualizar posición
    vehiculo["x"] += delta_x * velocidad
    vehiculo["y"] += delta_y * velocidad

    # Mantener dentro de los límites del mapa
    vehiculo["x"] = max(MAPA_LIMITES["x_min"], min(vehiculo["x"], MAPA_LIMITES["x_max"]))
    vehiculo["y"] = max(MAPA_LIMITES["y_min"], min(vehiculo["y"], MAPA_LIMITES["y_max"]))

    print(
        f"[EV_TICK_PATRULLA] {vehiculo['nombre']:<12} | "
        f"Pos: ({vehiculo['x']:5.1f}, {vehiculo['y']:5.1f}) | "
        f"Vel: {velocidad:.1f} km/tick"
    )

    return {
        "vehiculo": vehiculo["nombre"], 
        "x": vehiculo["x"], 
        "y": vehiculo["y"], 
        "velocidad": velocidad
    }


#Patrullaje en rutas específicas


def evento_tick_patrulla_con_rutas(vehiculo, indice_vehiculo):
    """
    Los vehículos patrullan siguiendo rutas predefinidas.
    
    Vehículo 1: suroccidente → noroccidente → nororiente
    Vehículo 2: suroccidente → suroriente → nororiente
    Vehículo 3: Ubicado alrededor del CAI (centro)
    """
    # Obtener ruta del vehículo
    ruta_key = f"vehiculo_{indice_vehiculo + 1}"
    if ruta_key not in RUTAS:
        # Fallback al patrullaje aleatorio
        return evento_tick_patrulla(vehiculo)
    
    puntos_ruta = RUTAS[ruta_key]["puntos_clave"]
    
    # Si no tiene waypoint actual, asignar el primero
    if "waypoint_actual" not in vehiculo:
        vehiculo["waypoint_actual"] = 0
    
    # Obtener waypoint destino
    idx_waypoint = vehiculo["waypoint_actual"]
    destino_x, destino_y = puntos_ruta[idx_waypoint]
    
    # Calcular dirección hacia el waypoint
    dx = destino_x - vehiculo["x"]
    dy = destino_y - vehiculo["y"]
    distancia = math.hypot(dx, dy)
    
    # Velocidad de patrulla
    velocidad = 3.0 + 2.0 * gen_vehiculos.aleatorio()  # 3-5 km/tick
    
    # Si está cerca del waypoint, cambiar al siguiente
    if distancia < velocidad:
        vehiculo["x"] = destino_x
        vehiculo["y"] = destino_y
        vehiculo["waypoint_actual"] = (idx_waypoint + 1) % len(puntos_ruta)
        print(f"[EV_TICK_PATRULLA] {vehiculo['nombre']} alcanzó waypoint {idx_waypoint + 1}")
    else:
        # Moverse hacia el waypoint
        vehiculo["x"] += (dx / distancia) * velocidad
        vehiculo["y"] += (dy / distancia) * velocidad
    
    # Pequeña variación aleatoria para simular tráfico
    vehiculo["x"] += (gen_vehiculos.aleatorio() - 0.5) * 0.5
    vehiculo["y"] += (gen_vehiculos.aleatorio() - 0.5) * 0.5
    
    # Mantener en límites
    vehiculo["x"] = max(MAPA_LIMITES["x_min"], min(vehiculo["x"], MAPA_LIMITES["x_max"]))
    vehiculo["y"] = max(MAPA_LIMITES["y_min"], min(vehiculo["y"], MAPA_LIMITES["y_max"]))
    
    print(
        f"[EV_TICK_PATRULLA] {vehiculo['nombre']:<12} | "
        f"Pos: ({vehiculo['x']:5.1f}, {vehiculo['y']:5.1f}) | "
        f"→ Waypoint {idx_waypoint + 1}: ({destino_x}, {destino_y}) | "
        f"Dist: {distancia:.1f} km"
    )
    
    return {
        "vehiculo": vehiculo["nombre"],
        "x": vehiculo["x"],
        "y": vehiculo["y"],
        "velocidad": velocidad
    }