import pyowm

# Sustituye "d673e50d06945bbe507d1854e1da52bf" con tu clave API de OpenWeatherMap
API_KEY = "d673e50d06945bbe507d1854e1da52bf"
owm = pyowm.OWM(API_KEY)

# Pregunta al usuario la ubicación
ciudad = input("Ingrese el nombre de la ciudad: ")

try:
    # Busca la ubicación
    observacion = owm.weather_at_place(ciudad)
    clima = observacion.get_weather()

    # Obtén la información del clima
    temperatura = clima.get_temperature('celsius')['temp']
    estado_cielo = clima.get_status()

    print(f'En {ciudad}, la temperatura es {temperatura}°C y el estado del cielo es {estado_cielo}.')
except pyowm.exceptions.api_response_error.NotFoundError:
    print(f'No se pudo encontrar información para {ciudad}.')
