from datetime import date
from modelos.Enums import MetodoPago, TipoGasto

class Gastos:
    def __init__(self, fecha: date, valor_origen: float, moneda: str,valor_peso: float,
                 metodo_pago: MetodoPago, tipo_gasto: TipoGasto):
        self.fecha = fecha
        self.valor_origen = valor_origen
        self.moneda = moneda
        self.valor_peso = valor_peso
        self.metodo_pago = metodo_pago
        self.tipo_gasto = tipo_gasto
        