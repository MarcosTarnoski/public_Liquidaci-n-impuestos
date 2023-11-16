#Standard library imports

#Third party imports
from selenium.webdriver.common.by import By

#Proyect imports
from utilities.baseClass import baseClass

class aplicativosMenu(baseClass):

    def __init__(self, driver):
        self.driver = driver

    mis_servicios = (By.XPATH, "//a[text()='Ver todos']")
    buscador = (By.ID, "buscadorInput")
    portal_IVA = (By.XPATH, "//p[text()='Portal IVA']")

    def enter_servicios(self):
        self.wait_to_click(aplicativosMenu.mis_servicios, 240)

    def search_portal_IVA(self):
        self.wait_to_click(aplicativosMenu.buscador, 60)
        search_bar = self.driver.find_element(*aplicativosMenu.buscador)
        search_bar.clear()  # borrar si hay algún texto
        search_bar.send_keys("PORTAL IVA")  # escribir "PORTAL IVA"

    def enter_portal_IVA(self):
        self.wait_to_click(aplicativosMenu.portal_IVA, 60)

