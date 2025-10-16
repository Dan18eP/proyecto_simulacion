from simulacion import Simulacion

def mostrar_resultados(self):
        total_incidentes = self.metricas["incidentes_totales"]
        print("\nRESULTADOS DE SIMULACIÓN")
        print(f"Tiempo simulado: {self.duracion}")
        print(f"Incidentes generados: {total_incidentes}")
        print(f"Incidentes atendidos con éxito (global): {self.metricas['incidentes_exitosos']}")
        print(f"Incidentes no trasladados (global): {self.metricas['incidentes_fallidos']}")

        # Porcentaje atendido por vehículo (sobre total de incidentes generados)
        print("\nPorcentaje de reportes atendidos por vehículo (sobre total generado):")
        for v in self.vehiculos:
            pct = (v.incidentes_atendidos / total_incidentes * 100) if total_incidentes else 0.0
            print(f" - {v.nombre}: {v.incidentes_atendidos} atendidos, {pct:.2f}% del total")

        # Porcentaje usuarios no trasladados (fallidos)
        no_trasladados_pct = (self.metricas['incidentes_fallidos'] / total_incidentes * 100) if total_incidentes else 0.0
        print(f"\nPorcentaje de usuarios no trasladados: {no_trasladados_pct:.2f}%")

        # Distancia total y promedio por vehículo
        print("\nDistancia recorrida por vehículo:")
        suma_distancias = 0.0
        for v in self.vehiculos:
            print(f" - {v.nombre}: distancia total = {v.distancia_total:.2f}")
            suma_distancias += v.distancia_total
        distancia_promedio = (suma_distancias / len(self.vehiculos)) if self.vehiculos else 0.0
        print(f"Distancia promedio por vehículo: {distancia_promedio:.2f}\n")


if __name__ == "__main__":

    simulacion = Simulacion(duracion_simulacion=50, intervalo=1, pausa_visual=False)
    simulacion.ejecutar()