import pyttsx3
import pyodbc

def obtener_voz_externa(engine):
    # Obtener la lista de voces disponibles
    voices = engine.getProperty('voices')

    # Buscar la voz deseada (en este caso, "Jenny")
    for voice in voices:
        if "Jenny" in voice.name:
            return voice.id

    # Si no se encuentra la voz "Jenny", devolver la primera voz
    return voices[0].id

def saludar():
    # Inicializar el motor de texto a voz
    engine = pyttsx3.init()

    # Obtener la voz externa deseada
    voz_externa_id = obtener_voz_externa(engine)

    # Establecer la voz del motor
    engine.setProperty('voice', voz_externa_id)

    # Configurar las propiedades del motor (opcional)
    engine.setProperty('rate', 150)  # Velocidad de habla (palabras por minuto)

    # Mensaje de saludo
    mensaje_saludo = "¡Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte?"

    # Decir el mensaje
    engine.say(mensaje_saludo)

    # Esperar a que termine de hablar
    engine.runAndWait()

    # Cadena de conexión a la base de datos SQL Server
    connection_string = 'DRIVER={SQL Server};SERVER=DESKTOP-J78FMU8;DATABASE=DB_Asistente;UID=sa;PWD=123'

    # Intentar establecer la conexión a la base de datos
    try:
        connection = pyodbc.connect(connection_string)
        engine.say("Conexión exitosa")

        # Esperar a que termine de hablar
        engine.runAndWait()
        print("Conexión exitosa")

        # Realizar operaciones en la base de datos aquí

    except pyodbc.Error as ex:
        engine.say("Error de conexión")

        # Esperar a que termine de hablar
        engine.runAndWait()
        print(f"Error de conexión: {ex}")

    finally:
        # Cerrar la conexión al finalizar
        if connection:
            connection.close()
            print("Conexión cerrada")
            engine.say("Conexión cerrada")

            # Esperar a que termine de hablar
            engine.runAndWait()

if __name__ == "__main__":
    try:
        saludar()
    except Exception as e:
        
        engine = pyttsx3.init()
        engine.say("Error no hay voces disponibles")

        # Esperar a que termine de hablar
        engine.runAndWait()
        print(f"Error: {e}")
