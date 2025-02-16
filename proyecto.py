import tkinter as tk
from tkinter import colorchooser
import math
import time

# Lista de opciones con estructura [(nombre, color, porcentaje)]
opciones = []
porcentaje_total = 0  # Controla que no se pase de 100%

# Crear ventana principal
root = tk.Tk()
root.title("Ruleta Personalizada")
root.geometry("1150x850")

# Crear marco principal
frame_principal = tk.Frame(root)
frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Crear marco para la ruleta (izquierda)
frame_ruleta = tk.Frame(frame_principal)
frame_ruleta.grid(row=0, column=0, padx=10)

# Crear marco para los controles (derecha)
frame_controles = tk.Frame(frame_principal)
frame_controles.grid(row=0, column=1, padx=20)

tk.Label(frame_controles, text="Nueva Opcion", font=("Arial", 12)).pack()

# Frame para agrupar la entrada de opción y el botón de color
frame_opcion = tk.Frame(frame_controles)
frame_opcion.pack(pady=5)

# Entrada para la nueva opción
entrada_opcion = tk.Entry(frame_opcion, font=("Arial", 12))
entrada_opcion.pack(side=tk.LEFT, padx=5)

# Botón de color sin texto, solo con el color
color_seleccionado = "#FFFFFF"  # Color por defecto
boton_color = tk.Button(frame_opcion, bg=color_seleccionado, width=3, height=1, command=lambda: seleccionar_color(boton_color))
boton_color.pack(side=tk.LEFT)

# Configurar el canvas de la ruleta
canvas = tk.Canvas(frame_ruleta, width=800, height=800, bg="white")
canvas.pack()

# Centro y radio de la ruleta
cx, cy = 400, 400
radio = 350

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
    velocidad_inicial = slider_velocidad.get()
    tiempo_total = float(entrada_tiempo_parada.get())  # Obtener tiempo total de la animación

    # Variables para controlar la animación
    angulo_actual = 0  # Ángulo inicial
    tiempo_inicio = time.time()  # Tiempo de inicio de la animación

    # Función que realiza la animación del giro
    def animar_giro():
        nonlocal angulo_actual, velocidad_inicial

        # Calcular el tiempo transcurrido
        tiempo_transcurrido = time.time() - tiempo_inicio

        # Detener la animación si se alcanza el tiempo total
        if tiempo_transcurrido >= tiempo_total:
            seleccionar_ganador(angulo_actual)
            return

        # Reducir la velocidad gradualmente
        velocidad_actual = velocidad_inicial * (1 - (tiempo_transcurrido / tiempo_total))

        # Actualizar el ángulo de la ruleta
        angulo_actual += velocidad_actual
        dibujar_ruleta(angulo_actual)

        # Llamar a la función de animación nuevamente
        root.after(50, animar_giro)

    # Iniciar la animación del giro
    animar_giro()

# Función para determinar la opción ganadora
def seleccionar_ganador(angulo_final):
    # Ajustar el ángulo final para que sea relativo a la flecha en la parte superior
    angulo_final_ajustado = (90 - angulo_final) % 360  

    angulo_inicio = 0
    for opcion, _, porcentaje in opciones:
        angulo_ext = (porcentaje / 100) * 360
        if angulo_inicio <= angulo_final_ajustado < angulo_inicio + angulo_ext:
            resultado_label.config(text=f"Resultado: {opcion}", fg="black")
            return
        angulo_inicio += angulo_ext

# Función para agregar opciones con porcentaje
def agregar_opcion():
    global porcentaje_total
    nueva_opcion = entrada_opcion.get().strip()
    porcentaje = slider_porcentaje.get()

    if not nueva_opcion:
        resultado_label.config(text="Ingrese un nombre válido", fg="red")
        return
    
    if porcentaje_total + porcentaje > 100:
        resultado_label.config(text="¡El total supera el 100%!", fg="red")
        return

    opciones.append((nueva_opcion, color_seleccionado, porcentaje))
    porcentaje_total += porcentaje
    entrada_opcion.delete(0, tk.END)
    slider_porcentaje.set(50)  # Reiniciar el slider a 10% por defecto
    actualizar_lista_opciones()
    actualizar_porcentaje_total()
    dibujar_ruleta()

# Función para seleccionar un color
def seleccionar_color(boton):
    global color_seleccionado
    color = colorchooser.askcolor(title="Selecciona un color")[1]
    if color:
        color_seleccionado = color
        boton.config(bg=color)  # Cambia el color del botón seleccionado

# Función para actualizar la lista de opciones
def actualizar_lista_opciones():
    lista_opciones.delete(0, tk.END)
    for opcion, color, porcentaje in opciones:
        lista_opciones.insert(tk.END, f"{opcion} - {porcentaje}%")
        lista_opciones.itemconfig(tk.END, {'fg': color})

# Función para actualizar el porcentaje total mostrado
def actualizar_porcentaje_total():
    etiqueta_porcentaje_total.config(text=f"Total: {porcentaje_total}%")

# Barra deslizante para elegir porcentaje
tk.Label(frame_controles, text="Porcentaje (%):", font=("Arial", 12)).pack()
slider_porcentaje = tk.Scale(
    frame_controles, from_=1, to=100, orient=tk.HORIZONTAL,
    font=("Arial", 12),  # Texto más grande
    length=250,          # Longitud de la barra
    sliderlength=30,      # Tamaño del botón deslizante
    width=15,             # Grosor de la barra
    showvalue=True
)
slider_porcentaje.set(50)  # Valor inicial predeterminado
slider_porcentaje.pack(pady=1)

# Entrada para controlar el tiempo de parada
tk.Label(frame_controles, text="Tiempo para parar (segundos):", font=("Arial", 12)).pack()
entrada_tiempo_parada = tk.Entry(frame_controles, font=("Arial", 12))
entrada_tiempo_parada.insert(0, "5")  # Valor predeterminado
entrada_tiempo_parada.pack(pady=5)

# Entrada para controlar la velocidad
tk.Label(frame_controles, text="Velocidad:", font=("Arial", 12)).pack()
slider_velocidad = tk.Scale(
    frame_controles, from_=1, to=100, orient=tk.HORIZONTAL,
    font=("Arial", 12),  # Texto más grande
    length=250,          # Longitud de la barra
    sliderlength=30,      # Tamaño del botón deslizante
    width=15,             # Grosor de la barra
    showvalue=True
)
slider_velocidad.set(50)  # Valor predeterminado
slider_velocidad.pack(pady=1)

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

# Etiqueta para mostrar el resultado
resultado_label = tk.Label(frame_controles, text="", font=("Arial", 12))
resultado_label.pack(pady=10)



#AÑAAÑA AÑAAÑA AÑAAÑA AÑAAÑA NO DIGAS ESO PE PTAMRE QUE ME CGA LA CABEZA CAUSA
# Función para inicializar la ruleta con opciones de prueba
def inicializar_pruebas():
    global opciones, porcentaje_total
    opciones.clear()  # Limpiar la lista de opciones existentes
    porcentaje_total = 0  # Reiniciar el porcentaje total

    # Agregar 20 opciones con 5% de probabilidad cada una
    for i in range(1, 51):
        opciones.append((f"{i}", "white", 2))  # Color único para cada opción
        porcentaje_total += 2

    # Actualizar la lista de opciones y dibujar la ruleta
    actualizar_lista_opciones()
    actualizar_porcentaje_total()
    dibujar_ruleta()

# Llamar a la función de pruebas después de configurar la interfaz
root.after(100, inicializar_pruebas)  # Esperar 100 ms para asegurar que la interfaz esté lista

# dibujar_ruleta()
root.mainloop()