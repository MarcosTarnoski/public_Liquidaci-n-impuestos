# Standard library imports
import sys

# Third party imports

# Proyect imports


def main_menu():
    print('¡HOLA! Soy ROBYCOOP912. Te voy a ayudar con la LIQUIDACIÓN del IVA.\n')
    print('1) DECORMEC\n2) WENTEK\n3) MI ESQUINA\n4) IKAIKA\n5) PEBEIRE\n')
    print('1) Enero\n2) Febrero\n3) Marzo\n4) Abril\n5) Mayo\n6) Junio\n7) Julio\n8) Agosto\n9) Septiembre\n10) Octubre\n11) Noviembre\n12) Diciembre\n')

def selected_option_main(empresa, mes):
    print(f"\n\n¡PERFECTO!. Elegiste {empresa}, MES {mes}.")

def operations_menu():
    print("\n\n1) Liquidación desde inicio\n2) Descarga de archivos\n3) Comparar excels COMPRAS y VENTAS\n4) Generar txts\n5) Subir txts a AFIP\n6) Generar excel 'MODIFICACIONES TACTICA' y enviar mail\n7) Salir\nSi desea cambiar de empresa, cerrar y volver a abrir la aplicación.\n")

def invalid_input():
    print("\n-VALOR INVALIDO- El valor ingresado debe ser un número entero presente en las opciones.\n")

def upload_txts_menu():
    print("\n¿Se importaran a AFIP facturas en dolares?")
    # print("¿Los archivos de TACTICA tienen los registros actualizados?\n")

def error_objects():
    print("\n### OBJECT NOT CREATED ERROR ### No ejecutar funciones que requieren pasos previos")

def finished_operation():
    print("\n## OPERACIÓN SOLICITADA FINALIZADA ##")

def salir():
    input("\nEJECUCION FINALIZADA. CERRAR PROGRAMA Y VOLVER A EJECUTAR SI LO DESEA.")
    sys.exit(0)
