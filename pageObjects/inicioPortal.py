#Standard library imports

#Third party imports
from selenium.webdriver.common.by import By

#Proyect imports
from utilities.baseClass import baseClass

class inicioPortal(baseClass):

    def __init__(self, driver):
        self.driver = driver

    btnIngresar = (By.XPATH, "//span[contains(text(), 'Ingresar')]")

    def ingresar_libros(self):
        self.wait_to_click(inicioPortal.btnIngresar, 120)
