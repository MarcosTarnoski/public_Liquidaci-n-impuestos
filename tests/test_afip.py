#Standard library imports
import time
import sys

#Third party imports
from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC #(el "as" es para guardar esto en una variable EC, para poder llamarlo mas facil)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

#Proyect imports
#se importa como si estuvieses parado en el directorio del MAIN, que es justamente desde el que ejecutas todo.
from data import portalIVA
from pageObjects.logInPage import logInPage
from pageObjects.aplicativosMenu import aplicativosMenu
from pageObjects.inicioPortal import inicioPortal
from pageObjects.changeRelation import changeRelation
from pageObjects.firstTime import firstTime
from pageObjects.menuPresentation import menuPresentation
from pageObjects.librosIVA import librosIVA
from pageObjects.nuevaDeclaracion import nuevaDeclaracion
from utilities.baseClass import baseClass
from dataprocessing.oldFiles import move_files
from selenium.common.exceptions import WebDriverException, SessionNotCreatedException


class testsAfip(baseClass):


    def __init__(self, empresa, loginCuit, mes):
        self.empresa = empresa
        self.cuit = loginCuit
        self.mes = mes
        self.password = "Beraza2022"
        try:
            self.creacion_driver()
        except SessionNotCreatedException:
            input("\n## ACTUALIZACION PENDIENTE ## - Por favor, solicitar actualización de la aplicación para poder utilizarla.")
            sys.exit(1)


    def test_log_in(self):
        #El get() para abrir la pagina lo hacemos acá y no en el conftest porque la sesión caduca. Entonces si lo ponemos en el setup() del conftest te la abre una vez sola
        # Necesitamos que se abra en los 2 procesos posibles: descargar excels o subir txts
        loginpage = logInPage(self.driver)
        # self.driver.maximize_window()

        # #Parche "try": (CORREGIR)
        # try:
        #     print("## entre al try ##\n")
        #     self.driver.maximize_window()
        # except WebDriverException:
        #     print("\nPor favor, recordar al abrir manualmente navegador para operar en el portal (borrar FC's dolares por ejemplo) recordar minimizar tamaño de la ventana.\nPara subir los txt, ejecutar funcion '5) Subir txts a AFIP'\n")
        #     self.driver.minimize_window()

        # #Parche "try": (CORREGIR)
        try:
            self.driver.maximize_window()
        except WebDriverException:
            # print("\nPor favor, recordar al abrir manualmente navegador para operar en el portal (borrar FC's dolares por ejemplo) recordar minimizar tamaño de la ventana.\nPara subir los txt, ejecutar funcion '5) Subir txts a AFIP'\n")
            self.driver.minimize_window()
            time.sleep(1)
            self.driver.maximize_window()

        time.sleep(1.5)
        self.driver.get("https://auth.afip.gob.ar/contribuyente_/login.xhtml")
        loginpage.enter_cuit(self.cuit)
        time.sleep(4)
        loginpage.siguiente()
        loginpage.enter_pass(self.password)
        loginpage.ingresar()
        # print("\nSi no visualiza el navegador, por favor abrirlo haciendo click en la barra de tareas.\n")



    def test_IVA_menu(self):
        appsmenu = aplicativosMenu(self.driver)
        appsmenu.enter_servicios()
        time.sleep(2)
        appsmenu.search_portal_IVA()
        time.sleep(2)
        appsmenu.enter_portal_IVA()
        time.sleep(2)
        self.driver.switch_to.window(self.driver.window_handles[len(self.driver.window_handles)-1]) #Cambiamos a la última pestaña que se haya abierto
        if self.empresa != "WENTEK SA":
            relation = changeRelation(self.driver, self.empresa) #PARA WENTEK NO VA
            relation.change_relation()
            time.sleep(2.5)
            relation.select_empresa()
            time.sleep(2.5)
        inicio = inicioPortal(self.driver)
        inicio.ingresar_libros()
        nueva_declaracion = nuevaDeclaracion(self.driver)
        nueva_declaracion.mostrar_periodos()
        nueva_declaracion.select_periodo(self.mes)
        nueva_declaracion.continuar()
        nueva_declaracion.ingresar()
        time.sleep(5)
        # Si aparece el menu para hacer click, le das nomas. Sino sigue normal.
        if self.driver.current_url == "https://serviciosjava2.afip.gob.ar/liva/jsp/verDatosInicialesPresentacion.do":
            firsttime = firstTime(self.driver)
            self.driver.execute_script("document.getElementsByClassName('customcheck')[6].click()")
            time.sleep(4.5)
            firsttime.guardar()
        self.wait_url("https://serviciosjava2.afip.gob.ar/liva/jsp/menuPresentacion.do", 240)
        time.sleep(4)



    def test_choose_book(self, locators):
        libro = menuPresentation(self.driver, locators['btnLibro'])
        libro.select_book()
        time.sleep(4)
        self.wait_url(locators['urlLibro'], 240)



    def test_download_book(self, modulo):
    # Pasamos como lista para que pueda recorrer un for la funcion, en una vuelta ejecuta lo de compras y en la otra lo de ventas. Cuando es solo una vuelta, lo pasas como lista igual asi lo reconoce y no tira error el for pero seria una vuelta sola para ese modulo
    # Se está pasando una lista de diccionarios
    # No hice un switch acá (funcion con un diccionario) porque son solo 3 condiciones
        if modulo == "Compras":
            locators = [portalIVA.compras]
        elif modulo == "Ventas":
            locators = [portalIVA.ventas]
        elif modulo == "ComprasyVentas":
            locators = [portalIVA.compras, portalIVA.ventas]
        else:
            raise ValueError("Valor argumento 'modulo' invalido")

        #El flag es para saber si ya recorrio una vez el for. Lo usamos para saber si tenemos que hace el driver.back en los casos que se hacen tanto compras como ventas
        flag = False

        self.test_log_in()
        self.test_IVA_menu()
        libroDownload = librosIVA(self.driver)

        for item in locators:
            self.test_choose_book(item)
            #  ******** DESCARGA LIBRO ********
            libroDownload.desplegable_importacion()
            libroDownload.select_afip()
            time.sleep(4)
            # AGERGAR EN ESTA LINEA CONSERVAR COMPROBANTE PREVIAMENTE INCLUIDO
            libroDownload.download_data()
            libroDownload.processing() #Espera hasta que la carga de datos este completada. Si tira error termina el programa y no descarga los datos.
            webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(3)
            libroDownload.to_excel()
            time.sleep(2) #Si estes delay no esta falla la descarga del excel compras
            if flag == False and len(locators)>1:
                flag = True #Se pone el flag en True para que no haga el driver.back en la segunda vuelta en caso de habers
                self.driver.back() #Regresa a pagina anterior

        # size = self.driver.get_window_size()
        # width = size.get("width")
        # height = size.get("height")
        self.driver.minimize_window()
        # self.driver.set_window_size(width, height)




    def test_upload_txts(self, locators):
        # Manejo de error, dado que si hay error en los TXT que se suben porque AFIP los rebota, queremos evitar falla del programa
        # try:
            # Inicializo variables y saco los files que correspondan (los files para la comparación vieja se pasan a carpeta LIQUIDACIÓN ANTERIOR).
            # Solo se sacan los archivos viejos de AFIP porque son los que siempre van a estar viejos. Puede ser que los de tactica esten todos los registros bien y que solo haya que subir en afip.
            # En ese caso, tendría que ver que los registros solo tengan "A CARGAR AFIP" y despues todo "MATCH EXACTO". Pero muchas veces el error de una factura cargada mal se elige no corregir y
            # se toma como bien. Entonces es dificil saber cuando estan bien los libros de tactica y cuando no. Por lo tanto dejo que el usuario saque y ponga los archivos del sistema.

            #El flag es para saber si ya recorrio una vez el for. Lo usamos para saber si tenemos que hace el driver.back en los casos que se hacen tanto compras como ventas
        flag = False

        print("\nSi aún no visualiza el navegador para subir txt, por favor maximizar manualmente la ventana desde la barra de tareas.\n")
        self.test_log_in()
        self.test_IVA_menu()
        libroUpload = librosIVA(self.driver)

        for item in locators:
            self.test_choose_book(item)
            #  ******** UPLOAD TXT ********
            libroUpload.desplegable_importacion()
            libroUpload.select_upload()
            time.sleep(2)
            libroUpload.charge_cte(item['pathTxtCte'])
            time.sleep(2)
            libroUpload.charge_alic(item['pathTxtAlic'])
            time.sleep(2)
            #Seleccionamos "CONSERVAR EL COMPROBANTE PREVIAMENTE INLCUIDO"
            libroUpload.desplegable_data()
            libroUpload.select_conserve_data()
            #Seleccionamos "LOS IMPORTES ESTAN EXPRESADOS EN PESOS ARGENTINOS" o "LOS IMPORTES ESTAN EXPRESADOS EN LA MONEDA ORIGINAL DEL COMPROBANTE"
            libroUpload.desplegable_moneda()
            libroUpload.select_pesos()
            time.sleep(2)
            libroUpload.importar_txt()
            libroUpload.processing()
            time.sleep(2)
            webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(4)
            libroUpload.to_excel()
            time.sleep(2)
            if flag == False and len(locators)>1:
                flag = True #Se pone el flag en True para que no haga el driver.back en la segunda vuelta en caso de haber
                self.driver.back() #Regresa a pagina anterior
                # En el main se pregunta si se subiran en dolares pero solo se puede dolares desde compras. No de ventas. Entonces antes de que pase a hacer el de ventas ponemos que se sube en moneda original.
        # except:
        #     print("### ERROR ### - Subida de TXT fallida.")
        self.driver.minimize_window()
