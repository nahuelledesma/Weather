from clima.utils import formatear_clima, formatear_pronostico

def mostrar_reporte(ciudad, clima, pronostico):
    print("\n=== REPORTE DE CLIMA ===")
    print(f"Ciudad: {ciudad}")
    print(formatear_clima(clima))
    print(formatear_pronostico(pronostico))
