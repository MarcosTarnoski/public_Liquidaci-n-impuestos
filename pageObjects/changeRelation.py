#Standard library imports

#Third party imports
from selenium.webdriver.common.by import By

#Proyect imports
from utilities.baseClass import baseClass

class changeRelation(baseClass):

    def __init__(self, driver, empresa):
        #En este caso, definimos como instance variable al locator porque si tomamos el valor de la empresa y lo definimos como
        #instance variable en el init, tira error. Lo que pasa es que primero se resuelven las class variables y despues las instance variables.
        self.btnEmpresa = (By.XPATH, "//h3[contains(text(), '"+empresa+"')]")
        self.driver = driver

    btnRelation = (By.XPATH, "//a[@href='#/changeRelation']")

    def change_relation(self):
        self.wait_to_click(changeRelation.btnRelation, 240)

    def select_empresa(self):
        self.wait_to_click(self.btnEmpresa, 120)
