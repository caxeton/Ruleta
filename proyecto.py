import tkinter as tk
from tkinter import colorchooser, messagebox
import random
import math
import time

# Lista de opciones con estructura [(nombre, color, porcentaje)]
opciones = []
porcentaje_total = 0  # Controla que no se pase de 100%

# Crear ventana principal
root = tk.Tk()
root.title("Ruleta Personalizada")
root.geometry("750x500")

# Crear marco principal
frame_principal = tk.Frame(root)
frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Crear marco para la ruleta (izquierda)
frame_ruleta = tk.Frame(frame_principal)
frame_ruleta.grid(row=0, column=0, padx=10)

# Crear marco para los controles (derecha)
frame_controles = tk.Frame(frame_principal)
frame_controles.grid(row=0, column=1, padx=20)

# Configurar el canvas de la ruleta
canvas = tk.Canvas(frame_ruleta, width=400, height=400, bg="white")
canvas.pack()

# Centro y radio de la ruleta
cx, cy = 200, 200
radio = 150
color_seleccionado = "#FFFFFF"

# Variables para controlar la velocidad y el tiempo
velocidad_inicial = 15  # Velocidad inicial
tiempo_parada = 2  # Tiempo en segundos para reducir la velocidad a 0

# Función para dibujar la ruleta
def dibujar_ruleta(angulo_base=0):
    canvas.delete("all")  # Borra todo antes de redibujar

    if not opciones:
        canvas.create_text(cx, cy, text="Agrega opciones", font=("Arial", 14, "bold"), fill="red")
        return

    angulo_inicio = angulo_base  # Se inicia en el ángulo base

    # Dibujar cada sector con su tamaño personalizado
    for opcion, color, porcentaje in opciones:
        angulo_ext = (porcentaje / 100) * 360  # Conversión de porcentaje a grados
        angulo_medio = angulo_inicio + angulo_ext / 2
        
        # Dibujar el sector con su color asignado
        canvas.create_arc(cx - radio, cy - radio, cx + radio, cy + radio,
                          start=angulo_inicio, extent=angulo_ext,
                          fill=color, outline="black", style=tk.PIESLICE)

        # Calcular la posición del texto
        angulo_radianes = math.radians(angulo_medio)
        text_x = cx + (radio / 2) * math.cos(angulo_radianes)
        text_y = cy - (radio / 2) * math.sin(angulo_radianes)

        # Dibujar el texto dentro del sector
        canvas.create_text(text_x, text_y, text=opcion, font=("Arial", 10, "bold"), fill="black")

        angulo_inicio += angulo_ext  # Mover al siguiente sector

    # Dibujar el centro de la ruleta
    canvas.create_oval(cx - 20, cy - 20, cx + 20, cy + 20, fill="black")

    # Dibujar la flecha roja (puntero)
    canvas.create_polygon(cx, cy - radio - 10, cx - 10, cy - radio - 30, 
                          cx + 10, cy - radio - 30, fill="red")

# Animación de giro
def girar_ruleta():
    if not opciones or porcentaje_total != 100:
        resultado_label.config(text="Asegúrate de que el total sea 100%", fg="red")
        return

    # Obtener los valores de velocidad y tiempo desde las entradas
    velocidad = velocidad_inicial
    tiempo_total = float(entrada_tiempo_parada.get())  # Obtener tiempo total de la animación

    # Calcular la cantidad de giros en función del tiempo total y la velocidad
    giros_totales = int(tiempo_total * velocidad_inicial)  # Determina cuántos giros en total basados en el tiempo y velocidad

    angulo_actual = 0  # Ángulo inicial
    velocidad_minima = 1  # Velocidad mínima para el giro

    # Función que realiza la animación del giro
    def animar_giro(giros_restantes, angulo_actual, velocidad):
        if giros_restantes <= 0:
            seleccionar_ganador(angulo_actual)
            return

        angulo_actual += velocidad
        dibujar_ruleta(angulo_actual)
        root.after(50, animar_giro, giros_restantes - 1, angulo_actual, max(velocidad_minima, velocidad - (velocidad_inicial / (tiempo_total * 2))))  # Llamada recursiva para animación

    # Iniciar la animación del giro
    animar_giro(giros_totales, angulo_actual, velocidad)

# Función para determinar la opción ganadora
def seleccionar_ganador(angulo_final):
    angulo_inicio = 0
    for opcion, _, porcentaje in opciones:
        angulo_ext = (porcentaje / 100) * 360
        if angulo_inicio <= angulo_final < angulo_inicio + angulo_ext:
            resultado_label.config(text=f"Resultado: {opcion}", fg="black")
            return
        angulo_inicio += angulo_ext

# Función para agregar opciones con porcentaje
def agregar_opcion():
    global porcentaje_total
    nueva_opcion = entrada_opcion.get().strip()
    porcentaje_str = entrada_porcentaje.get().strip()

    if not nueva_opcion or not porcentaje_str.isdigit():
        resultado_label.config(text="Ingrese un nombre y porcentaje válido", fg="red")
        return

    porcentaje = int(porcentaje_str)
    
    if porcentaje_total + porcentaje > 100:
        resultado_label.config(text="¡El total supera el 100%!", fg="red")
        return

    opciones.append((nueva_opcion, color_seleccionado, porcentaje))
    porcentaje_total += porcentaje
    entrada_opcion.delete(0, tk.END)
    entrada_porcentaje.delete(0, tk.END)
    actualizar_lista_opciones()
    actualizar_porcentaje_total()
    dibujar_ruleta()

# Función para seleccionar un color
def seleccionar_color():
    global color_seleccionado
    color = colorchooser.askcolor(title="Selecciona un color")[1]
    if color:
        color_seleccionado = color
        etiqueta_color.config(text=f"Color elegido", fg=color)

# Función para actualizar la lista de opciones
def actualizar_lista_opciones():
    lista_opciones.delete(0, tk.END)
    for opcion, color, porcentaje in opciones:
        lista_opciones.insert(tk.END, f"{opcion} - {porcentaje}%")
        lista_opciones.itemconfig(tk.END, {'fg': color})

# Función para actualizar el porcentaje total mostrado
def actualizar_porcentaje_total():
    etiqueta_porcentaje_total.config(text=f"Total: {porcentaje_total}%")

# Entrada para agregar opciones
tk.Label(frame_controles, text="Nueva Opción:", font=("Arial", 12)).pack()
entrada_opcion = tk.Entry(frame_controles, font=("Arial", 12))
entrada_opcion.pack(pady=5)

# Entrada para el porcentaje
tk.Label(frame_controles, text="Porcentaje (%):", font=("Arial", 12)).pack()
entrada_porcentaje = tk.Entry(frame_controles, font=("Arial", 12))
entrada_porcentaje.pack(pady=5)

# Entrada para controlar el tiempo de parada
tk.Label(frame_controles, text="Tiempo para parar (segundos):", font=("Arial", 12)).pack()
entrada_tiempo_parada = tk.Entry(frame_controles, font=("Arial", 12))
entrada_tiempo_parada.pack(pady=5)

# Botón para seleccionar color
boton_color = tk.Button(frame_controles, text="Seleccionar Color", command=seleccionar_color, font=("Arial", 12), bg="lightgray")
boton_color.pack(pady=5)

# Etiqueta de color seleccionado
etiqueta_color = tk.Label(frame_controles, text="Color elegido", font=("Arial", 10))
etiqueta_color.pack(pady=5)

# Botón para agregar opción
boton_agregar = tk.Button(frame_controles, text="Agregar Opción", command=agregar_opcion, font=("Arial", 12))
boton_agregar.pack(pady=5)

# Lista de opciones agregadas
lista_opciones = tk.Listbox(frame_controles, width=30, height=10, font=("Arial", 10))
lista_opciones.pack(pady=5)

# Indicador del porcentaje total
etiqueta_porcentaje_total = tk.Label(frame_controles, text="Total: 0%", font=("Arial", 12))
etiqueta_porcentaje_total.pack()

# Botón para girar
boton = tk.Button(frame_controles, text="Girar", command=girar_ruleta, font=("Arial", 14))
boton.pack(pady=10)


dibujar_ruleta()
root.mainloop()
