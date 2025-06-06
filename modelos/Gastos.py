from datetime import date
from modelos.Enums import MetodoPago, TipoGasto

class Gastos:
    def __init__(self, fecha: date, valor_origen: float, moneda: str,valor_peso: float,
                 metodo_pago: MetodoPago, tipo_gasto: TipoGasto):
        self._id = None
        self.fecha = fecha
        self.valor_origen = valor_origen
        self.moneda = moneda
        self.valor_peso = valor_peso
        self.metodo_pago = metodo_pago
        self.tipo_gasto = tipo_gasto

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value
    
    @staticmethod
    def agrupar_por_fecha(gastos: list):
        resultado = {}
        for g in gastos:
            fecha = g['fecha']
            metodo = g['metodo_pago']
            valor = g['valor_peso']

            if fecha not in resultado:
                resultado[fecha] = {'EFECTIVO': 0, 'TARJETA': 0, 'TOTAL': 0}

            resultado[fecha][metodo] += valor
            resultado[fecha]['TOTAL'] += valor

        return resultado

    @staticmethod
    def agrupar_por_tipo(gastos: list):
        resultado = {}
        for g in gastos:
            tipo = g['tipo_gasto']
            metodo = g['metodo_pago']
            valor = g['valor_peso']

            if tipo not in resultado:
                resultado[tipo] = {'EFECTIVO': 0, 'TARJETA': 0, 'TOTAL': 0}

            resultado[tipo][metodo] += valor
            resultado[tipo]['TOTAL'] += valor

        return resultado

