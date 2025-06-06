from datetime import date

from APIConvertidor import APIConvertidor
from modelos.Enums import TipoViaje


class Viaje:
    """
    Clase que representa un viaje con fecha de inicio y fin, presupuesto diario y tipo de viaje.
    """

    def __init__(self, fecha_inicio: date, fecha_fin: date, presupuesto_diario: float, tipo_viaje: TipoViaje):
        """
        Constructor de la clase Viaje.

        :param fecha_inicio: Fecha en la que inicia el viaje.
        :param fecha_fin: Fecha en la que finaliza el viaje.
        :param presupuesto_diario: Presupuesto diario destinado para el viaje.
        :param tipo_viaje: Tipo de viaje (objeto de la clase TipoViaje).
        """
        self._id = None  # ID del viaje, se asignará al guardar en la base de datos
        self._fecha_inicio = fecha_inicio
        self._fecha_fin = fecha_fin
        self._presupuesto_diario = presupuesto_diario
        self._tipo_viaje = tipo_viaje

    @property
    def id(self) -> int:
        """Devuelve el ID del viaje."""
        return self._id

    @id.setter
    def id(self, value: int):
        """Establece el ID del viaje."""
        self._id = value
        
    @property
    def fecha_inicio(self) -> date:
        """Devuelve la fecha de inicio del viaje."""
        return self._fecha_inicio

    @fecha_inicio.setter
    def fecha_inicio(self, value: date):
        """Establece la fecha de inicio del viaje."""
        self._fecha_inicio = value

    @property
    def fecha_fin(self) -> date:
        """Devuelve la fecha de fin del viaje."""
        return self._fecha_fin

    @fecha_fin.setter
    def fecha_fin(self, value: date):
        """Establece la fecha de fin del viaje."""
        self._fecha_fin = value

    @property
    def presupuesto_diario(self) -> float:
        """Devuelve el presupuesto diario del viaje."""
        return self._presupuesto_diario

    @presupuesto_diario.setter
    def presupuesto_diario(self, value: float):
        """Establece el presupuesto diario del viaje."""
        self._presupuesto_diario = value

    @property
    def tipo_viaje(self) -> TipoViaje:
        """Devuelve el tipo de viaje."""
        return self._tipo_viaje

    @tipo_viaje.setter
    def tipo_viaje(self, value: TipoViaje):
        """Establece el tipo de viaje."""
        self._tipo_viaje = value

    def __str__(self):
        return f"{self.tipo_viaje.value}: {self.fecha_inicio} -> {self.fecha_fin}, ${self.presupuesto_diario}"
    
    def verificarviaje_activo(self,fecha:date) -> bool:
        """
        Verifica si el viaje está activo comparando la fecha  con las fechas de inicio y fin.
        """
        return self.fecha_inicio <= fecha <= self.fecha_fin
    
    def validar_tipo_viaje(self)-> bool:
        if not isinstance(self.tipo_viaje, TipoViaje):
            raise ValueError
        return self.tipo_viaje == TipoViaje.INTERNACIONAL
    
    def ya_termino(self) -> bool:
        return date.today() > self.fecha_fin