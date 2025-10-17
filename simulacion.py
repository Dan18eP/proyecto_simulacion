# simulacion.py
import math
import time
from eventos import evento_incidente, evento_llegada_vehiculo, evento_tick_patrulla, evento_tick_patrulla_con_rutas
from generadores import gen_reportes
from geometria import EP1, EP2, MAPA_LIMITES


class Vehiculo:
    """Representa un vehículo de respuesta o patrulla."""
    def __init__(self, nombre, x, y, velocidad=2.0):
        """
        velocidad: unidades de distancia por unidad de tiempo del simulador (km/tick)
        """
        self.nombre = nombre
        self.x = float(x)
        self.y = float(y)
        self.velocidad = float(velocidad)
        self.estado = "PATRULLANDO"      # PATRULLANDO, DESPACHADO, TRASLADANDO, DISPONIBLE
        self.incidentes_atendidos = 0
        self.incidentes_fallidos = 0
        self.distancia_total = 0.0
        self.reportes_asignados = 0

    def mover_a(self, destino_x, destino_y):
        """Mueve el vehículo al punto destino y acumula la distancia recorrida."""
        distancia = math.hypot(self.x - destino_x, self.y - destino_y)
        self.distancia_total += distancia
        self.x = float(destino_x)
        self.y = float(destino_y)
        return distancia

    def distancia_a(self, x_objetivo, y_objetivo):
        """Calcula la distancia euclidiana al punto objetivo."""
        return math.hypot(self.x - x_objetivo, self.y - y_objetivo)

    def eta_a(self, x_objetivo, y_objetivo):
        """
        Calcula el ETA (Estimated Time of Arrival) al punto objetivo.
        Retorna: tiempo estimado en unidades de simulación (distancia / velocidad)
        """
        distancia = self.distancia_a(x_objetivo, y_objetivo)
        if self.velocidad <= 0:
            return float("inf")
        return distancia / self.velocidad


class Simulacion:
    """Controla la ejecución de la simulación y computa métricas requeridas."""
    
    def __init__(self, duracion_simulacion=100, intervalo=1.0, lambda_incidentes=0.5, pausa_visual=False):
        """
        Parámetros:
        -----------
        duracion_simulacion : float
            Duración total de la simulación en unidades de tiempo
        intervalo : float
            Salto de tiempo por ciclo de simulación
        lambda_incidentes : float
            Tasa promedio de incidentes por unidad de tiempo (parámetro λ de Poisson)
        pausa_visual : bool
            Si True, añade pausa para visualización en consola
        """
        self.duracion = float(duracion_simulacion)
        self.intervalo = float(intervalo)
        self.lambda_incidentes = float(lambda_incidentes)
        self.tiempo_actual = 0.0
        
        # Inicializar vehículos en posición suroccidente (según enunciado)
        self.vehiculos = [
            Vehiculo("Vehiculo 1", x=5.0, y=10.0, velocidad=2.5),
            Vehiculo("Vehiculo 2", x=5.0, y=10.0, velocidad=2.5),
            Vehiculo("Vehiculo 3", x= 32.5, y= 30.0, velocidad=2.5) #Vehículo en CAI (centro)
        ]
        
        self.metricas = {
            "incidentes_totales": 0,
            "incidentes_exitosos": 0,
            "incidentes_fallidos": 0
        }
        self.pausa_visual = pausa_visual

    def seleccionar_vehiculo(self, incidente):
        """
        Selecciona el vehículo más apropiado para responder al incidente.
        
        Criterios de selección:
        1. Solo considera vehículos en estado PATRULLANDO
        2. Prioriza por menor ETA (tiempo estimado de llegada)
        3. En caso de empate, prioriza por menor cantidad de reportes asignados
        
        Retorna:
        --------
        Vehiculo o None si no hay vehículos disponibles
        """
        disponibles = [v for v in self.vehiculos if v.estado == "PATRULLANDO"]
        if not disponibles:
            return None

        candidatos = []
        for v in disponibles:
            eta = v.eta_a(incidente["x"], incidente["y"])
            candidatos.append((eta, v.reportes_asignados, v))

        # Ordenar por ETA, luego por reportes asignados
        candidatos.sort(key=lambda t: (t[0], t[1]))
        vehiculo_seleccionado = candidatos[0][2]
        
        # Cambiar estado y aumentar contador
        vehiculo_seleccionado.estado = "DESPACHADO"
        vehiculo_seleccionado.reportes_asignados += 1
        
        return vehiculo_seleccionado

    def ejecutar(self):
        """
        Ejecuta la simulación principal.
        Genera incidentes con distribución de Poisson y procesa eventos.
        """
        print("=" * 70)
        print("INICIO DE SIMULACIÓN - SISTEMA DE SEGURIDAD UBER")
        print("=" * 70)
        print(f"Duración: {self.duracion} unidades de tiempo")
        print(f"Intervalo: {self.intervalo}")
        print(f"Tasa de incidentes (λ): {self.lambda_incidentes} por unidad de tiempo")
        print(f"Incidentes esperados: ~{int(self.lambda_incidentes * self.duracion)}")
        print(f"Límites del mapa: X ∈ [{MAPA_LIMITES['x_min']}, {MAPA_LIMITES['x_max']}], "
              f"Y ∈ [{MAPA_LIMITES['y_min']}, {MAPA_LIMITES['y_max']}]")
        print("=" * 70 + "\n")
        
        while self.tiempo_actual < self.duracion:
            # Generar número de incidentes usando distribución de Poisson
            num_incidentes = gen_reportes.poisson(self.lambda_incidentes * self.intervalo)
            
            # Procesar cada incidente generado en este tick
            for _ in range(num_incidentes):
                incidente = evento_incidente()
                self.metricas["incidentes_totales"] += 1

                # Seleccionar vehículo más cercano disponible
                vehiculo = self.seleccionar_vehiculo(incidente)
                
                if vehiculo:
                    # Fase 1: Ir al punto del incidente (acumula distancia)
                    vehiculo.mover_a(incidente["x"], incidente["y"])

                    # Fase 2: Intentar contacto con usuario (60% éxito)
                    resultado = evento_llegada_vehiculo(
                        {"nombre": vehiculo.nombre, "estado": vehiculo.estado},
                        incidente
                    )

                    # Fase 3: Si contacto exitoso, trasladar a estación EP
                    if isinstance(resultado, dict) and resultado.get("resultado") == "EXITO":
                        # Determinar estación según zona del incidente
                        ep_obj = EP2 if incidente["zona"] == "A1" else EP1
                        
                        # Trasladar a EP (acumula distancia)
                        vehiculo.mover_a(ep_obj["coordenadas"][0], ep_obj["coordenadas"][1])
                        
                        # Actualizar métricas
                        vehiculo.incidentes_atendidos += 1
                        self.metricas["incidentes_exitosos"] += 1
                    else:
                        # Usuario no encontrado
                        vehiculo.incidentes_fallidos += 1
                        self.metricas["incidentes_fallidos"] += 1

                    # Volver a estado de patrulla
                    vehiculo.estado = "PATRULLANDO"
                else:
                    # No hay vehículos disponibles (todos ocupados)
                    self.metricas["incidentes_fallidos"] += 1
                    print(f"[ALERTA] No hay vehículos disponibles para el incidente en {incidente['zona']}")

            # Actualizar posición de vehículos en patrulla (NO acumula distancia)
            for i, v in enumerate(self.vehiculos):
                if v.estado == "PATRULLANDO":
                    retorno = evento_tick_patrulla_con_rutas({
                        "nombre": v.nombre, 
                        "x": v.x, 
                        "y": v.y
                    }, i)
                    
                    if isinstance(retorno, dict):
                        # Actualizar posición del vehículo
                        v.x = float(retorno.get("x", v.x))
                        v.y = float(retorno.get("y", v.y))

            # Avanzar tiempo
            self.tiempo_actual += self.intervalo
            
            # Pausa visual opcional
            if self.pausa_visual:
                time.sleep(0.1)

        print("\n" + "=" * 70)
        print("FIN DE SIMULACIÓN")
        print(" ")
        self.mostrar_resultados()

    def mostrar_resultados(self):
        """Muestra las métricas finales de la simulación."""
        total_incidentes = self.metricas["incidentes_totales"]
        total_exitosos = self.metricas["incidentes_exitosos"]
        total_fallidos = self.metricas["incidentes_fallidos"]
        
        print(" ")
        print("RESULTADOS DE LA SIMULACIÓN")
        print(" ")
        
        # Métrica 1: Resumen general
        print(f"\n RESUMEN GENERAL")
        print(f"   Tiempo simulado: {self.duracion} unidades")
        print(f"   Tasa λ configurada: {self.lambda_incidentes}")
        print(f"   Incidentes generados: {total_incidentes}")
        print(f"   Incidentes exitosos: {total_exitosos} ({(total_exitosos/total_incidentes*100):.2f}%)")
        print(f"   Incidentes fallidos: {total_fallidos} ({(total_fallidos/total_incidentes*100):.2f}%)")

        # Métrica 2: Porcentaje de reportes atendidos por cada vehículo
        print(f"\n MÉTRICA 2: Porcentaje de reportes atendidos por vehículo")
        print(f"   {'Vehículo':<15} {'Atendidos':<12} {'% del Total':<12} {'Reportes Asignados':<20}")
        print(f"   {'-'*60}")
        for v in self.vehiculos:
            pct_atendidos = (v.incidentes_atendidos / total_incidentes * 100) if total_incidentes else 0.0
            print(f"   {v.nombre:<15} {v.incidentes_atendidos:<12} {pct_atendidos:>6.2f}%      {v.reportes_asignados:<20}")

        # Métrica 3: Porcentaje de usuarios NO trasladados a estaciones
        print(f"\n MÉTRICA 3: Usuarios no trasladados a estaciones de apoyo")
        no_trasladados_pct = (total_fallidos / total_incidentes * 100) if total_incidentes else 0.0
        print(f"   Total no trasladados: {total_fallidos}")
        print(f"   Porcentaje: {no_trasladados_pct:.2f}%")
        
        # Desglose de razones
        usuarios_no_encontrados = sum(v.incidentes_fallidos for v in self.vehiculos)
        sin_vehiculos = total_fallidos - usuarios_no_encontrados
        print(f"   - Usuario no encontrado (40% probabilidad): {usuarios_no_encontrados}")
        print(f"   - Sin vehículos disponibles: {sin_vehiculos}")

        # Métrica 4: Distancia promedio recorrida por vehículo
        print(f"\n MÉTRICA 4: Distancia recorrida por cada vehículo")
        print(f"   {'Vehículo':<15} {'Distancia Total (km)':<25} {'Incidentes Atendidos':<20}")
        print(f"   {'-'*60}")
        
        suma_distancias = 0.0
        for v in self.vehiculos:
            print(f"   {v.nombre:<15} {v.distancia_total:>10.2f} km              {v.incidentes_atendidos:<20}")
            suma_distancias += v.distancia_total
        
        distancia_promedio = (suma_distancias / len(self.vehiculos)) if self.vehiculos else 0.0
        print(f"   {'-'*60}")
        print(f"   {'PROMEDIO':<15} {distancia_promedio:>10.2f} km")
        
        # Estadísticas adicionales
        print(f"\n ESTADÍSTICAS ADICIONALES")
        if total_exitosos > 0:
            distancia_por_exito = suma_distancias / total_exitosos
            print(f"   Distancia promedio por incidente exitoso: {distancia_por_exito:.2f} km")
        
        print(" ")


if __name__ == "__main__":
    # Configuración de la simulación
    simulacion = Simulacion(
        duracion_simulacion=100,   # 100 unidades de tiempo
        intervalo=1.0,              # 1 unidad por tick   
        pausa_visual=False          # Sin pausa (ejecutar rápido)
    )
    
    simulacion.ejecutar()