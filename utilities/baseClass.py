#Standard library imports
import random

#Third party imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from openpyxl.utils import get_column_letter

#Proyect imports
from tests import conftest


class baseClass:

# No uso la creación del driver como constructor porque llamo a la baseClass en mas de un archivo (en la de los tests, pero tambien en cada uno de los modulos
# que hay por cada pagina). Cada vez que se cree un objeto de alguna de las clases en cada uno de los modulos se abriria una nueva ventana del driver. Y esto no se quiere.
# Entonces se crea un metodo para la creación del driver y este metodo se lo llama desde el constructor del test y desde este se lo pasamos a las otras clases que lo necesitan.
# Todo esto porque no puedo usar fixtures en este proyecto, si así pudiese sería diferente.

    # def __init__(self):
    #     self.driver = conftest.setup()


    def creacion_driver(self):
    # Podríamos crear esta funcion directamente en el modulo de TESTS llamando al modulo CONFTESTS pero lo hacemos aca para mantener el estandar de definir el driver en la baseClass
        self.driver = conftest.setup()

    def wait_to_click(self, locator, time):
        WebDriverWait(self.driver, time).until(EC.element_to_be_clickable(locator)).click()

    def wait_url(self, url, time):
        WebDriverWait(self.driver, time).until(EC.url_to_be((url)))

    def wait_to_text(self, text, locator, time):
        WebDriverWait(self.driver, time).until(EC.text_to_be_present_in_element(locator, text))

    def wait_element_presence(self, locator, time, path):
        WebDriverWait(self.driver, time).until(EC.presence_of_element_located(locator)).send_keys(path)


    def styling_df(self, dataframe, sheetName, writer):
        dataframe.style.apply(self.styling_df_colors, axis = 1).to_excel(writer, sheet_name=sheetName, index=False, freeze_panes=(1,0))
        worksheet = writer.sheets[sheetName]

        #Columns AutoFit
        for col in worksheet.columns:
            max_length = 0
            column = get_column_letter(col[0].column)  # Get the column name
            for cell in col:
                try:  # Necessary to avoid error on empty cells
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length) * 1.2
            worksheet.column_dimensions[column].width = adjusted_width

    def styling_df_colors(self, dataframe):

        if "Total Tactica" in dataframe.index:
            columna = 'Clasificación'
        elif "Tipo Cambio" in dataframe.index:
            columna = 'Clasificacion'
        else:
            color = 'white'
            return ['background-color: '+color]*len(dataframe.index)

        if dataframe[columna] == 'MATCH EXACTO' or dataframe[columna] == 'POTENCIAL ERROR - MATCH EXACTO' or dataframe[columna] == 'MATCH C/ TOLERANCIA' or dataframe[columna] == 'POTENCIAL ERROR - MATCH C/ TOLERANCIA' or dataframe[columna] == "MATCH C/ TOLERANCIA ($ extranjera)":
            color = '#A3BF8A'
        # elif dataframe[columna] == "REVISAR 'IVA'/'TOTAL'" or dataframe[columna] == "POTENCIAL ERROR - REVISAR 'IVA'/'TOTAL'":
        #     color = '#F2EF76'
        elif dataframe[columna] == "REVISAR 'IVA'/'TOTAL'" or dataframe[columna] == "POTENCIAL ERROR - REVISAR 'IVA'/'TOTAL'" or dataframe[columna] == "REVISAR 'CUIT'" or dataframe[columna] == "POTENCIAL ERROR - REVISAR 'CUIT'" or dataframe[columna] == "REVISAR 'N° FC'" or dataframe[columna] == "POTENCIAL ERROR - REVISAR 'N° FC'":
            color = '#F2B676'
        else:
            color = 'white'

        return ['background-color: '+color]*len(dataframe.index)
