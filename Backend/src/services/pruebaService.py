# -----------------------------------------------------------------------
# PRUEBAS
# -----------------------------------------------------------------------
from Backend.src.services.flightService import FlightService
from Backend.src.models.flight import Flight
 
service = FlightService()

# Cargar desde JSON y luego operar normalmente
service.load_from_json("Backend/json/ModoInserción.json")
service.tree.print_tree()
 
print("=" * 40)
print("TEST 1 — CREATE: crear vuelos")
print("=" * 40)
 
f1 = Flight("SB470", "Medellin",    "Cartagena", "10:00", 400, 120, False, False)
f2 = Flight("SB472", "Bogota",      "Cali",      "08:00", 350,  90, True,  False)
f3 = Flight("SB469", "Barranquilla","Bogota",    "12:00", 420, 110, False, True)
 
service.create_flight(f1)
service.create_flight(f2)
service.create_flight(f3)
 
print("\n--- AVL despues de crear ---")
service.tree.print_tree()
print(f"Total vuelos: {service.tree.treeWeight()}")
print(f"Altura:       {service.tree.heightTree()}")
print(f"Balance raiz: {service.tree.getBalanceFactor(service.tree.root)}")
 
 
print("\n" + "=" * 40)
print("TEST 2 — FIND: buscar vuelos")
print("=" * 40)
 
encontrado = service.find_flight("SB470")
print(f"Buscar SB470 -> {'encontrado: ' + str(encontrado) if encontrado else 'NO encontrado'}")
 
no_existe = service.find_flight("SB999")
print(f"Buscar SB999 -> {'encontrado' if no_existe else 'NO encontrado (esperado)'}")
 
 
print("\n" + "=" * 40)
print("TEST 3 — UPDATE: actualizar SB470")
print("=" * 40)
 
print(f"Precio antes: {service.find_flight('SB470').precioBase}")
service.update_flight("SB470", {"precioBase": 500, "origen": "Leticia"})
f = service.find_flight("SB470")
print(f"Precio despues: {f.precioBase}  |  Origen despues: {f.origen}")
 
print("\nActualizar vuelo que no existe:")
service.update_flight("SB999", {"precioBase": 1})
 
 
print("\n" + "=" * 40)
print("TEST 4 — UNDO: deshacer actualizacion")
print("=" * 40)
 
service.undo()
print(f"Precio tras undo: {service.find_flight('SB470').precioBase}")
print("(Nota: si el precio sigue en 999 es el bug conocido de undo+update)")
 
 
print("\n" + "=" * 40)
print("TEST 5 — DELETE: eliminar SB470")
print("=" * 40)
 
service.delete_flight("SB470")
print(f"Buscar SB470 tras eliminar -> {'encontrado' if service.find_flight('SB470') else 'NO encontrado (esperado)'}")
print(f"SB470 sigue existiendo     -> {'si (esperado)' if service.find_flight('SB470') else 'NO (error)'}")
 
print("\n--- AVL despues de eliminar SB300 ---")
service.tree.print_tree()

print("Rotaciones:", service.tree.rotations)
 
 
print("\n" + "=" * 40)
print("TEST 6 — UNDO: deshacer eliminacion de SB472")
print("=" * 40)
 
service.undo()
print(f"Buscar SB472 tras undo -> {'encontrado (esperado)' if service.find_flight('SB472') else 'NO encontrado (error)'}")
 
 
print("\n" + "=" * 40)
print("TEST 7 — CANCEL: cancelar SB470 y su subarbol")
print("=" * 40)
 
print("Arbol antes de cancelar:")
service.tree.print_tree()
service.cancel_flight("SB470")
print("Arbol despues de cancelar SB470:")
service.tree.print_tree()
print(f"SB470 -> {'encontrado (error)' if service.find_flight('SB470') else 'NO encontrado (esperado)'}")
 
 
print("\n" + "=" * 40)
print("TEST 8 — UNDO: deshacer cancel")
print("=" * 40)
 
service.undo()
print("Arbol tras undo del cancel:")
service.tree.print_tree()
 
 
print("\n" + "=" * 40)
print("TEST 9 — UNDO sin historial")
print("=" * 40)
 
while service.history.stack:
    service.undo()
print("Llamando undo con historial vacio (no debe explotar):")
service.undo()
print("OK — no lanzo excepcion")
 
 
print("\n" + "=" * 40)
print("TODOS LOS TESTS COMPLETADOS")
print("=" * 40)
 