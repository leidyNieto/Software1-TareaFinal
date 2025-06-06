import os
from dotenv import load_dotenv
import mysql.connector
from datetime import date
from typing import List
from modelos.Enums import TipoViaje, MetodoPago, TipoGasto
from modelos.Gastos import Gastos
from modelos.Viaje import Viaje

class Repositorio:
    """
    Clase encargada de manejar la conexión con la base de datos MySQL
    y realizar operaciones de lectura y escritura relacionadas con viajes y gastos.
    """
    def __init__(self):
        """
        Inicializa la configuración de la base de datos cargando las variables de entorno.
        """
        load_dotenv()
        self.config = {
            'host': os.getenv("MYSQL_HOST"),
            'user': os.getenv("MYSQL_USER"),
            'password': os.getenv("MYSQL_PASSWORD"),
            'database': os.getenv("MYSQL_DATABASE")
        }

    def cargar_viajes(self) -> List[Viaje]:
        """
        Obtiene todos los viajes registrados en la base de datos.

        Returns:
            List[Viaje]: Lista de objetos Viaje recuperados de la tabla `viajes`.
        """
        viajes = []
        try:
            conexion = mysql.connector.connect(**self.config)
            cursor = conexion.cursor()

            query = "SELECT id, tipo, fecha_inicio, fecha_fin, presupuesto_diario FROM viajes"
            cursor.execute(query)

            for row in cursor.fetchall():
                id_viaje = row[0]
                tipo = TipoViaje[row[1].upper()]
                fecha_inicio = row[2]
                fecha_fin = row[3]
                presupuesto_diario = float(row[4])
                viaje = Viaje(fecha_inicio, fecha_fin, presupuesto_diario, tipo)
                viaje.id = id_viaje  # Por si necesitas mantener el id
                viajes.append(viaje)

        except mysql.connector.Error as err:
            print(f"Error en conexión/consulta: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conexion' in locals() and conexion.is_connected():
                conexion.close()

        return viajes

    def guardar_gasto(self, viaje: Viaje, gasto: Gastos):
        """
        Guarda un gasto asociado a un viaje en la base de datos.

        Args:
            viaje (Viaje): Objeto Viaje al que pertenece el gasto.
            gasto (Gastos): Objeto Gastos que contiene los datos del gasto a guardar.
        """
        try:
            conexion = mysql.connector.connect(**self.config)
            cursor = conexion.cursor()

            query = """
                INSERT INTO gastos (viaje_id,fecha, valor_original, moneda, valor_convertido, tipo_pago, tipo_gasto)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            datos = (
                viaje.id,
                gasto.fecha,
                gasto.valor_origen,
                gasto.moneda,
                gasto.valor_peso,
                gasto.metodo_pago.name,
                gasto.tipo_gasto.name,
                
            )
            cursor.execute(query, datos)
            conexion.commit()
        except mysql.connector.Error as err:
            print(f"Error al guardar gasto: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conexion' in locals() and conexion.is_connected():
                conexion.close()
    
    def guardar_viaje(self, viaje: Viaje):
        """
        Guarda un nuevo viaje en la base de datos.
        Args:
            viaje (Viaje): Objeto Viaje que contiene los datos del viaje a guardar.
        Nota:
            El atributo `id` del objeto `viaje` será actualizado con el ID generado automáticamente por la base de datos.
        """
        try:
            conexion = mysql.connector.connect(**self.config)
            cursor = conexion.cursor()

            query = """
                INSERT INTO viajes (tipo, fecha_inicio, fecha_fin, presupuesto_diario)
                VALUES (%s, %s, %s, %s)
            """
            datos = (
                viaje.tipo_viaje.name,
                viaje.fecha_inicio,
                viaje.fecha_fin,
                viaje.presupuesto_diario
            )
            cursor.execute(query, datos)
            conexion.commit()
            viaje.id = cursor.lastrowid  # Asignar el ID generado al objeto viaje
        except mysql.connector.Error as err:
            print(f"Error al guardar viaje: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conexion' in locals() and conexion.is_connected():
                conexion.close()

    def obtener_gastos_por_viaje(self, viaje: Viaje):
        """
        Recupera todos los gastos asociados a un viaje específico.
        Args:
            viaje (Viaje): Objeto Viaje del cual se quieren obtener los gastos.
        Returns:
            List[dict]: Lista de diccionarios con la información de cada gasto, ordenados por fecha.
        """
        gastos = []
        try:
            conexion = mysql.connector.connect(**self.config)
            cursor = conexion.cursor()

            query = """
            SELECT fecha, valor_original, moneda, valor_convertido, tipo_pago, tipo_gasto
            FROM gastos
            WHERE viaje_id = %s
            ORDER BY fecha
            """
            cursor.execute(query, (viaje.id,))

            for row in cursor.fetchall():
                gasto = {
                    'fecha': row[0],
                    'valor_original': float(row[1]),
                    'moneda': row[2],
                    'valor_peso': float(row[3]),
                    'metodo_pago': row[4].upper(), 
                    'tipo_gasto': row[5].upper()
            }
                gastos.append(gasto)

        except mysql.connector.Error as err:
            print(f"Error al obtener gastos: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conexion' in locals() and conexion.is_connected():
                conexion.close()
        return gastos
