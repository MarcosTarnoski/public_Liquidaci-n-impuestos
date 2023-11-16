# Standard library imports

# Third party imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Proyect imports
from data.directory import directory

def setup():
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
    chromeOptions.add_experimental_option("prefs", {"download.default_directory" : directory+"\\paperworks"}) #Aca decimos la ruta en la que queremos que guarde archivos que se descarguen
    # chromeOptions.add_argument("--start-maximized") # No inicio aca porque ya agrego la funcion maximice desde el test. En la compue de Silvana no se porque si no esta abierta la ventana del driver no puede ingresar la URL y salta error.
    chromeOptions.add_argument('--disable-gpu') # Para que no salten esos errores raros
    service = Service(executable_path=r"C:\chromedriver_win32\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chromeOptions) #Hacemos referencia al
    # driver de chrome que vamos a usar en todo el programa.Con la letra "r" estas indicando que lo que sigue es una dirección, sino la
    # barra invertida '\' marcaría ERROR. Ademas se agrega la opcion de que no muestre el cartel "software de prueba automatizado"
    return driver
