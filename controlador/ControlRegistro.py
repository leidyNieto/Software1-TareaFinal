
from APIConvertidor import APIConvertidor
from modelos.Gastos import Gastos
from modelos.Viaje import Viaje
from modelos.Enums import MetodoPago, TipoGasto
from datetime import date

from repositorio.Repositorio import Repositorio
class ControlRegistro:
    def __init__(self, repositorio: Repositorio, api_convertidor: APIConvertidor):
        self.repositorio = repositorio
        self.api_convertidor = api_convertidor

    def registrar_gasto(self, viaje: Viaje, fecha: date, valor: float, moneda: str,
                        metodo_pago: MetodoPago, tipo_gasto: TipoGasto) -> dict:
        """
        Registra un gasto en un viaje. Convierte a COP si es internacional.
        Retorna información del gasto y diferencia con presupuesto.
        """
        if not viaje.verificarviaje_activo(fecha):
            raise ValueError("El viaje no está activo. No se puede registrar el gasto.")

        if viaje.validar_tipo_viaje() and moneda.upper() != "COP":
            valor_peso = self.api_convertidor.convertir(moneda.upper(), "COP", valor)
        else:
            valor_peso = valor

        gasto = Gastos(
            fecha=fecha,
            valor_origen=valor,
            moneda=moneda,
            valor_peso=valor_peso,
            metodo_pago=metodo_pago,
            tipo_gasto=tipo_gasto
            
        )
        self.repositorio.guardar_gasto(viaje, gasto)

        diferencia = viaje.presupuesto_diario - valor_peso
        return {
            "valor_en_cop": valor_peso,
            "presupuesto_diario": viaje.presupuesto_diario,
            "diferencia": diferencia
        }
