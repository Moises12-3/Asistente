import pyttsx3
import pyodbc
import time
import datetime
import random
import webbrowser
import requests

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
    engine = pyttsx3.init()
    voz_externa_id = obtener_voz_externa(engine)
    engine.setProperty('voice', voz_externa_id)
    engine.setProperty('rate', 150)

    # Obtener la hora actual
    now = datetime.datetime.now()

    # Determinar si es de mañana, tarde o noche
    if 5 <= now.hour < 12:
        periodo = "mañana"
    elif 12 <= now.hour < 18:
        periodo = "tarde"
    else:
        periodo = "noche"

    # Saludo personalizado según el periodo del día
    mensaje_saludo = f"¡Hola! Buen{'' if periodo == 'mañana' else 'as'} {periodo}. Soy Jenny, tu asistente virtual. ¿En qué puedo ayudarte?"
    
    engine.say(mensaje_saludo)
    engine.runAndWait()

def obtener_hora():
    now = datetime.datetime.now()
    hora_12h = now.strftime("%I:%M %p")
    periodo = ""
    if 5 <= now.hour < 12:
        periodo = "mañana"
    elif 12 <= now.hour < 18:
        periodo = "tarde"
    else:
        periodo = "noche"
    if now.minute == 0:
        return f"Son las {now.strftime('%I en punto')} de la {periodo}"
    else:
        return f"La hora actual es {hora_12h} de la {periodo}"

def contar_chiste():
    connection_string = 'DRIVER={SQL Server};SERVER=DESKTOP-J78FMU8;DATABASE=DB_Asistente;UID=sa;PWD=123'

    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        cursor.execute("SELECT MAX(ID) FROM dbo.chiste")
        max_id = cursor.fetchone()[0]

        random_id = random.randint(1, max_id)
        
        query = "SELECT TOP 1 Pronuncia FROM dbo.chiste WHERE ID >= ? ORDER BY NEWID()"
        cursor.execute(query, random_id)
        chiste = cursor.fetchone()[0]

        print(chiste)
        hablar_mensaje(chiste)

    except pyodbc.Error as ex:
        mensaje_error = f"Error de conexión a la base de datos: {ex}"
        print(mensaje_error)
        hablar_mensaje(mensaje_error)

    finally:
        if connection:
            connection.close()

            
def hablar_mensaje(mensaje):
    engine = pyttsx3.init()
    voz_externa_id = obtener_voz_externa(engine)
    engine.setProperty('voice', voz_externa_id)
    engine.setProperty('rate', 150)
    time.sleep(1)
    engine.say(mensaje)
    engine.runAndWait()

def abrir_chrome():
    hablar_mensaje("Abriendo Navegador Chrome, por favor espere")
    url = "https://github.com/Moises12-3"

    # Ruta al ejecutable del navegador que deseas usar (puedes cambiarla según tu navegador)
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

    # Abre la URL en el navegador especificado
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
    webbrowser.get('chrome').open(url)


def buscar_en_chrome():
    hablar_mensaje("Buscando en Google, por favor espere")

    # Pedir al usuario que ingrese los términos de búsqueda
    hablar_mensaje("Ingrese los términos de búsqueda en Google: ")
    terminos_busqueda = input("Ingrese los términos de búsqueda en Google: ")

    # Construir la URL de búsqueda en Google
    url = f"https://www.google.com/search?q={terminos_busqueda}"

    # Ruta al ejecutable del navegador que deseas usar (puedes cambiarla según tu navegador)
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

    # Abre la URL en una nueva pestaña del navegador especificado
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
    webbrowser.get('chrome').open_new_tab(url)

def obtener_noticias(api_key, ubicacion, idioma):
    url = "https://newsapi.org/v2/top-headlines"

    parametros = {
        'apiKey': api_key,
        'country': ubicacion,
        'language': idioma,
        'pageSize': 5
    }

    try:
        respuesta = requests.get(url, params=parametros)
        respuesta.raise_for_status()  # Esto generará una excepción para errores HTTP

        noticias = respuesta.json()

        if respuesta.status_code == 200:
            if noticias['totalResults'] > 0:
                for i, noticia in enumerate(noticias['articles'], 1):
                    titulo = noticia['title']
                    print(f"Noticia {i}: {titulo}")
            else:
                print("No se encontraron noticias para los parámetros proporcionados.")
        else:
            print(f"Error al obtener noticias. Código de estado: {respuesta.status_code}")
            print(respuesta.json())

    except requests.exceptions.HTTPError as errh:
        print(f"Error HTTP: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error de conexión: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Tiempo de espera agotado: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Error en la solicitud: {err}")

    print("Fin de la función obtener_noticias")



def ejecutar_comandos():
    while True:
        comando = input("Ingrese un comando: ").lower()

        try:
            if "hola jenny" in comando or "hola" in comando:
                saludar()
            elif "que hora es jenny" in comando or "que hora es" in comando or "necesito la hora " in comando:
                hora = obtener_hora()
                hablar_mensaje(hora)
                print(hora)
            elif "cuentame un chiste" in comando:
                contar_chiste()
            elif "abre chrome" in comando:
                abrir_chrome()
            elif "buscame en chrome" in comando:
                buscar_en_chrome()
            elif "noticias" in comando:
                api_key = 'cf71599490684efa894139b32187882c'
                ubicacion = 'ni'  # Reemplaza 'us' con tu ubicación deseada
                idioma = 'es'
                obtener_noticias(api_key, ubicacion, idioma)
            elif comando == "salir":
                break
            else:
                mensaje_no_reconocido = "Comando no reconocido. Prueba con 'hola jenny', 'que hora es jenny', 'cuentame un chiste' o 'noticias'."
                hablar_mensaje(mensaje_no_reconocido)
                print(mensaje_no_reconocido)

        except Exception as e:
            mensaje_error_general = f"Error general: {e}"
            print(mensaje_error_general)
            hablar_mensaje(mensaje_error_general)

if __name__ == "__main__":
    try:
        ejecutar_comandos()
    except Exception as e:
        mensaje_error_general = f"Error general: {e}"
        print(mensaje_error_general)
        hablar_mensaje(mensaje_error_general)
