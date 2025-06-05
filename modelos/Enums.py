from enum import Enum
class TipoViaje(Enum):
    """
    Enumeración que representa los tipos de viaje posibles.
    """
    NACIONAL = "NACIONAL"
    INTERNACIONAL = "INTERNACIONAL"

class MetodoPago(Enum):
    EFECTIVO = "Efectivo"
    TARJETA = "Tarjeta"

class TipoGasto(Enum):
    ALOJAMIENTO = "Alojamiento"
    TRANSPORTE = "Transporte"
    ALIMENTACION = "Alimentación"
    ENTRETENIMIENTO = "Entretenimiento"
    COMPRAS = "Compras"
