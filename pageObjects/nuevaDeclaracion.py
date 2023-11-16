#Standard library imports

#Third party imports
from selenium.webdriver.common.by import By

#Proyect imports
from utilities.baseClass import baseClass

class nuevaDeclaracion(baseClass):

    def __init__(self, driver):
        self.driver = driver

    desplegable_periodos = (By.ID, "periodo")
    btn_continuar = (By.XPATH, "//span[contains(text(), 'Continuar')]")
    btn_ingresar = (By.XPATH, "//span[contains(text(), 'Ingresar')]")

    def mostrar_periodos(self):
        self.wait_to_click(nuevaDeclaracion.desplegable_periodos, 120)

    def select_periodo(self, mes):
        selector_periodo = f"option[value='{mes}']"
        print(selector_periodo)
        periodo = (By.CSS_SELECTOR, selector_periodo)
        self.wait_to_click(periodo, 10)
    
    def continuar(self):
        self.wait_to_click(nuevaDeclaracion.btn_continuar, 10)

    def ingresar(self):
        self.wait_to_click(nuevaDeclaracion.btn_ingresar, 120)