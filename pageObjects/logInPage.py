#Hay una página para ingresar el usuario

#Standard library imports

#Third party imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Proyect imports
from utilities.baseClass import baseClass

class logInPage(baseClass):

    def __init__(self, driver):
        self.driver = driver

    inputCuit = (By.ID, "F1:username")
    btnSiguiente = (By.ID, "F1:btnSiguiente")
    inputPass = (By.ID, "F1:password")
    btnIngresar = (By.ID, "F1:btnIngresar")

    def enter_cuit(self, cuit):
        WebDriverWait(self.driver, 240).until(EC.presence_of_element_located(logInPage.inputCuit)).clear()
        # self.driver.find_element(*logInPage.inputCuit).clear()
        self.driver.find_element(*logInPage.inputCuit).send_keys(cuit)

    def siguiente(self):
        self.driver.find_element(*logInPage.btnSiguiente).click()

    def enter_pass(self, password):
        WebDriverWait(self.driver, 240).until(EC.presence_of_element_located(logInPage.inputPass)).clear()
        self.driver.find_element(*logInPage.inputPass).send_keys(password)

    def ingresar(self):
        self.driver.find_element(*logInPage.btnIngresar).click()
