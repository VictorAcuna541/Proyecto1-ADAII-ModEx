
from types import SimpleNamespace
from greedy import modexV

# Creamos dos agentes de prueba
agents = [
    SimpleNamespace(
        opinion=10,
        receptivity=1.0,
        influence=1.0
    ),
    SimpleNamespace(
        opinion=5,
        receptivity=0.0,
        influence=1.0
    )
]

# Presupuesto disponible: 0
rs = SimpleNamespace(
    agents=agents,
    max_budget=0
)

# Ejecutamos el algoritmo voraz
E, effort, extremism = modexV(rs)

print("Resultado de la prueba:")
print("Agentes moderados:", E)
print("Presupuesto utilizado:", effort)
print("Extremismo final:", extremism)

# Verificamos los resultados esperados
assert E == [1, 0], "Error: selección incorrecta de agentes"
assert effort == 0, "Error: se consumió presupuesto"
assert abs(extremism - 2.5) < 0.000001, "Error: extremismo incorrecto"

print("\nPRUEBA SUPERADA: el esfuerzo cero funciona correctamente.")