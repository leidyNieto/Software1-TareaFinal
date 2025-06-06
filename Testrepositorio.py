from datetime import date
import unittest
from unittest.mock import Mock, patch
from modelos.Enums import MetodoPago, TipoGasto, TipoViaje
from modelos.Gastos import Gastos
from modelos.Viaje import Viaje
from repositorio.Repositorio import Repositorio


class Testrepositorio(unittest.TestCase):

    @patch("mysql.connector.connect")
    def test_guardar_gasto(self, mock_connect):
        # Mocks internos de la conexión y cursor
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.is_connected.return_value = True

        # Crear objetos de prueba
        viaje = Viaje(date(2025, 6, 1), date(2025, 6, 10), 150000, TipoViaje.NACIONAL)
        viaje.id = 1

        gasto = Gastos(
            fecha=date(2025, 6, 2),
            valor_origen=30000,
            moneda="COP",
            metodo_pago=MetodoPago.TARJETA,
            tipo_gasto=TipoGasto.TRANSPORTE,
            valor_peso=30000
        )

        repo = Repositorio()
        repo.guardar_gasto(viaje, gasto)

        # ✅ Verificar que se llamó a connect
        mock_connect.assert_called_once()

        # ✅ Verificar que se ejecutó el query con datos correctos
        mock_cursor.execute.assert_called_once()
        args = mock_cursor.execute.call_args[0]
        query = args[0]
        valores = args[1]

        self.assertIn("INSERT INTO gastos", query)
        self.assertEqual(valores, (
            1,
            gasto.fecha,
            gasto.valor_origen,
            gasto.moneda,
            gasto.valor_peso,
            gasto.metodo_pago.name,
            gasto.tipo_gasto.name
        ))

        # ✅ Verificar commit y cierre
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()