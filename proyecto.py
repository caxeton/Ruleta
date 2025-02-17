import tkinter as tk
from tkinter import ttk, colorchooser
import math
import time
import random

# Lista de opciones con estructura [(nombre, color, porcentaje)]
opciones = []
porcentaje_total = 0  # Controla que no se pase de 100%

# Crear ventana principal
root = tk.Tk()
root.title("Ruleta Personalizada")
root.geometry("1600x900")

# Crear un contenedor para las vistas
contenedor_vistas = tk.Frame(root)
contenedor_vistas.pack(fill=tk.BOTH, expand=True)

# Función para cambiar entre vistas
def mostrar_vista(vista):
    # Oculta todas las vistas
    for v in todas_las_vistas:
        v.pack_forget()
    # Muestra la vista seleccionada
    vista.pack(fill=tk.BOTH, expand=True)

# Lista para almacenar todas las vistas
todas_las_vistas = []

# ---------------------------
# Vista Principal
# ---------------------------
vista_principal = tk.Frame(contenedor_vistas)
todas_las_vistas.append(vista_principal)

# Título de la vista principal
tk.Label(vista_principal, text="Menú Principal", font=("Arial", 24)).pack(pady=20)

# Marco para centrar los botones
frame_botones_principal = tk.Frame(vista_principal)
frame_botones_principal.pack(expand=True)  # Centrar en ambos ejes

# Botón de Ruleta (más grande)
boton_ruleta = tk.Button(frame_botones_principal, text="Ruleta", font=("Arial", 24), width=15, height=2, command=lambda: mostrar_vista(vista_ruleta))
boton_ruleta.pack(pady=10)

# Botón de Personalizar (más grande)
boton_personalizar = tk.Button(frame_botones_principal, text="Personalizar", font=("Arial", 24), width=15, height=2, command=lambda: mostrar_vista(vista_personalizar))
boton_personalizar.pack(pady=10)

# ---------------------------
# Vista de Ruleta
# ---------------------------
vista_ruleta = tk.Frame(contenedor_vistas)
todas_las_vistas.append(vista_ruleta)

# Botón de "Volver al Menú Principal" en la esquina superior izquierda
boton_volver_ruleta = tk.Button(vista_ruleta, text="Volver", font=("Arial", 14), command=lambda: mostrar_vista(vista_principal))
boton_volver_ruleta.place(x=10, y=10)  # Posición fija en la esquina superior izquierda

# Marco para centrar la ruleta y el botón "Girar"
frame_centro_ruleta = tk.Frame(vista_ruleta)
frame_centro_ruleta.pack(expand=True)

# Configurar el canvas de la ruleta
canvas = tk.Canvas(frame_centro_ruleta, width=800, height=800, bg="white")
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


# ---------------------------
# Vista de Personalización
# ---------------------------
vista_personalizar = tk.Frame(contenedor_vistas)
todas_las_vistas.append(vista_personalizar)

# Botón de "Volver al Menú Principal"
boton_volver_personalizar = tk.Button(vista_personalizar, text="Volver", font=("Arial", 14), command=lambda: mostrar_vista(vista_principal))
boton_volver_personalizar.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=10)

# Marco para la personalización de la ruleta
frame_personalizacion = tk.Frame(vista_personalizar)
frame_personalizacion.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Entrada para controlar el tiempo de parada
tk.Label(frame_personalizacion, text="Tiempo para parar (segundos):", font=("Arial", 12)).pack()
entrada_tiempo_parada = tk.Entry(frame_personalizacion, font=("Arial", 12))
entrada_tiempo_parada.insert(0, "5")  # Valor predeterminado
entrada_tiempo_parada.pack(pady=5)

# Entrada para controlar la velocidad
tk.Label(frame_personalizacion, text="Velocidad:", font=("Arial", 12)).pack()
slider_velocidad = tk.Scale(
    frame_personalizacion, from_=1, to=100, orient=tk.HORIZONTAL,
    font=("Arial", 12), length=250, sliderlength=30, width=15, showvalue=True
)
slider_velocidad.set(50)  # Valor predeterminado
slider_velocidad.pack(pady=1)

# Etiqueta de color seleccionado
tk.Label(frame_personalizacion, text="Nombre Opción", font=("Arial", 12)).pack()



# Botón de color sin texto, solo con el color
color_seleccionado = "#FFFFFF"  # Color por defecto
boton_color = tk.Button(frame_personalizacion, bg=color_seleccionado, width=3, height=1, command=lambda: seleccionar_color(boton_color))
boton_color.pack(pady=5)

# Barra deslizante para elegir porcentaje
tk.Label(frame_personalizacion, text="Porcentaje (%):", font=("Arial", 12)).pack()
slider_porcentaje = tk.Scale(
    frame_personalizacion, from_=1, to=100, orient=tk.HORIZONTAL,
    font=("Arial", 12), length=250, sliderlength=30, width=15, showvalue=True
)
slider_porcentaje.set(50)  # Valor inicial predeterminado
slider_porcentaje.pack(pady=1)

# Marco para la lista de opciones
frame_contenedor_opciones = tk.Frame(frame_personalizacion)
frame_contenedor_opciones.pack(fill=tk.BOTH, expand=False, pady=10)

# Crear un Canvas y una barra de desplazamiento
canvas_opciones = tk.Canvas(frame_contenedor_opciones, bg="white")
scrollbar = ttk.Scrollbar(frame_contenedor_opciones, orient=tk.VERTICAL, command=canvas_opciones.yview)
canvas_opciones.configure(yscrollcommand=scrollbar.set)

# Empaquetar el Canvas y la barra de desplazamiento
canvas_opciones.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Crear un Frame interno dentro del Canvas
frame_lista_opciones = tk.Frame(canvas_opciones)
canvas_opciones.create_window((0, 0), window=frame_lista_opciones, anchor=tk.NW)

# Configurar el desplazamiento del Canvas
def configurar_desplazamiento(event):
    canvas_opciones.configure(scrollregion=canvas_opciones.bbox("all"))

frame_contenedor_opciones.bind("<Configure>", configurar_desplazamiento)

# Indicador del porcentaje total
etiqueta_porcentaje_total = tk.Label(frame_personalizacion, text="Total: 0%", font=("Arial", 12))
etiqueta_porcentaje_total.pack()

# ---------------------------
# Funcionalidades adicionales
# ---------------------------
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




# Dentro de la configuración de la vista de la ruleta, agrega el botón "Girar"
boton_girar = tk.Button(frame_centro_ruleta, text="Girar", font=("Arial", 18), width=10, height=2, command=girar_ruleta)
boton_girar.pack(pady=20)

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

def agregar_opcion(event=None):
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
    slider_porcentaje.set(50)  # Reiniciar el slider a 50% por defecto
    actualizar_lista_opciones()
    actualizar_porcentaje_total()
    dibujar_ruleta()


# Entrada para la nueva opción
entrada_opcion = tk.Entry(frame_personalizacion, font=("Arial", 12))
entrada_opcion.pack(pady=5)
entrada_opcion.bind("<Return>", agregar_opcion)  # Agregar opción al presionar Enter


def editar_porcentaje(indice, nuevo_porcentaje):
    global porcentaje_total
    opcion_actual, color_actual, porcentaje_actual = opciones[indice]

    if porcentaje_total - porcentaje_actual + nuevo_porcentaje > 100:
        resultado_label.config(text="¡El total supera el 100%!", fg="red")
        return

    # Actualizar la opción
    opciones[indice] = (opcion_actual, color_actual, nuevo_porcentaje)
    porcentaje_total = porcentaje_total - porcentaje_actual + nuevo_porcentaje

    actualizar_porcentaje_total()
    dibujar_ruleta()

def editar_nombre(indice, nuevo_nombre):
    opcion_actual, color_actual, porcentaje_actual = opciones[indice]
    opciones[indice] = (nuevo_nombre, color_actual, porcentaje_actual)
    dibujar_ruleta()

def eliminar_opcion(indice):
    global porcentaje_total
    opcion_actual, _, porcentaje_actual = opciones[indice]

    # Eliminar la opción
    opciones.pop(indice)
    porcentaje_total -= porcentaje_actual

    actualizar_lista_opciones()
    actualizar_porcentaje_total()
    dibujar_ruleta()

def seleccionar_color(boton):
    global color_seleccionado
    color = colorchooser.askcolor(title="Selecciona un color")[1]
    if color:
        color_seleccionado = color
        boton.config(bg=color)  # Cambia el color del botón seleccionado

def actualizar_lista_opciones():
    for widget in frame_lista_opciones.winfo_children():
        widget.destroy()

    for indice, (opcion, color, porcentaje) in enumerate(opciones):
        frame_opcion = tk.Frame(frame_lista_opciones)
        frame_opcion.pack(fill=tk.X, pady=2)

        # Marco para el nombre y el color
        frame_nombre_color_porcentaje_eliminar = tk.Frame(frame_opcion)
        frame_nombre_color_porcentaje_eliminar.pack(fill=tk.X)

        # Mostrar el nombre de la opción (editable)
        entrada_nombre = tk.Entry(frame_nombre_color_porcentaje_eliminar, font=("Arial", 12))
        entrada_nombre.insert(0, opcion)
        entrada_nombre.bind("<Return>", lambda e, i=indice, entrada=entrada_nombre: editar_nombre(i, entrada.get()))
        entrada_nombre.pack(side=tk.LEFT, padx=5)

        # Mostrar el color de la opción
        boton_color = tk.Button(frame_nombre_color_porcentaje_eliminar, bg=color, width=3, height=1, command=lambda i=indice: seleccionar_color(boton_color))
        boton_color.pack(side=tk.LEFT, padx=5)

        # Mostrar el porcentaje de la opción (editable)
        entrada_porcentaje = tk.Entry(frame_nombre_color_porcentaje_eliminar, font=("Arial", 12), width=5)
        entrada_porcentaje.insert(0, str(porcentaje))
        entrada_porcentaje.pack(side=tk.LEFT, padx=5)

        # Botón para eliminar la opción
        boton_eliminar = tk.Button(frame_nombre_color_porcentaje_eliminar, text="Eliminar", command=lambda i=indice: eliminar_opcion(i), font=("Arial", 12))
        boton_eliminar.pack(side=tk.RIGHT, padx=5)

def actualizar_porcentaje_total():
    etiqueta_porcentaje_total.config(text=f"Total: {porcentaje_total}%")

# ---------------------------
# Mostrar la vista principal al inicio
# ---------------------------
mostrar_vista(vista_principal)

# Iniciar la aplicación
root.mainloop()