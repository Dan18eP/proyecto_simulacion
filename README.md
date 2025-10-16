# Simulación de Sistema de Seguridad UBER

Este proyecto implementa una **simulación de respuesta a incidentes** por parte de vehículos de patrulla en un entorno urbano.  
El objetivo es modelar y analizar el comportamiento del sistema ante diferentes tasas de incidentes y configuraciones de vehículos.

---

## Estructura del Proyecto

proyecto_simulacion/
│
├── simulacion.py # Control principal de la simulación
├── resultados.py # Módulo encargado de mostrar métricas y estadísticas
├── eventos.py # Genera los eventos de incidentes, llegadas y patrullas
├── generadores.py # Contiene generadores aleatorios (ej. distribución de Poisson)
├── geometria.py # Define posiciones y límites del mapa
├── test_incidente.py #.Prueba que los incidentes se estén generando correctamente
├── pruebas_generadores.py # Asegura que los incidentes se estén generando correctamente con las diferentes pruebas definidas en generadores.py
└── README.md # Este archivo


## Descripción General

El programa simula incidentes reportados por usuarios, asignando a cada uno un vehículo de patrulla disponible que:
1. Se dirige al punto del incidente.  
2. Intenta contactar al usuario (60% de probabilidad de éxito).  
3. En caso exitoso, traslada al usuario a una estación de apoyo (EP1 o EP2).  

Durante la simulación se recopilan métricas como:
- Número total de incidentes.
- Porcentaje de éxito en los traslados.
- Distancia recorrida por cada vehículo.
- Casos fallidos (usuarios no encontrados o falta de vehículos).

---

## Ejecución

### 1. Requisitos
Asegúrate de tener **Python 3.8+** instalado.

### 2. Ejecutar la simulación
Desde la terminal o consola, en la carpeta del proyecto:

```
python simulacion.py
```

Esto iniciará la simulación y mostrará en consola los resultados finales.

## Parámetros de la Simulación
Los parámetros principales se pueden configurar en el constructor de la clase Simulacion (en simulacion.py):

  simulacion = Simulacion(
      duracion_simulacion=100,   # Duración total en unidades de tiempo
      intervalo=1.0,             # Intervalo por ciclo de simulación
      lambda_incidentes=0.5,     # Tasa promedio de incidentes (λ de Poisson)
      pausa_visual=False         # Pausa visual (True para animar en consola)
  )

---
## Resultados

El módulo resultados.py muestra al final del proceso:

  - Resumen general de incidentes.
  - Métricas por vehículo.
  - Porcentaje de usuarios no trasladados.
  - Distancia promedio recorrida.
  - Estadísticas adicionales (como distancia por incidente exitoso).

Autor
Daniel Echeverría

Proyecto académico para la simulación de sistemas de respuesta y optimización logística.

Licencia
Este proyecto se distribuye bajo la licencia MIT, lo que permite su uso libre para fines educativos y de investigación.
