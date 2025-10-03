import plotly.graph_objects as go

def graficar_pronostico(pronostico, ciudad):
    """
    Gráfico interactivo de 7 días:
    - Líneas para temperaturas máximas y mínimas
    - Tooltip enriquecido con prob. de lluvia y viento
    """
    fechas = pronostico["time"]
    maxs = pronostico["temperature_2m_max"]
    mins = pronostico["temperature_2m_min"]
    lluvias = pronostico.get("precipitation_probability_max", [0]*len(fechas))
    vientos = pronostico.get("windspeed", [0]*len(fechas))  # si no hay, ponemos 0

    fig = go.Figure()

    hover_text_max = [f"Máx: {mx}°C<br>Prob. Lluvia: {ll}%<br>Viento: {v} km/h" 
                      for mx, ll, v in zip(maxs, lluvias, vientos)]
    hover_text_min = [f"Mín: {mn}°C<br>Prob. Lluvia: {ll}%<br>Viento: {v} km/h" 
                      for mn, ll, v in zip(mins, lluvias, vientos)]

    # Temperatura máxima
    fig.add_trace(go.Scatter(
        x=fechas,
        y=maxs,
        mode='lines+markers',
        name='Temp. Máx (°C)',
        line=dict(color='red'),
        hovertext=hover_text_max,
        hoverinfo='text'
    ))

    # Temperatura mínima
    fig.add_trace(go.Scatter(
        x=fechas,
        y=mins,
        mode='lines+markers',
        name='Temp. Mín (°C)',
        line=dict(color='blue'),
        hovertext=hover_text_min,
        hoverinfo='text'
    ))

    fig.update_layout(
        title=f"Pronóstico de 7 días - {ciudad}",
        xaxis_title="Fecha",
        yaxis_title="Temperatura (°C)",
        legend=dict(x=0.01, y=0.99),
        template='plotly_white'
    )

    fig.show()
