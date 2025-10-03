import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from clima.api import buscar_ciudad, obtener_clima_actual_latlon, obtener_pronostico_latlon, obtener_pronostico_horario
from clima.historial import cargar_historial, guardar_historial
import webbrowser
import tempfile

class ClimaApp:
    def __init__(self, root):
        self.root = root
        root.title("Reportes de Clima")
        root.geometry("950x800")

        self.historial_ciudades = cargar_historial()

        self.label = tk.Label(root, text="Ingrese ciudad:")
        self.label.pack(pady=5)
        self.ciudad_var = tk.StringVar()
        self.entry = ttk.Combobox(root, textvariable=self.ciudad_var, width=40, values=self.historial_ciudades)
        self.entry.pack(pady=5)

        self.boton = tk.Button(root, text="Buscar clima", command=self.buscar_clima)
        self.boton.pack(pady=10)

        self.texto_reporte = tk.Text(root, height=38, width=115)
        self.texto_reporte.pack(pady=10)

        self.boton_grafico = tk.Button(root, text="Mostrar gráfico", command=self.mostrar_grafico)
        self.boton_grafico.pack(pady=5)
        self.boton_grafico.pack_forget()

        self.pronostico_guardado = None
        self.ciudad_guardada = None

    def buscar_clima(self):
        ciudad_input = self.ciudad_var.get().strip()
        if not ciudad_input or len(ciudad_input) < 2:
            messagebox.showerror("Error", "Ingrese un nombre de ciudad válido.")
            return

        self.texto_reporte.delete(1.0, tk.END)
        self.texto_reporte.insert(tk.END, "🔎 Buscando...\n")
        self.root.update()

        coincidencias = buscar_ciudad(ciudad_input)
        if not coincidencias:
            self.texto_reporte.delete(1.0, tk.END)
            self.texto_reporte.insert(tk.END, "❌ No se encontraron coincidencias.\n")
            return

        if len(coincidencias) > 1:
            opciones = [f"{c['name']}, {c.get('state','')}, {c['country']}".strip(", ") for c in coincidencias]
            seleccion = self.pedir_seleccion(opciones)
            if seleccion is None:
                self.texto_reporte.delete(1.0, tk.END)
                return
        else:
            seleccion = 0

        ciudad_elegida = coincidencias[seleccion]
        lat = ciudad_elegida['lat']
        lon = ciudad_elegida['lon']
        nombre_completo = f"{ciudad_elegida['name']}, {ciudad_elegida['country']}"

        if nombre_completo not in self.historial_ciudades:
            self.historial_ciudades.insert(0, nombre_completo)
            if len(self.historial_ciudades) > 5:
                self.historial_ciudades.pop()
        self.entry['values'] = self.historial_ciudades
        guardar_historial(self.historial_ciudades)

        clima = obtener_clima_actual_latlon(lat, lon)
        pronostico = obtener_pronostico_latlon(lat, lon)
        pronostico_hora = obtener_pronostico_horario(lat, lon)

        self.pronostico_guardado = pronostico
        self.ciudad_guardada = nombre_completo

        self.texto_reporte.delete(1.0, tk.END)
        reporte = f"=== 🌤️ REPORTE DE CLIMA ===\nCiudad: {nombre_completo}\n"
        reporte += f"🌡️ Temperatura: {clima.get('temperature', 'N/A')}°C | 💨 Viento: {clima.get('windspeed', 'N/A')} km/h\n\n"
        reporte += "=== 🌦️ Pronóstico de 7 días ===\n"
        for i in range(len(pronostico["time"])):
            fecha_obj = datetime.strptime(pronostico["time"][i], "%Y-%m-%d")
            fecha_formateada = fecha_obj.strftime("%d-%m-%Y")
            lluvia = pronostico['precipitation_probability_max'][i]
            icon_lluvia = "🌧️" if lluvia >= 30 else "☀️"
            temp_max = pronostico['temperature_2m_max'][i]
            temp_min = pronostico['temperature_2m_min'][i]
            icon_temp = "🔥" if temp_max >= 30 else ("❄️" if temp_min <= 10 else "")
            reporte += f"{fecha_formateada} -> Min: {temp_min}°C | Max: {temp_max}°C {icon_temp} | Lluvia: {lluvia}% {icon_lluvia}\n"

        reporte += "\n=== 🌡️ Pronóstico horario hoy ===\n"
        for i in range(len(pronostico_hora["time"])):
            hora = pronostico_hora["time"][i].split("T")[1][:5]
            temp = pronostico_hora["temperature_2m"][i]
            icon_temp = "🔥" if temp >= 30 else ("❄️" if temp <= 10 else "")
            reporte += f"{hora} -> {temp}°C {icon_temp}\n"

        self.texto_reporte.insert(tk.END, reporte)
        self.boton_grafico.pack()

    def pedir_seleccion(self, opciones):
        sel_window = tk.Toplevel(self.root)
        sel_window.title("Seleccione ciudad")
        sel_window.geometry("400x300")
        tk.Label(sel_window, text="Se encontraron varias coincidencias:").pack(pady=5)

        canvas_frame = tk.Frame(sel_window)
        canvas_frame.pack(fill="x", padx=10)

        canvas = tk.Canvas(canvas_frame, height=200)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        var = tk.IntVar(value=-1)
        for i, op in enumerate(opciones):
            tk.Radiobutton(scrollable_frame, text=op, variable=var, value=i).pack(anchor="w", pady=2)

        boton_ok = tk.Button(sel_window, text="Seleccionar", command=sel_window.destroy)
        boton_ok.pack(pady=5)

        sel_window.wait_window()
        if var.get() == -1:
            return None
        return var.get()

    def mostrar_grafico(self):
        if self.pronostico_guardado and self.ciudad_guardada:
            from reportes.graficos import graficar_pronostico
            graficar_pronostico(self.pronostico_guardado, self.ciudad_guardada)
