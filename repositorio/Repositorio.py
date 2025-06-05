import os
from dotenv import load_dotenv
import mysql.connector
from datetime import date
from typing import List
from modelos.Enums import TipoViaje, MetodoPago, TipoGasto
from modelos.Gastos import Gastos
from modelos.Viaje import Viaje

class Repositorio:
    def __init__(self):
        load_dotenv()
        self.config = {
            'host': os.getenv("MYSQL_HOST"),
            'user': os.getenv("MYSQL_USER"),
            'password': os.getenv("MYSQL_PASSWORD"),
            'database': os.getenv("MYSQL_DATABASE")
        }

    def cargar_viajes(self) -> List[Viaje]:
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
