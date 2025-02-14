import tkinter as tk
import random
import math
import time

# Lista de opciones de la ruleta (vacía para que el usuario agregue)
opciones = []

# Crear ventana principal
root = tk.Tk()
root.title("Ruleta de Premios")
root.geometry("500x600")

# Configurar el canvas
canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.pack()

# Centro y radio de la ruleta
cx, cy = 200, 200
radio = 150

# Función para dibujar la ruleta
def dibujar_ruleta(angulo_base=0):
    canvas.delete("all")  # Borra todo antes de redibujar

    if not opciones:
        canvas.create_text(cx, cy, text="Agrega opciones", font=("Arial", 14, "bold"), fill="red")
        return

    angulo_por_sector = 360 / len(opciones)

    # Dibujar la base circular
    canvas.create_oval(cx - radio, cy - radio, cx + radio, cy + radio, 
                       fill="white", outline="black", width=2)

    # Dibujar sectores rotados
    for i, opcion in enumerate(opciones):
        angulo_inicio = (i * angulo_por_sector + angulo_base) % 360
        angulo_medio = angulo_inicio + angulo_por_sector / 2
        color = f"#{random.randint(0, 0xFFFFFF):06x}"
        
        # Dibujar el sector
        canvas.create_arc(cx - radio, cy - radio, cx + radio, cy + radio,
                          start=angulo_inicio, extent=angulo_por_sector,
                          fill=color, outline="black", style=tk.PIESLICE)

        # Calcular la posición del texto
        angulo_radianes = math.radians(angulo_medio)
        text_x = cx + (radio / 2) * math.cos(angulo_radianes)
        text_y = cy - (radio / 2) * math.sin(angulo_radianes)

        # Dibujar el texto en el sector
        canvas.create_text(text_x, text_y, text=opcion, font=("Arial", 10, "bold"), fill="black")

    # Dibujar el centro de la ruleta
    canvas.create_oval(cx - 20, cy - 20, cx + 20, cy + 20, fill="black")

    # Dibujar la flecha roja (puntero)
    canvas.create_polygon(cx, cy - radio - 10, cx - 10, cy - radio - 30, 
                          cx + 10, cy - radio - 30, fill="red")

# Animación de giro
def girar_ruleta():
    if not opciones:
        resultado_label.config(text="¡Agrega opciones primero!", fg="red")
        return

    angulo_por_sector = 360 / len(opciones)
    giros = random.randint(20, 40)  # Cantidad de giros
    angulo_actual = 0
    velocidad = 15  # Velocidad inicial

    for _ in range(giros):
        angulo_actual += velocidad
        dibujar_ruleta(angulo_actual)
        root.update()
        time.sleep(0.05)

        if velocidad > 2:
            velocidad -= 1  # Desaceleración progresiva

    # Seleccionar el ganador basado en la posición final
    angulo_final = angulo_actual % 360
    indice_ganador = int(angulo_final // angulo_por_sector)
    opcion_ganadora = opciones[indice_ganador]
    resultado_label.config(text=f"Resultado: {opcion_ganadora}", fg="black")

# Función para agregar opciones a la lista
def agregar_opcion():
    nueva_opcion = entrada_opcion.get().strip()
    if nueva_opcion and nueva_opcion not in opciones:
        opciones.append(nueva_opcion)
        entrada_opcion.delete(0, tk.END)
        lista_opciones.config(text="Opciones: " + ", ".join(opciones))
        dibujar_ruleta()
    else:
        resultado_label.config(text="Opción inválida o repetida", fg="red")

# Dibujar la ruleta inicial
dibujar_ruleta()

# Entrada para agregar opciones
entrada_opcion = tk.Entry(root, font=("Arial", 12))
entrada_opcion.pack(pady=5)

# Botón para agregar opciones
boton_agregar = tk.Button(root, text="Agregar Opción", command=agregar_opcion, font=("Arial", 12))
boton_agregar.pack(pady=5)

# Mostrar opciones agregadas
lista_opciones = tk.Label(root, text="Opciones: Ninguna", font=("Arial", 10))
lista_opciones.pack(pady=5)

# Botón para girar
boton = tk.Button(root, text="Girar", command=girar_ruleta, font=("Arial", 14))
boton.pack(pady=10)

# Etiqueta para mostrar el resultado
resultado_label = tk.Label(root, text="Resultado: ?", font=("Arial", 14))
resultado_label.pack()

# Ejecutar la ventana
root.mainloop()
