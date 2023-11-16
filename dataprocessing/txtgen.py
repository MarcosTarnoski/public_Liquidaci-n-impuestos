# Standard library imports

# Third party imports
import pandas as pd

# Proyect imports
from data import txt, matching


class txtGenerator:

    def __init__(self, module, month):

        self.modulo = module
        self.mes = month
        if self.modulo == "Compras":
            self.pathTxtCte = txt.compras['pathTxtCte']
            self.pathNewTxtCte = txt.compras['pathNewTxtCte']
            self.pathTxtAlic = txt.compras['pathTxtAlic']
            self.pathNewTxtAlic = txt.compras['pathNewTxtAlic']
            self.nComprobante = matching.compras['nComprobante']
        elif self.modulo == "Ventas":
            self.pathTxtCte = txt.ventas['pathTxtCte']
            self.pathNewTxtCte = txt.ventas['pathNewTxtCte']
            self.pathTxtAlic = txt.ventas['pathTxtAlic']
            self.pathNewTxtAlic = txt.ventas['pathNewTxtAlic']
            self.nComprobante = matching.ventas['nComprobante']
        else:
            raise ValueError("Valor argumento 'modulo' invalido")


    def read_write_txt(self, data, txtPath, newTxtPath):

        with open(f'{txtPath}{self.mes}.txt', 'r') as fileRead:
            with open(newTxtPath, 'w') as fileWrite:
                citi = fileRead.readlines()
                for x in data:
                    for i in citi:
                        if x in i:
                            fileWrite.write(i)

        # Verifico que la cantidad de registros en el txt generado coincida con la cantidad de registros "A CARGAR AFIP". Pero solo hago la verificacion si se trata de TXT CTES
        if self.pathNewTxtCte == newTxtPath:
            with open(newTxtPath, 'r') as fileRead:
                if self.rowsCount != len(fileRead.readlines()):
                    input(f"\n## WARNING ## {self.modulo} - 'txt COMPROBANTES' mal confeccionado - No coincide la cantidad de registros 'A CARGAR AFIP' con los filtrados en el txt.\nCorregir manualmente registros para luego subir al portal.\nPresione 'ENTER' para continuar...")


    def generate_txt(self, filePath):
        while True:
            # Dentro de un 'while true' de modo que si hay error con los archivos se puedan cargar sin necesidad de ejecutar todo de nuevo
            try:
                dataframe = pd.read_excel(filePath, sheet_name = 1)
                filter = (dataframe["Clasificación"] == "A CARGAR AFIP")
                dataframe = dataframe[filter]
                self.rowsCount = len(dataframe)

                #si ninguno pasa este filtro no se cree el txt
                if self.rowsCount != 0:

                    self.txtGenerated = True
                    facturas = dataframe.loc[:, self.nComprobante].copy() # Tomo valores de fila de nueva cabecera y los convierto en lista (array)
                    facturas = facturas.str.replace('-','000000000000')
                    cuits =  dataframe.loc[:, 'CUIT'].copy()

                    #En el cambio de tipo de variable de CUITS a STRING, agrega ".0" al final. Hay que sacarlo.
                    cuits = cuits.astype(str)
                    cuits = cuits.str.replace('\.0','', regex = True)
                    tipofcTxt = dataframe.loc[:, 'Tipo Tactica'].copy()

                    if self.modulo == "Compras":

                        filter1 = tipofcTxt.str.contains('Nota de Crédito - A')
                        filter2 = tipofcTxt.str.contains('Nota de Débito - A')
                        filter3 = tipofcTxt.str.contains('Nota de Crédito - B')
                        filter4 = tipofcTxt.str.contains('Nota de Débito - B')
                        filter5 = tipofcTxt.str.contains('Nota de Crédito - C')
                        filter6 = tipofcTxt.str.contains('Nota de Débito - C')
                        filter7 = tipofcTxt.str.contains('Factura - A')
                        filter8 = tipofcTxt.str.contains('Factura - C')
                        filter9 = tipofcTxt.str.contains('Factura - B')
                        filter10 = tipofcTxt.str.contains('Factura - M')
                        filter11 = tipofcTxt.str.contains('Nota de Crédito - M')
                        tipofcTxt.loc[filter1] = '003'
                        tipofcTxt.loc[filter2] = '002'
                        tipofcTxt.loc[filter3] = '008'
                        tipofcTxt.loc[filter4] = '007'
                        tipofcTxt.loc[filter5] = '013'
                        tipofcTxt.loc[filter6] = '012'
                        tipofcTxt.loc[filter7] = '001'
                        tipofcTxt.loc[filter8] = '011'
                        tipofcTxt.loc[filter9] = '006'
                        tipofcTxt.loc[filter10] = '051'
                        tipofcTxt.loc[filter11] = '053'

                        self.checkCte = tipofcTxt + facturas + "                80000000000" + cuits
                        self.checkAlic = tipofcTxt + facturas + "80000000000" + cuits
                    else:
                        filter1 = tipofcTxt.str.contains('|'.join(['CEA - Nota de Crédito A En Ventas - Electrónica','CVA - Nota de Crédito A En Ventas']))
                        filter2 = tipofcTxt.str.contains('DEA - Nota de Débito A En Ventas - Electrónica')
                        filter3 = tipofcTxt.str.contains('Nota de Crédito B')
                        filter4 = tipofcTxt.str.contains('Nota de Débito B')
                        filter5 = tipofcTxt.str.contains('Nota de Crédito C')
                        filter6 = tipofcTxt.str.contains('Nota de Débito C')
                        filter7 = tipofcTxt.str.contains('|'.join(['FEA - Factura de Venta A - Electrónica', 'FAA - Factura de Venta A'])) # Podría ser solo 'Factura de Venta A'
                        filter8 = tipofcTxt.str.contains('FEA-PYME - Factura de Crédito A En Ventas - Electrónica MiPyME')
                        filter9 = tipofcTxt.str.contains('CEA-PYME - Nota de Crédito A En Ventas - Electrónica MiPyME')
                        filter10 = tipofcTxt.str.contains('FEB - Factura de Venta B - Electrónica')
                        filter11 = tipofcTxt.str.contains('FAE - Factura de Venta E')
                        tipofcTxt.loc[filter1] = '003'
                        tipofcTxt.loc[filter2] = '002'
                        tipofcTxt.loc[filter3] = '008'
                        tipofcTxt.loc[filter4] = '007'
                        tipofcTxt.loc[filter5] = '013'
                        tipofcTxt.loc[filter6] = '012'
                        tipofcTxt.loc[filter7] = '001'
                        tipofcTxt.loc[filter8] = '201'
                        tipofcTxt.loc[filter9] = '203'
                        tipofcTxt.loc[filter10] = '006'
                        tipofcTxt.loc[filter11] = '019'

                        self.checkCte = tipofcTxt + facturas
                        self.checkAlic = facturas


                    self.read_write_txt(self.checkCte, self.pathTxtCte, self.pathNewTxtCte)
                    self.read_write_txt(self.checkAlic, self.pathTxtAlic, self.pathNewTxtAlic)

                    print(f"\n## ARCHIVO GENERADO ## {self.modulo} - Archivo txt")
                    break

                else:
                    self.txtGenerated = False
                    print(f"\n## ARCHIVO NO GENERADO ## {self.modulo} - No hay comprobantes 'A CARGAR AFIP'")
                    break

            except FileNotFoundError:
                input(f"\n### ERROR ### TXT '{self.modulo}' no encontrado. Verificar que los txt del sistema esten en la carpeta.\nPresione 'ENTER' para continuar...")

            except PermissionError:
                input(f'\n### ERROR ### Por favor, cerrar archivo Excel "IVA {self.modulo}".\nPresione "ENTER" para continuar' )
