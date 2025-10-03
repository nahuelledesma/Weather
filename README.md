# ClimaApp

Aplicación de escritorio en Python para consultar el clima actual y el pronóstico de 7 días de cualquier ciudad del mundo, con visualización gráfica y almacenamiento de historial.

## Características
- **Interfaz gráfica** con Tkinter.
- **Búsqueda inteligente** de ciudades (soporta ambigüedad y selección de país/estado).
- **Reporte detallado** con emojis y pronóstico horario.
- **Gráficos interactivos** de temperaturas y probabilidad de lluvia (Plotly).
- **Historial** de las últimas 5 ciudades consultadas.
- **Persistencia** del historial en `ciudades.json`.
- **Ejecutable standalone** para Windows generado con PyInstaller.

## Estructura del proyecto
```
clima/
    api.py           # Funciones para consultar APIs de clima y geocoding
    utils.py         # Utilidades de formato
    historial.py     # Manejo de historial de ciudades
    app.py           # Lógica de la interfaz gráfica (Tkinter)
config/
    settings.py      # Configuración global (unidades, idioma)
reportes/
    graficos.py      # Gráficos interactivos con Plotly
    consola.py       # Reporte en consola (opcional)
main.py             # Punto de entrada de la app
ciudades.json       # Historial de ciudades (se genera automáticamente)
requirements.txt    # Dependencias
```

## Instalación y ejecución desde código fuente
1. **Clona el repositorio:**
    ```sh
    git clone https://github.com/tuusuario/ClimaApp.git
    cd ClimaApp
    ```
2. **Instala las dependencias:**
    ```sh
    pip install -r requirements.txt
    ```
3. **Ejecuta la aplicación:**
    ```sh
    python main.py
    ```

## Uso del ejecutable (Windows)
Si no quieres instalar Python ni dependencias, puedes usar el ejecutable generado con PyInstaller:

- Busca el archivo `main.exe` en la carpeta `dist/` (se genera automáticamente tras correr PyInstaller).
- Haz doble clic en `main.exe` para abrir la aplicación con interfaz gráfica.
- No se abrirá consola adicional (modo `--windowed`).

**Nota:** Si quieres generar el ejecutable tú mismo:
```sh
pyinstaller --onefile --noconsole --windowed main.py
```
El ejecutable aparecerá en la carpeta `dist/`.

## Dependencias principales
- `requests`
- `tkinter` (incluido en Python estándar)
- `plotly`
- `matplotlib` (opcional)

## Créditos
- Datos meteorológicos: [Open-Meteo](https://open-meteo.com/)
- Geocoding: [Open-Meteo Geocoding API](https://open-meteo.com/en/docs/geocoding-api)

---
¡Contribuciones y sugerencias son bienvenidas!
