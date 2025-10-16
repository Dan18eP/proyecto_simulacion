# Módulo de generadores mixtos para simulación de seguridad Uber

import math

class GeneradorMixto:
    """Implementa un generador congruencial lineal mixto (LCG mixto)."""

    def __init__(self, a, c, m, x0):
        self.a = a
        self.c = c
        self.m = m
        self.x = x0

    def siguiente(self):
        """Genera el siguiente número entero Xn."""
        self.x = (self.a * self.x + self.c) % self.m
        return self.x

    def aleatorio(self):
        """Retorna un número aleatorio U en [0,1)."""
        return self.siguiente() / self.m
    
    def poisson(self, lmbda):
        """
        Genera una variable aleatoria con distribución de Poisson.
        lmbda: tasa promedio de eventos (lambda)
        Retorna: número de eventos que ocurren
        """
        if lmbda <= 0:
            return 0
        
        L = math.exp(-lmbda)
        k = 0
        p = 1.0
        
        while p > L:
            k += 1
            p *= self.aleatorio()
        
        return k - 1


# Pruebas de bondad de ajuste
def prueba_frecuencia(valores, num_intervalos=10):
    """Prueba de Frecuencia: divide [0,1) en k intervalos y compara frecuencias."""
    
    total_valores = len(valores)
    frecuencias_observadas = [0] * num_intervalos

    # Contar cuántos valores caen en cada intervalo
    for valor in valores:
        indice_intervalo = min(int(valor * num_intervalos), num_intervalos - 1)
        frecuencias_observadas[indice_intervalo] += 1

    frecuencia_esperada = total_valores / num_intervalos
    chi_cuadrado = sum(
        (observado - frecuencia_esperada) ** 2 / frecuencia_esperada
        for observado in frecuencias_observadas
    )

    return chi_cuadrado, frecuencias_observadas


def prueba_distancia(valores):
    """Prueba de Distancia: mide la distancia promedio entre valores consecutivos."""
    distancias_sucesivas = [abs(valores[i+1] - valores[i]) for i in range(len(valores) - 1)]
    
    promedio = sum(distancias_sucesivas) / len(distancias_sucesivas)
    esperado = 1 / math.sqrt(12)  # Valor esperado de la distancia promedio
    diferencia= abs(promedio - esperado)
    
    return promedio, esperado, diferencia

# Configuración de generadores (cumplen periodo completo)
gen_vehiculos = GeneradorMixto(a=501, c=547, m=1000, x0=827)
gen_reportes = GeneradorMixto(a=5001, c=4607, m=10000, x0=4049)

for _ in range(100):
    print(gen_reportes.aleatorio())