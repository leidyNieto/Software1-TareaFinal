import os
from dotenv import load_dotenv
import requests

class APIConvertidor:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("EXCHANGE_API_KEY")
        self.base_url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/latest"

    """
    Realiza la conversión de una cantidad de dinero desde una moneda origen a una moneda destino
    utilizando la API de ExchangeRate.

    Parámetros:
    - moneda_origen: código ISO de la moneda de origen (por ejemplo, 'USD')
    - moneda_destino: código ISO de la moneda destino (por ejemplo, 'EUR')
    - valor: cantidad de dinero a convertir

    Retorna:
    - El valor convertido, redondeado a 2 decimales

    Lanza:
    - ValueError si ocurre un error en la consulta o si la moneda destino no está disponible
    """

    def convertir(self, moneda_origen: str, moneda_destino: str, valor: float) -> float:
        moneda_origen = moneda_origen.upper()
        moneda_destino = moneda_destino.upper()
        url = f"{self.base_url}/{moneda_origen}"
        response = requests.get(url)
        data = response.json()

        if data.get("result") == "success":
            tasa = data["conversion_rates"].get(moneda_destino)
            if tasa:
                return round(valor * tasa, 2) 
            else:
                raise ValueError(f"❌ No se encontró la tasa para {moneda_destino}")
        else:
            raise ValueError("❌ La API respondió sin éxito")
