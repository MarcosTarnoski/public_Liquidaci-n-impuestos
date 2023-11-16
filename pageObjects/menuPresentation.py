#Standard library imports

#Third party imports
from selenium.webdriver.common.by import By

#Proyect imports
from utilities.baseClass import baseClass


class menuPresentation(baseClass):

    def __init__(self, driver, locator):
        self.btnLibro = (By.ID, locator)
        self.driver = driver

    def select_book(self):
        self.wait_to_click(self.btnLibro, 240)
