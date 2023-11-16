# Standard imports
import os
import shutil

# Third imports

# Proyect imports
from data.oldfiles import folderPath


def create_folder():
    if not os.path.isdir(folderPath):
    # Si no está la carpeta la creo. Verifico esto porque puede ser que ya haya sido creada en otra ejecucion del test "test_upload_txts"
        os.mkdir(folderPath)


def move_files(path):
    while True:
        try:
            # For porque pueden ser archivos de compras y ventas
            for item in path:
            # Verifico que este el archivo antes de moverlo. Puede ser que me lo hayan tocado/cambiado por ejemplo y me tiraria error el programa en ese caso
                if os.path.isfile(item):
                    fileName = item[item.rfind('\\')+1:]
                    target = item[:-len(fileName)]
                    fileName = fileName.replace('.xlsx', ' (old).xlsx')
                    if "paperworks" in target:
                        target = target+"LIQUIDACION INICIAL\\"+fileName
                    else:
                        target = target+"paperworks\\LIQUIDACION INICIAL\\"+fileName
                    shutil.move(item, target)
            break
        except PermissionError:
            input("### ERROR ### - Cerrar archivos excel abiertos.\nPresione 'ENTER' para continuar...")
