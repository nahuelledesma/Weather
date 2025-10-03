import requests

def buscar_ciudad(nombre: str):
    """
    Busca coincidencias de una ciudad usando la API de geocoding de Open-Meteo.
    Devuelve una lista de diccionarios únicos con 'name', 'country', 'state', 'lat', 'lon'.
    """
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={nombre}&count=10"
    respuesta = requests.get(url).json()

    if "results" not in respuesta:
        return []

    resultados = []
    seen = set()
    for r in respuesta["results"]:
        ciudad = r.get("name", "")
        pais = r.get("country", "")
        estado = r.get("admin1", "")
        lat = r.get("latitude")
        lon = r.get("longitude")

        # ignorar entradas sin lat/lon
        if lat is None or lon is None:
            continue

        key = (ciudad, estado, pais)
        if key not in seen:
            resultados.append({
                "name": ciudad,
                "country": pais,
                "state": estado,
                "lat": lat,
                "lon": lon
            })
            seen.add(key)
    return resultados




def seleccionar_ciudad():
    """
    Pide al usuario que ingrese una ciudad y selecciona la correcta si hay varias coincidencias.
    Devuelve latitud, longitud, nombre completo y país.
    """
    nombre = input("Ingrese el nombre de la ciudad: ")
    coincidencias = buscar_ciudad(nombre)

    if not coincidencias:
        print("No se encontraron ciudades con ese nombre.")
        return None

    # Si hay más de una coincidencia, mostrar opciones
    if len(coincidencias) == 1:
        seleccion = 0
    else:
        print("\nSe encontraron varias coincidencias:")
        for i, c in enumerate(coincidencias):
            estado = f", {c['state']}" if c['state'] else ""
            print(f"{i+1}) {c['name']}{estado}, {c['country']}")
        while True:
            try:
                seleccion = int(input(f"Seleccione la ciudad (1-{len(coincidencias)}): ")) - 1
                if 0 <= seleccion < len(coincidencias):
                    break
            except ValueError:
                pass
            print("Opción inválida. Intente nuevamente.")

    ciudad_elegida = coincidencias[seleccion]
    return ciudad_elegida["lat"], ciudad_elegida["lon"], ciudad_elegida["name"], ciudad_elegida["country"]


def obtener_clima_actual_latlon(lat, lon):
    """
    Devuelve el clima actual de una ubicación especificada por latitud y longitud.
    """
    url_clima = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    respuesta = requests.get(url_clima).json()
    return respuesta.get("current_weather", {})


def obtener_pronostico_latlon(lat, lon):
    """
    Devuelve el pronóstico diario de una ubicación especificada por latitud y longitud.
    """
    url_pronostico = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max"
        f"&timezone=auto"
    )
    respuesta = requests.get(url_pronostico).json()
    return respuesta.get("daily", {})

import requests

def obtener_pronostico_horario(lat, lon):
    """
    Devuelve el pronóstico horario del día actual para la latitud y longitud dadas.
    Retorna un diccionario con 'time' y 'temperature_2m' para las horas del día.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m",
        "timezone": "auto"
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    data = r.json()
    
    # Solo devolver las horas del día actual
    from datetime import datetime
    hoy = datetime.now().strftime("%Y-%m-%d")
    horas = []
    temperaturas = []
    for t, temp in zip(data["hourly"]["time"], data["hourly"]["temperature_2m"]):
        if t.startswith(hoy):
            horas.append(t)
            temperaturas.append(temp)
    return {"time": horas, "temperature_2m": temperaturas}
