def formatear_clima(data: dict) -> str:
    """Formatea el clima actual en texto legible."""
    if "error" in data:
        return f"Error: {data['error']}"

    return f"Temperatura: {data['temperature']}°C | Viento: {data['windspeed']} km/h"


def formatear_pronostico(data: dict) -> str:
    """Formatea el pronóstico diario en una tabla de texto."""
    if "error" in data:
        return f"Error: {data['error']}"

    salida = "\n=== Pronóstico de 7 días ===\n"
    fechas = data["time"]
    maxs = data["temperature_2m_max"]
    mins = data["temperature_2m_min"]
    lluvias = data["precipitation_probability_max"]

    for i in range(len(fechas)):
        salida += f"{fechas[i]} -> Min: {mins[i]}°C | Max: {maxs[i]}°C | Lluvia: {lluvias[i]}%\n"

    return salida
