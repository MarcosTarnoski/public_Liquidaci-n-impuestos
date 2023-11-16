#Standard library imports

#Third party imports
from selenium.webdriver.common.by import By

#Proyect imports
from utilities.baseClass import baseClass

class librosIVA(baseClass):

    def __init__(self, driver):
        self.driver = driver

# Common locators
    despImport = (By.ID, "btnDropdownImportar")
    textProcesada = (By.XPATH, "//*[@id='tablaTareas']/tbody/tr[1]/td[4]/span")
    btnExcel = (By.XPATH, "//span[contains(text(), 'Excel')]")

# Download books locators
    optionAfip = (By.ID, "lnkImportarAFIP")
    btnDownload = (By.ID, "btnImportarAFIPImportar")

# Upload TXT locatos
    optionUpload = (By.ID, "lnkImportarArchivo")
    inputCte = (By.ID, "archivo")
    inputAlic = (By.ID, "archivoIVA")
    despData = (By.XPATH, "//*[@id='formArchivos']/div/div[3]/div/div/button")
    selectOldData = (By.XPATH, "//*[@id='formArchivos']/div/div[3]/div/div/div/ul/li[1]/a/span[1]")
    despMoneda = (By.XPATH, "//*[@id='formArchivos']/div/div[4]/div/div/button")
    selectDolar = (By.XPATH, "//*[@id='formArchivos']/div/div[4]/div/div/div/ul/li[2]/a/span[1]")
    selectPesos = (By.XPATH, "//*[@id='formArchivos']/div/div[4]/div/div/div/ul/li[1]/a/span[1]")
    btnImportTxt = (By.ID, "btnImportarArchivosImportar")




# Common functions
    def desplegable_importacion(self):
        self.wait_to_click(librosIVA.despImport, 240)

    def processing(self):
        self.wait_to_text("Procesada", librosIVA.textProcesada, 240)

    def to_excel(self):
        # self.driver.find_element(*librosIVA.btnExcel).click()
        self.driver.execute_script("document.getElementsByClassName('btn btn-default buttons-excel buttons-html5 btn-defaut btn-sm sinborde')[0].click()")



# Download books funtions
    def select_afip(self):
        self.wait_to_click(librosIVA.optionAfip, 10)

    def download_data(self):
        self.wait_to_click(librosIVA.btnDownload, 10)


# Upload TXT Functions
    def select_upload(self):
        self.wait_to_click(librosIVA.optionUpload, 10)

    def charge_cte(self, path):
        #No hago el send_keys aca porque con el wait element to be located en la base Class y aca el send_keys no andaba: "AttributeError: 'NoneType' object has no attribute 'send_keys'"
        self.wait_element_presence(librosIVA.inputCte, 180, path)

    def charge_alic(self, path):
        self.driver.find_element(*librosIVA.inputAlic).send_keys(path)

    def desplegable_data(self):
        self.driver.find_element(*librosIVA.despData).click()

    def select_conserve_data(self):
        self.wait_to_click(librosIVA.selectOldData, 15)

    def desplegable_moneda(self):
        self.driver.find_element(*librosIVA.despMoneda).click()

    def select_dolares(self):
        self.wait_to_click(librosIVA.selectDolar, 15)

    def select_pesos(self):
        self.wait_to_click(librosIVA.selectPesos, 15)

    def importar_txt(self):
        self.driver.find_element(*librosIVA.btnImportTxt).click()
