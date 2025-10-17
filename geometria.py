import math

class Area:
    def __init__(self, nombre, tipo, parametros):
        self.nombre = str(nombre)
        self.tipo = tipo
        self.parametros = parametros

    def contiene(self, x, y):
        """Verifica si un punto (x,y) está dentro del área."""
        #A1: Triángulo
        if self.tipo == "triangulo":
            vertices = self.parametros.get("vertices")
            if vertices and len(vertices) == 3:
                return self._punto_en_triangulo(x, y, vertices)
            return False

        #A2: Semicírculo
        elif self.tipo == "semicirculo":
            cx, cy = self.parametros.get("centro")
            r = self.parametros.get("radio")
            distancia = math.sqrt((x - cx)**2 + (y - cy)**2)
            # Semicírculo con apertura hacia abajo: y <= cy
            return distancia <= r and y <= cy
        #A3: Rectángulo (CAI)
        elif self.tipo == "rectangulo":
            x_min = self.parametros.get("x_min")
            x_max = self.parametros.get("x_max")
            y_min = self.parametros.get("y_min")
            y_max = self.parametros.get("y_max")
            return x_min <= x <= x_max and y_min <= y <= y_max

        return False

    def _punto_en_triangulo(self, px, py, vertices):
        """
        Verifica si un punto (px, py) está dentro de un triángulo.
        Usa el método de áreas (coordenadas baricéntricas).
        """
        x1, y1 = vertices[0]
        x2, y2 = vertices[1]
        x3, y3 = vertices[2]

        def area_triangulo(ax, ay, bx, by, cx, cy):
            return abs((ax*(by-cy) + bx*(cy-ay) + cx*(ay-by)) / 2.0)

        area_total = area_triangulo(x1, y1, x2, y2, x3, y3)
        area1 = area_triangulo(px, py, x2, y2, x3, y3)
        area2 = area_triangulo(x1, y1, px, py, x3, y3)
        area3 = area_triangulo(x1, y1, x2, y2, px, py)

        return abs(area_total - (area1 + area2 + area3)) < 0.01


# SISTEMA DE COORDENADAS
# Origen (0, 0) en esquina inferior izquierda del mapa completo
# X: 0 a 65 km (horizontal)
# Y: -12.5 a 100 km (vertical, incluyendo sobresalientes)

# Alturas de referencia:
# - Base de A2: y = -12.5 (sobresale hacia abajo)
# - EP2 y borde inferior del rectángulo: y = 10
# - P2 (centro de A2): y = 10
# - P1 (base de A1): y = 50
# - Pico de A1: y = 90 (P1 + 40 km)
# - EP1: y = 90

# Posiciones horizontales:
# - Borde izquierdo: x = 0
# - Inicio del rectángulo A3: x = 20
# - Centro (P1, P2, CAI alineados): x = 32.5
# - Final del rectángulo A3: x = 45
# - Borde derecho: x = 65

#ÁREA A1 (TRIÁNGULO) - Sobresale 40 km arriba
#Base del triángulo en y = 50 (nivel de P1), Ancho de base: 4.5 + 4.5 = 9 km, Altura: 40 km hacia arriba, Pico en y = 90

A1 = Area("A1", "triangulo", {
    "vertices": [
        (28.0, 50.0),   # Vértice inferior izquierdo (32.5 - 4.5)
        (37.0, 50.0),   # Vértice inferior derecho (32.5 + 4.5)
        (32.5, 90.0)    # Vértice superior (pico)
    ]
})


# ÁREA A2 (SEMICÍRCULO) - Sobresale 12.5 km abajo
#Centro en P2: (32.5, 10), Radio: 12.5 km, La parte más baja llega a y = 10 - 12.5 = -2.5, Apertura hacia abajo (sur)

A2 = Area("A2", "semicirculo", {
    "centro": (32.5, 10.0),
    "radio": 12.5
})


# ÁREA A3 (RECTÁNGULO CENTRAL)
# Dimensiones:Ancho: 25 km (desde x=20 hasta x=45) Alto: 40 km (desde y=10 hasta y=50)

A3 = Area("A3", "rectangulo", {
    "x_min": 20.0,
    "x_max": 45.0,
    "y_min": 10.0,
    "y_max": 50.0
})

# ESTACIONES Y PUNTOS CLAVE: EP1= Esquina superior izquierda (al nivel del pico de A1)
EP1 = {
    "nombre": "EP1",
    "coordenadas": (0.0, 90.0)  # Alineado con el pico de A1
}

# EP2: Esquina inferior derecha
EP2 = {
    "nombre": "EP2",
    "coordenadas": (65.0, 10.0)
}

# CAI (Centro de Operaciones): Centro exacto del rectángulo A3
CO = {
    "nombre": "Centro de Operaciones (CAI)",
    "coordenadas": (32.5, 30.0)  # Centro de A3
}

# Puntos de referencia (intersecciones)
P1 = {
    "nombre": "P1",
    "coordenadas": (32.5, 50.0)  # Base del triángulo A1
}

P2 = {
    "nombre": "P2", 
    "coordenadas": (32.5, 10.0)  # Centro del semicírculo A2
}

# LÍMITES DEL MAPA COMPLETO
MAPA_LIMITES = {
    "x_min": 0.0,
    "x_max": 65.0,
    "y_min": -2.5,    # Parte más baja de A2 (10 - 12.5)
    "y_max": 90.0     # Pico de A1 (50 + 40)
}

# RUTAS DE PATRULLA
RUTAS = {
    "vehiculo_1": {
        "nombre": "Vehículo 1",
        "rutas": [
            "suroccidente-noroccidente",  # Lado izquierdo vertical
            "noroccidente-nororiente"     # Lado superior horizontal
        ],
        "puntos_clave": [
            (5.0, 10.0),   # Suroccidente
            (5.0, 90.0),   # Noroccidente
            (32.5, 90.0),  # Nororiente (centro superior)
        ]
    },
    "vehiculo_2": {
        "nombre": "Vehículo 2",
        "rutas": [
            "suroccidente-suroriente",    # Lado inferior horizontal
            "suroriente-nororiente"       # Lado derecho vertical
        ],
        "puntos_clave": [
            (5.0, 10.0),   # Suroccidente
            (60.0, 10.0),  # Suroriente
            (60.0, 90.0),  # Nororiente (derecha superior)
        ]
    },
    "vehiculo_3": {
        "nombre": "Vehículo 3",
        "rutas": [
            "circular_cai"                # Patrulla alrededor del CAI
        ],
        "puntos_clave": [
            (32.5, 30.0),  # Centro (CAI)
            (32.5, 50.0),  # Arriba del CAI
            (45.0, 30.0),  # Derecha del CAI
            (32.5, 10.0),  # Abajo del CAI
            (20.0, 30.0),  # Izquierda del CAI
        ]
    }
}

# FUNCIÓN DE VERIFICACIÓN


def verificar_geometria():
    """Prueba la geometría definida con puntos conocidos."""

    print("VERIFICACIÓN DE GEOMETRÍA - SISTEMA DE SEGURIDAD UBER")

    print(f"\nLímites del mapa:")
    print(f"  X: {MAPA_LIMITES['x_min']} a {MAPA_LIMITES['x_max']} km")
    print(f"  Y: {MAPA_LIMITES['y_min']} a {MAPA_LIMITES['y_max']} km")
    print(f"  Dimensiones: {MAPA_LIMITES['x_max'] - MAPA_LIMITES['x_min']} × {MAPA_LIMITES['y_max'] - MAPA_LIMITES['y_min']} km")
    
    print(" ")
    print(" PUNTOS CLAVE DEL SISTEMA")

    
    puntos_sistema = [
        ("EP1", EP1["coordenadas"]),
        ("EP2", EP2["coordenadas"]),
        ("CAI (Centro Ops)", CO["coordenadas"]),
        ("P1 (base A1)", P1["coordenadas"]),
        ("P2 (centro A2)", P2["coordenadas"]),
    ]
    
    for nombre, (x, y) in puntos_sistema:
        print(f"  {nombre:20s}: ({x:5.1f}, {y:5.1f})")
    
    print(" ")
    print("PRUEBA DE CONTENCIÓN DE ÁREAS")

    
    puntos_prueba = [
        (32.5, 70.0, "Centro superior de A1"),
        (32.5, 85.0, "Cerca del pico de A1"),
        (32.5, 30.0, "Centro de A3 (CAI)"),
        (32.5, 5.0, "Dentro de A2 (semicírculo)"),
        (32.5, -1.0, "Parte baja de A2"),
        (10.0, 30.0, "Área no transitada (izquierda)"),
        (50.0, 30.0, "Área no transitada (derecha)"),
        (0.0, 90.0, "EP1"),
        (65.0, 10.0, "EP2"),
    ]
    
    print(f"\n{'Coordenadas':<15} {'Descripción':<30} {'Área(s)':<20}")
    print(" ")
    
    for x, y, descripcion in puntos_prueba:
        en_a1 = A1.contiene(x, y)
        en_a2 = A2.contiene(x, y)
        en_a3 = A3.contiene(x, y)
        
        areas = []
        if en_a1: areas.append("A1")
        if en_a2: areas.append("A2")
        if en_a3: areas.append("A3")
        
        resultado = ", ".join(areas) if areas else "Ninguna"
        print(f"({x:5.1f}, {y:6.1f})  {descripcion:<30} {resultado:<20}")
    
    print(" ")


if __name__ == "__main__":
    verificar_geometria()