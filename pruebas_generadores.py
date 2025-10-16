# Validación estadística de los generadores mixtos

from generadores import GeneradorMixto, prueba_frecuencia, prueba_distancia
from registro_resultados import guardar_resultados
import matplotlib.pyplot as plt


def validar_generador(nombre, a, c, m, x0):
    """Ejecuta las pruebas estadísticas de un generador y muestra los resultados."""
    generador = GeneradorMixto(a, c, m, x0)
    valores = [generador.aleatorio() for _ in range(m//2)]

    chi_cuadrado, frecuencias_observadas = prueba_frecuencia(valores)
    promedio, esperado, diferencia = prueba_distancia(valores)
    estado = "Aprobada" if diferencia < 0.02 else "Posible desviación"
    parametros = {"a": a, "c": c, "m": m, "x0": x0}

    print(f"{nombre}")
    print(f"Parámetros: a={a}, c={c}, m={m}, x0={x0}")
    print(f"Chi² (frecuencia): {chi_cuadrado:.3f}")
    print(f"Frecuencias por intervalo: {frecuencias_observadas}")
    print(f"Distancia promedio: {promedio:.4f}")
    print(f"Valor esperado: {esperado:.4f}")
    print(f"Diferencia: {diferencia:.4f}")
    print(f"Estado de la prueba: {estado}\n")
    
    guardar_resultados(nombre, parametros, chi_cuadrado, frecuencias_observadas, promedio, esperado, diferencia, estado)


if __name__ == "__main__":
    validar_generador("Generador Vehículos", a=501, c=547, m=1000, x0=827)
    validar_generador("Generador Reportes", a=5001, c=4607, m=10000, x0=4049)

    print("Validación completada. Si las frecuencias son equilibradas y la distancia promedio ≈ 0.2887, los generadores son estadísticamente aceptables.")
    

    
