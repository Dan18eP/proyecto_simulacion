from eventos import evento_incidente

# Probar 100 generaciones
conteo_a1 = 0
conteo_a2 = 0

for _ in range(100):
    inc = evento_incidente()
    if inc["zona"] == "A1":
        conteo_a1 += 1
    else:
        conteo_a2 += 1

print(f"A1: {conteo_a1} incidentes")
print(f"A2: {conteo_a2} incidentes")
print(f"Proporción A1/A2: {conteo_a1/conteo_a2:.2f}")