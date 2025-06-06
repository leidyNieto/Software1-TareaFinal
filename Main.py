from datetime import datetime
from APIConvertidor import APIConvertidor
from controlador.ControlRegistro import ControlRegistro
from modelos.Enums import MetodoPago, TipoGasto, TipoViaje
from modelos.Viaje import Viaje
from repositorio.Repositorio import Repositorio

# Función genérica para mostrar enums
def seleccionar_enum(enum_class, mensaje):
    print(mensaje)
    for i, item in enumerate(enum_class, start=1):
        print(f"{i}. {item.name} ({item.value})")
    seleccion = int(input("Seleccione una opción: "))
    return list(enum_class)[seleccion - 1]

# Inicializar componentes
repositorio = Repositorio()
api_convertidor = APIConvertidor()
controlador = ControlRegistro(repositorio, api_convertidor)

# Variable para almacenar el viaje activo
viaje = None

# Menú principal
while True:
    print("\n=== Menú Principal ===")
    print("1. Crear nuevo viaje")
    print("2. Registrar gasto")
    print("0. Salir")
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        print("\n=== Crear nuevo viaje ===")
        try:
            fecha_inicio = datetime.strptime(input("Fecha de inicio (YYYY-MM-DD): "), "%Y-%m-%d").date()
            fecha_fin = datetime.strptime(input("Fecha de fin (YYYY-MM-DD): "), "%Y-%m-%d").date()
            presupuesto = float(input("Presupuesto diario (COP): "))
            tipo_viaje = seleccionar_enum(TipoViaje, "Seleccione el tipo de viaje:")

            viaje = Viaje(fecha_inicio, fecha_fin, presupuesto, tipo_viaje)
            viaje_id = repositorio.guardar_viaje(viaje)
            if viaje_id != -1:
                print("✅ Viaje guardado exitosamente ")
            else:
                print("❌ Error al guardar el viaje.")
        except Exception as e:
            print(f"❌ Error al crear el viaje: {e}")

    elif opcion == "2":
        print("\n=== Registrar gasto ===")
        viajes_disponibles = repositorio.cargar_viajes()
        if not viajes_disponibles:
            print("⚠️ No hay viajes registrados. Cree uno primero.")
            continue
        print("Seleccione un viaje:")
        for i, v in enumerate(viajes_disponibles, start=1):
            print(f"{i}. {v.tipo_viaje.name} | {v.fecha_inicio} → {v.fecha_fin} | Presupuesto: {v.presupuesto_diario} COP")

        try:
            seleccion = int(input("Opción: "))
            if seleccion < 1 or seleccion > len(viajes_disponibles):
                print("❌ Selección inválida.")
                continue
            viaje = viajes_disponibles[seleccion - 1]
            
        except ValueError:
            print("❌ Debe ingresar un número.")
            continue
        try:
            fecha_gasto = datetime.strptime(input("Fecha del gasto (YYYY-MM-DD): "), "%Y-%m-%d").date()        
            valor = float(input("Valor del gasto: "))
            moneda = input("Moneda del gasto (ej: USD, COP): ").strip().upper()
            metodo_pago = seleccionar_enum(MetodoPago, "Seleccione el método de pago:")
            tipo_gasto = seleccionar_enum(TipoGasto, "Seleccione el tipo de gasto:")

            resultado = controlador.registrar_gasto(
                viaje=viaje,
                fecha=fecha_gasto,
                valor=valor,
                moneda=moneda,
                metodo_pago=metodo_pago,
                tipo_gasto=tipo_gasto
            )

            print("\n✅ Gasto registrado exitosamente:")
            print(f"💰 Valor en COP: {resultado['valor_en_cop']}")
            print(f"📊 Diferencia con presupuesto diario: {resultado['diferencia']}")

        except Exception as e:
            print(f"❌ Error al registrar el gasto: {e}")
            continue

    elif opcion == "0":
        print("👋 Saliendo del programa...")
        break

    else:
        print("❌ Opción no válida. Intente de nuevo.")
