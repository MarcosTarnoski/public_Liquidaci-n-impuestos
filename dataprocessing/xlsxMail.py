# Standard library imports

# Third party imports
import pandas as pd

# Proyect imports
from utilities.baseClass import baseClass

#Registros pendientes de carga en sistema. Se hace clase porque se usara para comparas o ventas. Ademas, así tambien puedo heredar las funciones para darle estilo al excel
class regPendientes(baseClass):

    def __init__(self, modulo, path):
        self.modulo = modulo
        self.path = path

    def export_pendientes(self):
        # Primero verifico que hayan registros a enviar por mail.
        # Lo tengo que revisar siempre porque el usuario pudo haber modificado alguna Clasificación a mano, por esto no me puedo guiar por atributos de etapas anteriores para saber si enviar o no el mail.
        # Prefiero pagar el costo de un poco mas de redundancia (o de generar objeto inncecesario porque quizas se crean 2 y no hay mails para enviar) a cambio de mayor versatilidad.
        # Ademas asi le queda una explicacion al usuario que falta porque no se generó
        while True:
            try:
                # print("PATHS: ",self.path)
                dataframeAfip = pd.read_excel(self.path, sheet_name = "Libro AFIP")
                filterA = dataframeAfip["Clasificacion"].str.contains('|'.join(["A CARGAR TACTICA","REVISAR 'CUIT'","REVISAR 'N° FC'","REVISAR 'IVA'/'TOTAL'"]))
                self.dataframeAfip = dataframeAfip[filterA]
                rowsCountA = len(self.dataframeAfip)

                # filterA = (dataframeAfip["Clasificacion"] == "A CARGAR TACTICA") | (dataframeAfip["Clasificacion"] == "REVISAR 'CUIT'") | (dataframeAfip["Clasificacion"] == "REVISAR 'N° FC'") | (dataframeAfip["Clasificacion"] == "REVISAR 'IVA'/'TOTAL'")
                dataframeTct = pd.read_excel(self.path, sheet_name = "Libro Táctica")
                filterT = dataframeTct["Clasificación"].str.contains("POTENCIAL ERROR")
                self.dataframeTct = dataframeTct[filterT]
                rowsCountT = len(self.dataframeTct)

                #si ninguno pasa el filtro anterior no se crea el excel
                if rowsCountA > 0 or rowsCountT > 0:
                    self.path = self.path.replace('.xlsx',' - CORRECCIONES TACTICA.xlsx')

                    with pd.ExcelWriter(self.path) as writer:
                        if rowsCountT > 0:
                            self.styling_df(self.dataframeTct, "Libro Táctica", writer)
                        if rowsCountA > 0:
                            self.styling_df(self.dataframeAfip, "Libro AFIP", writer)

                    print(f"\n## ARCHIVO GENERADO ## - Se ha generado archivo {self.modulo} 'CORRECCIONES TACTICA' para enviar por mail")
                else:
                    print(f"\n## ARCHIVO NO GENERADO ## - No hay registros {self.modulo} 'CORRECCIONES TACTICA'")
                break

            except PermissionError:
                input(f'\n### ERROR ### Por favor, cerrar archivo Excel "{self.modulo} - CORRECIONES TACTICA".\nPresione "ENTER" para continuar' )
