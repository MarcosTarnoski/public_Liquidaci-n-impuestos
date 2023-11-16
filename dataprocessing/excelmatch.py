# Standard library imports
import os

# Third party imports
import pandas as pd
import numpy as np
from openpyxl.utils import get_column_letter

# Proyect imports
from data import matching
from utilities.baseClass import baseClass


#         *************** FUNCIONES ***************
class excelProcessing(baseClass):

    TOLERANCE = 1.5
    dfNotas = pd.DataFrame(matching.notas)

    def __init__(self, modulo, empresa, cuit, mes):
    #Inicializamos variables según se concilie "Ventas" o "Compras"
        self.empresa = empresa
        self.mes = mes
        if modulo == "Compras":
            self.pathTct = matching.compras['pathTct']
            self.errorFields = matching.compras['errorFields']
            self.nDocAfip = matching.compras['nDocAfip']
            self.nComprobante = matching.compras['nComprobante']
            self.pathAfip = f"{matching.compras['pathAfip']}{cuit}.xlsx"
            self.fechaTct = matching.compras['fechaTct']
            self.exportPath = f"{matching.compras['exportPath']}{self.empresa} {self.mes}.xlsx"
            self.modulo = "Compras"
        elif modulo == "Ventas":
            self.pathTct = matching.ventas['pathTct']
            self.errorFields = matching.ventas['errorFields']
            self.nDocAfip = matching.ventas['nDocAfip']
            self.nComprobante = matching.ventas['nComprobante']
            self.pathAfip = f"{matching.ventas['pathAfip']}{cuit}.xlsx"
            self.fechaTct = matching.ventas['fechaTct']
            self.exportPath = f"{matching.ventas['exportPath']}{self.empresa} {self.mes}.xlsx"
            self.modulo = "Ventas"
        else:
            raise ValueError("Valor argumento 'modulo' invalido")

    def dataframes_comparison(self):
    # Armamos un 'while true' de modo que si salta error por no estar los archivos, se ejecute una y otra vez hasta que esten los archivos y no tener que empezar todo de nuevo
        while True:
            try:
                #        *************** STRUCTURING DATAFRAMES ***************
                dfAfip = pd.read_excel(self.pathAfip, skiprows = 1)
                # Formato al DataFrame AFIP
                #Notas de credito a importe negativo, Facturas en formato TACTICA.
                filtroNCAfip = dfAfip['Tipo'].str.contains('Nota de Crédito')
                dfAfip.loc[filtroNCAfip, ['IVA', 'Total']] = dfAfip.loc[filtroNCAfip, ['IVA', 'Total']] * -1
                dfAfip['Punto de Venta'] = dfAfip['Punto de Venta'].apply(self.pventa)+"-"+dfAfip['Número Desde'].apply(self.ndesde)
                dfAfip = dfAfip.drop(['Número Desde'], axis=1)
                #Clave convertirlo en Float a los valores porque sino queda como datatype "Object" y no se puede aplicar los metodos de nummpy para valores con tolerancia
                dfAfip[["IVA", "Total", self.nDocAfip]] = dfAfip[["IVA", "Total", self.nDocAfip]].astype(float)
                #Agregamos columna Clasificacion a los dataframes
                dfAfip.insert(0, 'Clasificacion', "")
                newColumnNamesAfip = dfAfip.columns.to_list()

                file_libro_tct = os.path.isfile(self.pathTct)
                if file_libro_tct and not dfAfip.empty:
                    # Formato al DataFrame Tactica
                    dfTct = pd.read_excel(self.pathTct)
                    filaInicialDFTct = dfTct[dfTct.eq(self.fechaTct).any(1)].index[0] + 1
                    filaFinalDFTct = dfTct[dfTct.eq('TOTALES').any(1)].index[0] - 1
                    newColumnNamesTct = dfTct.iloc[filaInicialDFTct - 1].to_list() # Tomo valores de fila de nueva cabecera y los convierto en lista (array)
                    #Convertimos a STRING todos los elementos de las nuevas etiquetas columnas, porque hay algunos que no lo son (21%, 27%)
                    for item in range(len(newColumnNamesTct)):
                        newColumnNamesTct[item] = str(newColumnNamesTct[item])
                        if newColumnNamesTct[item] in ['Tipo', 'Total', '0.21', '0.27', 'IVA', '0.03']:
                            newColumnNamesTct[item] = self.switch_Tct_Cols(newColumnNamesTct[item])
                    # Ahora si se puede asignar
                    dfTct.columns = newColumnNamesTct # Con la lista, puedo asignar las nuevas etiquetas a las columnas
                    dfTct = dfTct.iloc[filaInicialDFTct:filaFinalDFTct + 1] # Tomo las filas del DF que tienen los registros
                    #CUIT formato AFIP, IVA en formato AFIP (columna que sume total de los IVA)
                    dfTct['CUIT'] = dfTct['CUIT'].str.replace('-','')
                    dfTct['CUIT'] = dfTct['CUIT'].str.replace('/','')
                    dfTct['CUIT'] = dfTct['CUIT'].astype(float)
                    dfTct = dfTct.replace(" ", 0)

                    if self.empresa == "DECORMEC SA":
                        dfTct['IVA Tactica'] = dfTct['3%'] + dfTct['10,5 %'] + dfTct['21%'] + dfTct['27%']
                    else:
                        dfTct['IVA Tactica'] = dfTct['10,5 %'] + dfTct['21%'] + dfTct['27%']
                    
                    #Clave convertirlo en Float a los valores porque sino queda como datatype "Object" y no se puede aplicar los metodos de nummpy para valores con tolerancia
                    dfTct[["IVA Tactica", "Total Tactica"]] = dfTct[["IVA Tactica", "Total Tactica"]].astype(float)
                    #Agregamos columna Clasificacion a los dataframes
                    dfTct.insert(0, 'Clasificación', "")
                    newColumnNamesTct = dfTct.columns.to_list()

                    #        *************** MATCHING DATA ***************
                    #Primero vemos que no hayan registros duplicados. Si los hay, no se continua con la comparacion y se exporta para eliminarlos y volver a ejecutar la comparacion.
                    duplicatedTCT = dfTct.duplicated(subset = [self.nComprobante, 'Tipo Tactica','CUIT'], keep = False)
                    duplicatedAfip = dfAfip.duplicated(subset = ['Punto de Venta', 'Tipo',self.nDocAfip], keep = False)

                    if duplicatedTCT.sum() > 0 or duplicatedAfip.sum() > 0 :
                        dfTct_dup = dfTct[duplicatedTCT].copy()
                        dfAfip_dup = dfAfip[duplicatedAfip].copy()
                        #        *************** EXPORTING DATA ***************
                        with pd.ExcelWriter(self.exportPath) as writer:
                            if duplicatedTCT.sum() > 0:
                                self.styling_df(dfTct_dup, "DUPLICADOS_Libro Táctica", writer)
                            if duplicatedAfip.sum() > 0:
                                self.styling_df(dfAfip_dup, "DUPLICADOS_Libro Afip", writer)
                        input("\n### REGISTRO DUPLICADO ###\nSolicitar eliminar registro duplicado (ver archivo Excel creado).\nPara continuar con la 'LIQUIDACIÓN IVA', eliminar el duplicado del libro en Excel (Libro1, Libro 2, Comprobantes AFIP, según corresponda).\nPresione 'ENTER' para continuar")
                    else:
                    #        *************** MATCHING DATA ***************
                    # ERRORES POTENCIALES
                        dfTct = self.filter_errors(newColumnNamesTct, dfTct, self.errorFields)

                    #  1ER FILTRO: "Match Exacto"
                        aux = self.filter_merge([self.nComprobante,"CUIT","IVA Tactica", "Total Tactica"], ["Punto de Venta",self.nDocAfip,"IVA", "Total"], newColumnNamesTct, newColumnNamesAfip, dfTct, dfAfip)
                        self.df1Tct = aux[0]
                        self.df1Afip = aux[1]

                    #  2DO FILTRO: "Moneda extranjera: dentro de tolerancia respetando Tipo de cambio AFIP, CUIT y N°FC exactos"
                        #Elimino filas que pasaron 1er filtro. Para esto concateno los dataframes original y el del filtro 1 y elimino aquellas que quedan duplicadas
                        dfAfip = self.drop_filtered_rows([dfAfip, self.df1Afip], newColumnNamesAfip)
                        dfTct = self.drop_filtered_rows([dfTct, self.df1Tct], newColumnNamesTct)
                        # Filtro las de moneda extranjera
                        filter_extranjera = dfAfip['Moneda'] != "$"
                        dfAfip_extranjera = dfAfip[filter_extranjera].copy()
                        aux = self.filter_merge([self.nComprobante,"CUIT"], ["Punto de Venta", self.nDocAfip], newColumnNamesTct, newColumnNamesAfip, dfTct, dfAfip_extranjera)
                        df2Tct = aux[0]
                        df2Afip = aux[1]
                        aux = self.filter_tolerance(df2Tct, df2Afip, excelProcessing.TOLERANCE)
                        self.df2Tct = aux[0]
                        self.df2Afip = aux[1]

                    #  3ER FILTRO: "Match c/ tolerancia"
                        dfAfip = self.drop_filtered_rows([dfAfip, self.df2Afip], newColumnNamesAfip)
                        dfTct = self.drop_filtered_rows([dfTct, self.df2Tct], newColumnNamesTct)
                        aux = self.filter_merge([self.nComprobante,"CUIT"], ["Punto de Venta",self.nDocAfip], newColumnNamesTct, newColumnNamesAfip, dfTct, dfAfip)
                        df3Tct = aux[0]
                        df3Afip = aux[1]
                        aux = self.filter_tolerance(df3Tct, df3Afip, excelProcessing.TOLERANCE)
                        self.df3Tct = aux[0]
                        self.df3Afip = aux[1]

                    # 4TO FILTRO: Match CUIT y N° FC "Revisar IVA/TOTAL"
                        #Elimino filas que pasaron 2do filtro. Para esto concateno los dataframes original y el del filtro 2 y elimino aquellas que quedan duplicadas
                        dfTct = self.drop_filtered_rows([dfTct, self.df3Tct], newColumnNamesTct)
                        dfAfip = self.drop_filtered_rows([dfAfip, self.df3Afip], newColumnNamesAfip)
                        aux = self.filter_merge([self.nComprobante,"CUIT"], ["Punto de Venta",self.nDocAfip], newColumnNamesTct, newColumnNamesAfip, dfTct, dfAfip)
                        self.df4Tct = aux[0]
                        self.df4Afip = aux[1]

    # Args: cols a comparar del left df, cols a comparar del right df, todas las cols del df tct, todas las cols del df afip, left df, right df
                    # 5TO FILTRO: No coinciden CUITS "Revisar cual es el CUIT correcto", dentro de tolerancia
                        dfTct = self.drop_filtered_rows([self.df4Tct, dfTct], newColumnNamesTct)
                        dfAfip = self.drop_filtered_rows([dfAfip, self.df4Afip], newColumnNamesAfip)
                        aux = self.filter_merge([self.nComprobante], ["Punto de Venta"], newColumnNamesTct, newColumnNamesAfip, dfTct, dfAfip)
                        df5Tct = aux[0]
                        df5Afip = aux[1]
                        aux = self.filter_tolerance(df5Tct, df5Afip, excelProcessing.TOLERANCE)
                        self.df5Tct = aux[0]
                        self.df5Afip = aux[1]

                    # 6TO FILTRO: No coincide N° FC, dentro de tolerancia
                        dfTct = self.drop_filtered_rows([self.df5Tct,dfTct], newColumnNamesTct)
                        dfAfip = self.drop_filtered_rows([self.df5Afip,dfAfip], newColumnNamesAfip)
                        aux = self.filter_merge(["CUIT"], [self.nDocAfip], newColumnNamesTct, newColumnNamesAfip, dfTct, dfAfip)
                        df6Tct = aux[0]
                        df6Afip = aux[1]
                        aux = self.filter_tolerance(df6Tct, df6Afip, excelProcessing.TOLERANCE)
                        self.df6Tct = aux[0]
                        self.df6Afip = aux[1]

                    # Clasificacion a DATAFRAMES ya filtrados
                        dfTct['Clasificación'] = dfTct['Clasificación'] + "A CARGAR AFIP"
                        dfAfip['Clasificacion'] = dfAfip['Clasificacion'] + "A CARGAR TACTICA"
                        self.df1Tct['Clasificación'] = self.df1Tct['Clasificación'] + "MATCH EXACTO"
                        self.df1Afip['Clasificacion'] = self.df1Afip['Clasificacion'] + "MATCH EXACTO"
                        self.df2Tct['Clasificación'] = self.df2Tct['Clasificación'] + "MATCH C/ TOLERANCIA ($ extranjera)" # Antes "A CARGAR AFIP ($ extranjera)"
                        self.df2Afip['Clasificacion'] = self.df2Afip['Clasificacion'] + "MATCH C/ TOLERANCIA ($ extranjera)" # Antes "ELIMINAR DEL PORTAL ($ extranjera)"
                        self.df3Tct['Clasificación'] = self.df3Tct['Clasificación'] + "MATCH C/ TOLERANCIA"
                        self.df3Afip['Clasificacion'] = self.df3Afip['Clasificacion'] + "MATCH C/ TOLERANCIA"
                        self.df4Tct['Clasificación'] = self.df4Tct['Clasificación'] + "REVISAR 'IVA'/'TOTAL'"
                        self.df4Afip['Clasificacion'] = self.df4Afip['Clasificacion'] + "REVISAR 'IVA'/'TOTAL'"
                        self.df5Tct['Clasificación'] = self.df5Tct['Clasificación'] + "REVISAR 'CUIT'"
                        self.df5Afip['Clasificacion'] = self.df5Afip['Clasificacion'] + "REVISAR 'CUIT'"
                        self.df6Tct['Clasificación'] = self.df6Tct['Clasificación'] + "REVISAR 'N° FC'"
                        self.df6Afip['Clasificacion'] = self.df6Afip['Clasificacion'] + "REVISAR 'N° FC'"

                    # Uno todos los filtros en un mismo DF
                        newColumnNamesAfip.remove('Clasificacion')
                        newColumnNamesTct.remove('Clasificación')

                        dfAfip = pd.concat([dfAfip, self.df2Afip, self.df6Afip, self.df4Afip, self.df5Afip, self.df1Afip, self.df3Afip], ignore_index = True)
                        self.dfAfip = dfAfip.drop_duplicates(subset=newColumnNamesAfip, keep = 'last')
                        dfTct = pd.concat([dfTct, self.df2Tct, self.df6Tct, self.df4Tct, self.df5Tct, self.df1Tct, self.df3Tct], ignore_index = True)
                        self.dfTct = dfTct.drop_duplicates(subset=newColumnNamesTct, keep = 'last')

                        #Creamos dataframe con diferencias
                        sumIVATct = self.dfTct['IVA Tactica'].sum()
                        sumIVAAfip = (self.dfAfip['IVA']*self.dfAfip['Tipo Cambio']).sum()
                        
                        dataDif = {'IVA Tactica':[sumIVATct], 'IVA Afip':[sumIVAAfip], 'Diferencia':[sumIVATct-sumIVAAfip]}
                        self.dfDif = pd.DataFrame(dataDif)
                        dataframes = {"Resumen IVA":self.dfDif, "Libro Táctica":self.dfTct, "Libro AFIP": self.dfAfip}
                        self.dataframes_export(dataframes)
                else:
                    # Si no hay LIBRO IVA de TACTICA o el df de AFIP está vacío
                    sumIVATct = 0
                    sumIVAAfip = 0
                    if not file_libro_tct:
                        # Si no hay LIBRO IVA de TACTICA
                        print("\nNo hay 'Libro IVA Tactica'. Si faltó agregar el archivo, agregarlo y luego ejecutar función 3.")
                        DF_TCT_EMPTY = {'Clasificación':[],
                                        'Fecha Emisión':[],
                                        'Nº Compra':[],
                                        'Tipo Tactica':[],
                                        'Fecha Registración':[],
                                        'Fecha Creación':[],
                                        'Razón Social':[],
                                        'CUIT':[],
                                        'Condición de Compra':[],
                                        'Escenario':[],
                                        'CAI':[],
                                        'SubTotal':[],
                                        'SubTotal Neto No Gravado':[],
                                        'SubTotal Neto Exento':[],
                                        'SubTotal Neto 3 %':[],
                                        'SubTotal Neto 10,5 %':[],
                                        'SubTotal Neto 21 %':[],
                                        'SubTotal Neto 27 %':[],
                                        '3%':[],
                                        '10,5 %':[],
                                        '21%':[],
                                        '27%':[],
                                        'Otras Alicuotas':[],
                                        'Impuestos Internos':[],
                                        'Otro':[],
                                        'Percepción IIBB (ventas) Buenos Aires':[],
                                        'Percepción IIBB CABA (Ventas) CABA':[],
                                        'Percepcion IVA Buenos Aires':[],
                                        'Percepcion Santa Fe Santa Fe':[],
                                        'Percepcion IIBB (Compras) Buenos Aires':[],
                                        'Percepción IIBB CABA (Compras)':[],
                                        'IMP IIBB SIRCREB':[],
                                        'Otras Percepciones':[],
                                        'Total Tactica':[],
                                        'IVA Tactica':[]
                        }

                        # Si no se convierte a str, tira error la funcion de filtros
                        # de clasificaciones para los mails, porq tienen que ser str
                        # los datos para filtrar, por default no lo son cuando está
                        # sin datos la columna. Decimos especificamente que no hay datos
                        # para evitar este problema
                        self.dfTct = pd.DataFrame(DF_TCT_EMPTY)
                        self.dfTct.loc[0,"Clasificación"] = "NO HAY DATOS"
                    else:
                        # Si hay dfTct
                        # Formato al DataFrame Tactica
                        dfTct = pd.read_excel(self.pathTct)
                        filaInicialDFTct = dfTct[dfTct.eq(self.fechaTct).any(1)].index[0] + 1
                        filaFinalDFTct = dfTct[dfTct.eq('TOTALES').any(1)].index[0] - 1
                        newColumnNamesTct = dfTct.iloc[filaInicialDFTct - 1].to_list() # Tomo valores de fila de nueva cabecera y los convierto en lista (array)
                        #Convertimos a STRING todos los elementos de las nuevas etiquetas columnas, porque hay algunos que no lo son (21%, 27%)
                        for item in range(len(newColumnNamesTct)):
                            newColumnNamesTct[item] = str(newColumnNamesTct[item])
                            if newColumnNamesTct[item] in ['Tipo', 'Total', '0.21', '0.27', 'IVA', '0.03']:
                                newColumnNamesTct[item] = self.switch_Tct_Cols(newColumnNamesTct[item])
                        # Ahora si se puede asignar
                        dfTct.columns = newColumnNamesTct # Con la lista, puedo asignar las nuevas etiquetas a las columnas
                        dfTct = dfTct.iloc[filaInicialDFTct:filaFinalDFTct + 1] # Tomo las filas del DF que tienen los registros
                        #CUIT formato AFIP, IVA en formato AFIP (columna que sume total de los IVA)
                        dfTct['CUIT'] = dfTct['CUIT'].str.replace('-','')
                        dfTct['CUIT'] = dfTct['CUIT'].str.replace('/','')
                        dfTct['CUIT'] = dfTct['CUIT'].astype(float)
                        dfTct = dfTct.replace(" ", 0)
                        if self.empresa == "DECORMEC SA":                            
                            dfTct['IVA Tactica'] = dfTct['3%'] + dfTct['10,5 %'] + dfTct['21%'] + dfTct['27%']
                        else:                            
                            dfTct['IVA Tactica'] = dfTct['10,5 %'] + dfTct['21%'] + dfTct['27%']
                        #Clave convertirlo en Float a los valores porque sino queda como datatype "Object" y no se puede aplicar los metodos de nummpy para valores con tolerancia
                        dfTct[["IVA Tactica", "Total Tactica"]] = dfTct[["IVA Tactica", "Total Tactica"]].astype(float)
                        #Agregamos columna Clasificacion a los dataframes
                        dfTct.insert(0, 'Clasificación', "")
                        dfTct['Clasificación'] = dfTct['Clasificación'] + "A CARGAR AFIP"
                        self.dfTct = dfTct

                        sumIVATct = self.dfTct['IVA Tactica'].sum()


                    if dfAfip.empty:
                        # Si el df de AFIP está vacío
                        print("\n'Libro IVA AFIP' vacío.")
                        # Si no se convierte a str, tira error la funcion de filtros
                        # de clasificaciones para los mails, porq tienen que ser str
                        # los datos para filtrar, por default no lo son cuando está
                        # sin datos la columna. Decimos especificamente que no hay datos
                        # para evitar este problema
                        dfAfip.loc[0,"Clasificacion"] = "NO HAY DATOS"

                    else:
                        dfAfip['Clasificacion'] = dfAfip['Clasificacion'] + "A CARGAR TACTICA"
                        sumIVAAfip = (dfAfip['IVA']*dfAfip['Tipo Cambio']).sum()
                        

                    dataDif = {'IVA Tactica':[sumIVATct], 'IVA Afip':[sumIVAAfip], 'Diferencia':[sumIVATct-sumIVAAfip]}
                    self.dfDif = pd.DataFrame(dataDif)
                    self.dfAfip = dfAfip
                    dataframes = {"Resumen IVA":self.dfDif, "Libro Táctica":self.dfTct, "Libro AFIP":self.dfAfip}
                    self.dataframes_export(dataframes)

                break # Para salir de la función 'dataframes_comparison' al terminarse

            except FileNotFoundError:
                print("\n### ERROR ###: No se encuentran los archivos en el directorio correspondiente")
                input(f"\nEn caso de estar, revisar que los archivos correspondan a {self.empresa}.\nPresione 'ENTER' para continuar...")
                # sys.exit(1)
            # except:
            #     # Se pone un input y no print porque sino entra de nuevo a la función (x el while true) y salta todo el tiempo el error en la consola
            #     print("\n### ERROR ###: Revisar que las tablas tengan el formato original")
            #     input(f"\nRevisar que los archivos correspondan a {self.empresa}.\nPresione 'ENTER' para continuar...")


    def pventa(self, int):
        int = str(int)
        length = len(int)
        return ("0"*(5-length))+int

    def ndesde(self, int):
        int = str(int)
        length = len(int)
        return ("0"*(8-length))+int

    def switch_Tct_Cols(self, column):
        switch = {
            'Tipo': 'Tipo Tactica',
            'Total':'Total Tactica',
            '0.21':'21%',
            '0.27':'27%',
            '0.03':'3%'
        }
        return switch[column]

    def filter_errors(self, columnas, dataframe, fields):
        flag = False
    # primero gurado en vector "camposErrores" los campos donde hay que buscar los errores
        for i in columnas:
            if i in fields:
                if flag == True:
                    camposErrores.append(i)
                else:
                    camposErrores = [i]
                    flag = True

        # Este if flag == True es clave porque si esta en False significa que no se creó la variable (por ej se liquida Pebeire), entonces ahi no tiene que buscar errores
        if flag == True:
            filterErrores = 0
            for x in camposErrores:
                filterErrores = dataframe[x] > 0
                dataframe.loc[filterErrores, 'Clasificación'] = "POTENCIAL ERROR - "

        return dataframe


    def drop_filtered_rows(self, dataframes, columns):
        newDataframe = pd.concat(dataframes)
        newDataframe = newDataframe.drop_duplicates(subset = columns, keep = False)
        return newDataframe

    def filter_merge(self, left, right, columnsTct, columnsAfip, dfTct, dfAfip):
        # Args: cols a comparar del left df, cols a comparar del right df, todas las cols del df tct, todas las cols del df afip, left df, right df
        df = pd.merge(dfTct, dfAfip, left_on=left, right_on=right)
        newDfTct = df.loc[:, columnsTct].copy()
        newDfAfip = df.loc[:, columnsAfip].copy()
        return newDfTct, newDfAfip

    def filter_tolerance(self, dfTct, dfAfip, tol):
        #necesito definir listas porque el ".values[]" en el Dataframe Afip no se puede aplicar a una operación matematica, pero si a una lista (que sería el resultado de la multiplicacion"
        list1 = dfAfip['IVA']*dfAfip['Tipo Cambio']
        list2 = dfAfip['Total']*dfAfip['Tipo Cambio']

        # Dataframe Tactica
        # mask1 = np.isclose(dfTct['IVA Tactica'].values[:, None], list1, atol=tol).any(1)
        # mask2 = np.isclose(dfTct['Total Tactica'].values[:, None], list2, atol=tol).any(1)
        mask1 = np.isclose(dfTct['IVA Tactica'].values[:, None], list1, atol=tol)
        mask2 = np.isclose(dfTct['Total Tactica'].values[:, None], list2, atol=tol)
        dfTct = dfTct[mask1 & mask2].copy()

        # Dataframe Afip
        # mask1 = np.isclose(list1.values[:, None], dfTct['IVA Tactica'], atol=tol).any(1)
        # mask2 = np.isclose(list2.values[:, None], dfTct['Total Tactica'], atol=tol).any(1)
        mask1 = np.isclose(list1.values[:, None], dfTct['IVA Tactica'], atol=tol)
        mask2 = np.isclose(list2.values[:, None], dfTct['Total Tactica'], atol=tol)
        dfAfip = dfAfip[mask1 & mask2].copy()

        return dfTct, dfAfip


    def dataframes_export(self, dataframes):
    #modulo tiene que ser ó "Ventas" o "Compras"}
        while True:
            try:
                with pd.ExcelWriter(self.exportPath) as writer:
                    for sheet in dataframes.keys():
                        self.styling_df(dataframes[sheet], sheet, writer)
                    # writer = pd.ExcelWriter(self.exportPath)
                    #
                    # self.styling_df(dfDif, "Resumen IVA", writer)
                    # self.styling_df(dfTct, "Libro Táctica", writer)
                    # self.styling_df(dfAfip, "Libro Afip", writer)
                    # self.dfNotas.to_excel(writer, sheet_name="notas", index=False)
                    #
                    # writer.save()
                print(f"\n### ARCHIVO GENERADO ### 'IVA {self.modulo}'. Ya se puede ver la comparacion de los registros.")
                break

            except PermissionError:
                input(f'\n### ERROR ### Por favor, cerrar archivo Excel "IVA {self.modulo}".\nPresione "ENTER" para continuar' )
