# Standard library imports

# Third party imports

# Proyect imports
from data import logInPage, txt
from tests import test_afip
from dataprocessing.excelmatch import excelProcessing
from dataprocessing.txtgen import txtGenerator
from dataprocessing.oldFiles import create_folder, move_files
from dataprocessing.xlsxMail import regPendientes
from data import portalIVA    # Lo necesito para la parte de upload_txts
from menu import menu
from emails.mailing import send_email
from errors.inputs import inputValidations as iv

# *********** PRESENTACION ***********
# Primero consultamos de qué empresa se trata para ingresar el CUIT y saber despues el "changeRelation".

def main():
    menu.main_menu()

    while True:
        # main menu
        empresa = input('Indica el NUMERO de empresa a liquidar: ')
        mes = input('Mes a liquidar: ')

        if iv.validation_data_menu(empresa, mes):
            datosEmpresa = logInPage.switch_empresa(empresa)
            mes = txt.switch_mes(mes)
            menu.selected_option_main(datosEmpresa[2], mes)

            while True:
                # Validados los input, pasamos a ver que funcion se ejecutará.
                # operations menu
                # menu.operations_menu()
                # option = input("Ingrese opción: ")
                option = "1"

                if iv.validation_operations_menu(option, 8):
                    # try:
                        if option == '1':
                        # LIQUIDACIÓN DESDE INICIO

                            # *********** DESCARGA DE ARCHIVOS AFIP ***********
                            # afip = test_afip.testsAfip(datosEmpresa[2], datosEmpresa[0], mes)
                            # afip.test_download_book("ComprasyVentas")

                            # *********** MATCHING DF ***********
                            dfCompras = excelProcessing("Compras", datosEmpresa[2], datosEmpresa[1], mes)
                            dfCompras.dataframes_comparison()
                            dfVentas = excelProcessing("Ventas", datosEmpresa[2], datosEmpresa[1], mes)
                            dfVentas.dataframes_comparison()

                                # *********** ENVIO MAIL ***********
                            # Enviar mail con archivos "MODIFICACIONES TACTICA"
                            input("\n### REPORTES EMAIL ###\nRevisar registros hoja 'Libro Afip'. Se reportarán por mail Clasificaciones:\n'A CARGAR TACTICA'\n'REVISAR CUIT'\n'REVISAR N° FC'\n'REVISAR IVA-TOTAL'.\n\nRevisar hoja 'Libro Tactica'. Se reportaran por mail registros con Clasificación:\n'POTENCIAL ERROR'\n\nPresione cualquier tecla cuando desee proceder con el envio de mails.\n")
                            ptesMailCompras = regPendientes("Compras", dfCompras.exportPath)
                            ptesMailCompras.export_pendientes()
                            ptesMailVentas = regPendientes("Ventas", dfVentas.exportPath)
                            ptesMailVentas.export_pendientes()

                            # Evalúo si se creo archivo (comparando paths), si fue creado (paths diferentes) lo envío por mail
                            if ptesMailCompras.path != dfCompras.exportPath:
                                send_email([ptesMailCompras.path], datosEmpresa[3]['adressCompras'], f'IVA Compras {datosEmpresa[2]} {mes} pendientes')
                            if ptesMailVentas.path != dfVentas.exportPath:
                                send_email([ptesMailVentas.path], datosEmpresa[3]['adressVentas'], f'IVA Ventas {datosEmpresa[2]} {mes} pendientes')

                            # *********** GENERATING TXT ***********
                            input("\nRevisar registros hoja 'Táctica', clasificacion 'A CARGAR AFIP'.\nPresione 'ENTER' cuando desee proceder con la creación de los txt.\n")
                            txtCompras = txtGenerator("Compras", mes)
                            txtCompras.generate_txt(dfCompras.exportPath)
                            txtVentas = txtGenerator("Ventas", mes)
                            txtVentas.generate_txt(dfVentas.exportPath)

                            # *********** UPLOAD TXT's ***********
                            if txtCompras.txtGenerated or txtVentas.txtGenerated:
                                # Creo directorio para guardar los archivos viejos. Primero me fijo que no este creado ya, que puede estarlo en caso que se este ejecutando la funcion de nuevo.
                                create_folder()
                                # menu.upload_txts_menu()
                                # upload menu
                                        # input("-ARCHIVOS TACTICA- Ubicar 'Libro1' y/o 'Libro2' actualizados. Presione 'ENTER' para continuar")
                                        # input("Por favor, maximizar navegador.\nPresione 'ENTER' cuando este hecho.")

                            #Evaluo cuales son los archivos a subir, paso parametros a test_upload_txts en funcion de esto y luego comparo los dataframes que fueron descargados.
                            # La evaluacion la podría hacer dentro de la misma funcion para simplificar codigo pero despues se complicaba la funcoin move_files() porque no tengo en ese archivo
                            # las direcciones sino que las tengo en un objeto creado en este main. Y para saber que dirección pasarle que busque necesito evaluar cual txt se va a subir para lo cual
                            # necesito los condicionales aca, y no es eficiente poner la evaluación de mismas condiciones tanto acá como en el test.
                            # Si le pasaba todos los datos y direcciones podia evaluarlo adentro, pero ejecutar funciones y evaluar tantas cosas ya pierde la esencia de ser un test.

                                if txtCompras.txtGenerated and txtVentas.txtGenerated:
                                    locators = [portalIVA.compras, portalIVA.ventas]
                                    move_files([dfCompras.exportPath, dfVentas.exportPath, dfCompras.pathAfip, dfVentas.pathAfip])
                                    afip.test_upload_txts(locators)
                                    dfCompras.dataframes_comparison()
                                    dfVentas.dataframes_comparison()

                                if txtCompras.txtGenerated and not txtVentas.txtGenerated:
                                    locators = [portalIVA.compras]
                                    move_files([dfCompras.exportPath, dfCompras.pathAfip])
                                    afip.test_upload_txts(locators)
                                    dfCompras.dataframes_comparison()

                                if not txtCompras.txtGenerated and txtVentas.txtGenerated:
                                    # Cuando no se trata se upload COMPRAS, no hay posibilidad de cargar facturas en dolares. Entonces le ponemos false y la funcion ya lo interpreta y no hace nada con ese dato
                                    fcdolar = False
                                    locators = [portalIVA.ventas]
                                    move_files([dfVentas.exportPath, dfVentas.pathAfip])
                                    afip.test_upload_txts(locators)
                                    dfVentas.dataframes_comparison()

                                # break


                        elif option == '2':
                        # DESCARGA DE ARCHIVOS
                            afip = test_afip.testsAfip(datosEmpresa[2], datosEmpresa[0], mes)
                            afip.test_download_book("ComprasyVentas")

                        elif option == '3':
                        # COMPRARAR ARCHIVOS EXCEL
                            # *********** COMPARING DF ***********
                            dfCompras = excelProcessing("Compras", datosEmpresa[2], datosEmpresa[1], mes)
                            dfCompras.dataframes_comparison()
                            dfVentas = excelProcessing("Ventas", datosEmpresa[2], datosEmpresa[1], mes)
                            dfVentas.dataframes_comparison()

                        elif option == '4':
                        # GENERAR TXTS
                            # *********** GENERATING TXT ***********
                            input("\nRevisar registros hoja 'Táctica', 'A CARGAR AFIP'. Presione 'ENTER' cuando desee proceder con la creación de los txt.\n")
                            txtCompras = txtGenerator("Compras", mes)
                            txtCompras.generate_txt(dfCompras.exportPath)
                            txtVentas = txtGenerator("Ventas", mes)
                            txtVentas.generate_txt(dfVentas.exportPath)

                        elif option == '5':
                        # SUBIR TXTS A AFIP
                            afip = test_afip.testsAfip(datosEmpresa[2], datosEmpresa[0], mes)
                            if txtCompras.txtGenerated or txtVentas.txtGenerated:
                                # Creo directorio para guardar los archivos viejos. Primero me fijo que no este creado ya, que puede estarlo en caso que se este ejecutando la funcion de nuevo.
                                create_folder()
                                # menu.upload_txts_menu()

                                # while True:
                                # # upload menu
                                #     fcdolar = input('-FC DOLARES- Ingrese 1 (SI) o 2 (NO): ')
                                #     if iv.validation_operations_menu(fcdolar, 3):
                                        # input("-ARCHIVOS TACTICA- Ubicar 'Libro1' y/o 'Libro2' actualizados. Presione 'ENTER' para continuar")
                                        # input("Por favor, maximice navegador\nPresione 'ENTER' cuando este hecho.")

                                # Evaluo cual es son los archivos a subir, paso parametros a test_upload_txts en funcion de esto y luego comparo los dataframes que fueron descargados.
                                # La evaluacion la podría hacer dentro de la misma funcion para simplificar codigo pero despues se complicaba la funcoin move_files() porque no tengo en ese archivo
                                # las direcciones sino que las tengo en un objeto creado en este main. Y para saber que dirección pasarle que busque necesito evaluar cual txt se va a subir para lo cual
                                # necesito los condicionales aca, y no es eficiente poner la evaluación de mismas condiciones tanto acá como en el test.
                                # Si le pasaba todos los datos y direcciones podia evaluarlo adentro, pero ejecutar funciones y evaluar tantas cosas ya pierde la esencia de ser un test.

                                if txtCompras.txtGenerated and txtVentas.txtGenerated:
                                    locators = [portalIVA.compras, portalIVA.ventas]
                                    move_files([dfCompras.exportPath, dfVentas.exportPath, dfCompras.pathAfip, dfVentas.pathAfip])
                                    afip.test_upload_txts(locators)
                                    dfCompras.dataframes_comparison()
                                    dfVentas.dataframes_comparison()

                                if txtCompras.txtGenerated and not txtVentas.txtGenerated:
                                    locators = [portalIVA.compras]
                                    move_files([dfCompras.exportPath, dfCompras.pathAfip])
                                    afip.test_upload_txts(locators)
                                    dfCompras.dataframes_comparison()

                                if not txtCompras.txtGenerated and txtVentas.txtGenerated:
                                    # Cuando no se trata se upload COMPRAS, no hay posibilidad de cargar facturas en dolares. Entonces le ponemos false y la funcion ya lo interpreta y no hace nada con ese dato
                                    locators = [portalIVA.ventas]
                                    move_files([dfVentas.exportPath, dfVentas.pathAfip])
                                    afip.test_upload_txts(locators)
                                    dfVentas.dataframes_comparison()

                                        # break


                        elif option == '6':
                            # Enviar mail con archivos "MODIFICACIONES TACTICA"
                            input("\n### REPORTES EMAIL ###\nRevisar registros hoja 'Libro Afip'. Se reportarán por mail Clasificaciones:\n'A CARGAR TACTICA'\n'REVISAR CUIT'\n'REVISAR N° FC'\n'REVISAR IVA-TOTAL'.\n\nRevisar hoja 'Libro Tactica'. Se reportaran por mail registros con Clasificación:\n'POTENCIAL ERROR'\n\nPresione cualquier tecla cuando desee proceder con el envio de mails.\n")
                            ptesMailCompras = regPendientes("Compras", dfCompras.exportPath)
                            ptesMailCompras.export_pendientes()
                            ptesMailVentas = regPendientes("Ventas", dfVentas.exportPath)
                            ptesMailVentas.export_pendientes()

                            # Evalúo si se creo archivo (comparando paths), si fue creado (paths diferentes) lo envío por mail
                            if ptesMailCompras.path != dfCompras.exportPath:
                                send_email([ptesMailCompras.path], datosEmpresa[3]['adressCompras'], f'IVA Compras {datosEmpresa[2]} {mes} pendientes')

                            if ptesMailVentas.path != dfVentas.exportPath:
                                send_email([ptesMailVentas.path], datosEmpresa[3]['adressVentas'], f'IVA Ventas {datosEmpresa[2]} {mes} pendientes')


                        elif option == '7':
                        # SALIR
                            menu.salir()

                        menu.finished_operation()

                    # except (NameError, AttributeError):
                    #     menu.error_objects()


if __name__ == "__main__":
    main()