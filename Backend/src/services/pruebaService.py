# -----------------------------------------------------------------------
# PRUEBAS
# -----------------------------------------------------------------------
from services.flightService import FlightService
from models.flight import Flight

service = FlightService()

# Cargar desde JSON
service.load_from_json("Backend/json/ModoInserción.json")

print("\nÁrbol inicial:")
service.tree.print_tree()

# -----------------------------------------------------------------------
print("\n" + "=" * 40)
print("TEST 1 — CREATE NORMAL (con balanceo)")
print("=" * 40)

f1 = Flight("SB470", "Medellin", "Cartagena", "10:00", 400, 120, False, False)
f2 = Flight("SB472", "Bogota", "Cali", "08:00", 350, 90, True, False)
f3 = Flight("SB469", "Barranquilla", "Bogota", "12:00", 420, 110, False, True)

service.create_flight(f1)
service.create_flight(f2)
service.create_flight(f3)

print("\n--- AVL balanceado ---")
service.tree.print_tree()
print("Rotaciones:", service.tree.rotations)

# -----------------------------------------------------------------------
print("\n" + "=" * 40)
print("TEST 2 — MODO ESTRÉS (SIN BALANCEO)")
print("=" * 40)

service.tree.enable_stress_mode()

# Insertar en orden para forzar degeneración
stress_flights = [
    Flight("SB800", "A", "B", "10:00", 100, 10, False, False),
    Flight("SB810", "A", "B", "10:00", 100, 10, False, False),
    Flight("SB820", "A", "B", "10:00", 100, 10, False, False),
    Flight("SB830", "A", "B", "10:00", 100, 10, False, False),
]

for f in stress_flights:
    service.create_flight(f)

print("\n--- Árbol en modo estrés (deformado) ---")
service.tree.print_tree()

print(f"Altura (debería aumentar): {service.tree.heightTree()}")

# -----------------------------------------------------------------------
print("\n" + "=" * 40)
print("TEST 3 — REBALANCEO GLOBAL")
print("=" * 40)

cost = service.tree.rebalance_all()

print("\n--- Árbol después de rebalanceo global ---")
service.tree.print_tree()

print("\nCosto del rebalanceo:")
print(cost)

print(f"Altura después: {service.tree.heightTree()}")
print(f"Balance raíz: {service.tree.getBalanceFactor(service.tree.root)}")

# -----------------------------------------------------------------------
print("\n" + "=" * 40)
print("TEST 4 — MÉTRICAS")
print("=" * 40)

print(f"Hojas: {service.tree.countLeaves()}")
print(f"Cancelaciones masivas: {service.mass_cancellations}")
print(f"Rotaciones acumuladas: {service.tree.rotations}")

# -----------------------------------------------------------------------
print("\n" + "=" * 40)
print("TEST 5 — CANCELACIÓN MASIVA + UNDO")
print("=" * 40)

print("\nÁrbol antes de cancelar:")
service.tree.print_tree()

service.cancel_flight("SB470")

print("\nÁrbol después de cancelar:")
service.tree.print_tree()

print(f"Cancelaciones masivas: {service.mass_cancellations}")

print("\nUNDO cancelación:")
service.undo()
service.tree.print_tree()

# -----------------------------------------------------------------------
print("\n" + "=" * 40)
print("TEST 6 — UNDO TOTAL")
print("=" * 40)

while service.history.stack:
    service.undo()

print("Árbol final tras undo total:")
service.tree.print_tree()

print("\nOK — pruebas completadas")