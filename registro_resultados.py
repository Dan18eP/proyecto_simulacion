# ============================================================
# registro_resultados.py
# Registro de resultados de las pruebas de generadores en CSV
# ============================================================

import csv
from datetime import datetime


def guardar_resultados(
    nombre_generador,
    parametros,
    chi_cuadrado,
    frecuencias_observadas,
    promedio,
    esperado,
    diferencia,
    estado,
    archivo="resultados_generadores.csv"
):
    """
    Guarda los resultados de una prueba de generador mixto en un archivo CSV.

    Parámetros:
        nombre_generador (str): Nombre identificador del generador.
        parametros (dict): Diccionario con las constantes a, c, m, x0 y N.
        chi_cuadrado (float): Resultado de la prueba de frecuencia.
        frecuencias_observadas (list): Lista de frecuencias por intervalo.
        promedio (float): Distancia promedio observada.
        esperado (float): Valor esperado teórico de la distancia promedio.
        diferencia (float): Diferencia absoluta entre promedio y esperado.
        estado (str): Resultado de la prueba ('Aprobada' o 'Posible desviación').
        archivo (str): Nombre del archivo CSV donde se almacenarán los resultados.
    """

    encabezados = [
        "Fecha",
        "Generador",
        "a",
        "c",
        "m",
        "x0",
        "Chi²",
        "Frecuencias Observadas",
        "Distancia Promedio",
        "Distancia Esperada",
        "Diferencia",
        "Estado"
    ]

    fila = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        nombre_generador,
        parametros["a"],
        parametros["c"],
        parametros["m"],
        parametros["x0"],
        round(chi_cuadrado, 4),
        str(frecuencias_observadas),
        round(promedio, 4),
        round(esperado, 4),
        round(diferencia, 4),
        estado
    ]

    try:
        with open(archivo, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow(encabezados)
            writer.writerow(fila)
    except Exception as e:
        print(f"Error al guardar los resultados: {e}")
