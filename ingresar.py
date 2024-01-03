import tkinter as tk
import pyodbc
import subprocess

# Establecer la cadena de conexión
# connection_string = 'DRIVER={SQL Server};SERVER=DESKTOP-J78FMU8;DATABASE=DB_Asistente;UID=sa;PWD=123'
connection_string = 'DRIVER={SQL Server};SERVER=192.168.0.4;DATABASE=DB_Asistente;UID=sa;PWD=123'

# Función para ejecutar la consulta SQL
def ejecutar_consulta(pronuncia, accion, palabra, mensaje_label):
    try:
        # Conectar a la base de datos
        conexion = pyodbc.connect(connection_string)

        # Crear un cursor
        cursor = conexion.cursor()

        # Consulta SQL con parámetros
        consulta_sql = f"INSERT INTO dbo.Accion (Pronuncia, Accion, Palabra) VALUES ('{pronuncia}', '{accion}', '{palabra}')"

        # Ejecutar la consulta
        cursor.execute(consulta_sql)

        # Confirmar los cambios
        conexion.commit()

        # Cerrar la conexión
        conexion.close()

        # Limpiar los Entry widgets
        entry_pronuncia.delete(0, tk.END)
        entry_accion.delete(0, tk.END)
        entry_palabra.delete(0, tk.END)

        # Actualizar el mensaje
        mensaje_label.config(text="Datos ingresados correctamente.")

    except Exception as e:
        print(f"Error: {e}")
        # Actualizar el mensaje en caso de error
        mensaje_label.config(text=f"Error: {e}")

# Función para obtener los valores de los Entry widgets y ejecutar la consulta
def obtener_valores_y_ejecutar():
    pronuncia = entry_pronuncia.get()
    accion = entry_accion.get()
    palabra = entry_palabra.get()

    ejecutar_consulta(pronuncia, accion, palabra, mensaje_label)

# Función para abrir el otro script (asistente.py)
def abrir_asistente():
    ventana.destroy()
    # Ocultar la ventana actual
    # ventana.iconify()

    # Ejecutar el otro script (asistente.py)
    subprocess.run(["python", "asistente.py"])

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Ingresar Datos")

# Obtener las dimensiones de la pantalla
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()

# Establecer las dimensiones de la ventana
ancho_ventana = 400
alto_ventana = 300

# Calcular la posición para centrar la ventana
x_pos = (ancho_pantalla - ancho_ventana) // 2
y_pos = (alto_pantalla - alto_ventana) // 2

# Establecer la geometría de la ventana
ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")

# Crear Entry widgets
entry_pronuncia = tk.Entry(ventana, width=30)
entry_accion = tk.Entry(ventana, width=30)
entry_palabra = tk.Entry(ventana, width=30)

# Crear etiquetas para los Entry widgets
label_pronuncia = tk.Label(ventana, text="Pronuncia:")
label_accion = tk.Label(ventana, text="Accion:")
label_palabra = tk.Label(ventana, text="Palabra:")

# Crear botón para ejecutar la consulta
boton_ejecutar = tk.Button(ventana, text="Ejecutar Consulta", command=obtener_valores_y_ejecutar)

# Crear botón para abrir el otro script
boton_asistente = tk.Button(ventana, text="Abrir Asistente", command=abrir_asistente)

# Crear etiqueta para el mensaje
mensaje_label = tk.Label(ventana, text="")

# Organizar los widgets en la ventana
label_pronuncia.grid(row=0, column=0, padx=10, pady=5)
entry_pronuncia.grid(row=0, column=1, padx=10, pady=5)
label_accion.grid(row=1, column=0, padx=10, pady=5)
entry_accion.grid(row=1, column=1, padx=10, pady=5)
label_palabra.grid(row=2, column=0, padx=10, pady=5)
entry_palabra.grid(row=2, column=1, padx=10, pady=5)
boton_ejecutar.grid(row=3, column=0, columnspan=2, pady=10)
boton_asistente.grid(row=4, column=0, columnspan=2, pady=10)
mensaje_label.grid(row=5, column=0, columnspan=2, pady=10)

# Iniciar el bucle principal de la aplicación
ventana.mainloop()
