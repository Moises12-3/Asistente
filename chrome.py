import webbrowser

# Especifica la URL que deseas abrir en el navegador
url = "https://github.com/Moises12-3"

# Ruta al ejecutable del navegador que deseas usar (puedes cambiarla según tu navegador)
chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

# Abre la URL en el navegador especificado
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
webbrowser.get('chrome').open(url)
