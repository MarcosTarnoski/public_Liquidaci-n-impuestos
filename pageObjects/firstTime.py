#Standard library imports

#Third party imports
from selenium.webdriver.common.by import By

#Proyect imports
from utilities.baseClass import baseClass


class firstTime(baseClass):

    def __init__(self, driver):
        self.driver = driver
        
    btnGuardar = (By.ID, "btnGuardar")

    def guardar(self):
        self.wait_to_click(firstTime.btnGuardar, 40)
