from datetime import date
import unittest
from unittest.mock import Mock
from controlador.ControlRegistro import ControlRegistro
from modelos.Enums import MetodoPago, TipoGasto, TipoViaje
from modelos.Viaje import Viaje


class Testviajegastos (unittest.TestCase):
    def setUp(self):
        self.viaje_nacional = Viaje(date(2025, 6, 1), date(2025, 6, 10), 150000, TipoViaje.NACIONAL)
        self.viaje_nacional.id = 1  # ← importante para simular que está guardado

        self.viaje_internacional = Viaje(date(2025, 6, 1), date(2025, 6, 10), 150000, TipoViaje.INTERNACIONAL)
        self.viaje_internacional.id = 2

        self.repositorio_mock = Mock() 
        self.api_mock = Mock()         
        self.controlador = ControlRegistro(self.repositorio_mock, self.api_mock)

    def test_registrar_gasto_nacional(self):
        resultado = self.controlador.registrar_gasto(
        viaje=self.viaje_nacional,
        fecha=date(2025,6,2),
        valor=50000,
        moneda="COP",
        metodo_pago=MetodoPago.TARJETA,
        tipo_gasto=TipoGasto.TRANSPORTE
    )

         # Confirmar que NO se llamó a la API de conversión
        self.api_mock.convertir.assert_not_called()
        self.repositorio_mock.guardar_gasto.assert_called_once()        
        self.assertEqual(resultado['valor_en_cop'], 50000)
        self.assertEqual(resultado['diferencia'], 100000)

    def test_registrar_gasto_internacional_con_conversion(self):
        self.api_mock.convertir.return_value = 200000

        resultado = self.controlador.registrar_gasto(
            viaje=self.viaje_internacional,
            fecha=date(2025, 6, 5),
            valor=50,
            moneda="USD",
            metodo_pago=MetodoPago.EFECTIVO,
            tipo_gasto=TipoGasto.COMPRAS
        )

        self.api_mock.convertir.assert_called_once_with("USD", "COP", 50)
        self.repositorio_mock.guardar_gasto.assert_called_once()
        self.assertEqual(resultado['valor_en_cop'], 200000)
        self.assertEqual(resultado['diferencia'], -50000)

    def test_gasto_fuera_del_rango_de_viaje(self):
        with self.assertRaises(Exception) as context:
            self.controlador.registrar_gasto(
                viaje=self.viaje_nacional,
                fecha=date(2025, 5, 20),
                valor=30000,
                moneda="COP",
                metodo_pago=MetodoPago.EFECTIVO,
                tipo_gasto=TipoGasto.ALIMENTACION
            )
        self.assertIn("El viaje no está activo. No se puede registrar el gasto.", str(context.exception))
        
if __name__ == '__main__':
    unittest.main()
