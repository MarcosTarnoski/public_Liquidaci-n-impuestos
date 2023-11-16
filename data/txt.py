# Proyect imports
from data.directory import directory

def switch_mes(numero):
    switch = {
        '1': '202301',
        '2': '202302',
        '3': '202303',
        '4': '202304',
        '5': '202305',
        '6': '202306',
        '7': '202307',
        '8': '202308',
        '9': '202309',
        '10': '202310',
        '11': '202311',
        '12': '202312',
    }
    return switch[numero]



compras = {
'pathTxtCte': f'{directory}\\paperworks\\reginfo_cv_compras_cbte_',
'pathNewTxtCte':f'{directory}\\LIBRO_IVA_DIGITAL_COMPRAS_CBTE.txt',
'pathTxtAlic':f'{directory}\\paperworks\\reginfo_cv_compras_alicuotas_',
'pathNewTxtAlic':f'{directory}\\LIBRO_IVA_DIGITAL_COMPRAS_ALICUOTAS.txt'
}

ventas = {
'pathTxtCte':f'{directory}\\paperworks\\reginfo_cv_ventas_cbte_',
'pathNewTxtCte':f'{directory}\\LIBRO_IVA_DIGITAL_VENTAS_CBTE.txt',
'pathTxtAlic':f'{directory}\\paperworks\\reginfo_cv_ventas_alicuotas_',
'pathNewTxtAlic':f'{directory}\\LIBRO_IVA_DIGITAL_VENTAS_ALICUOTAS.txt'
}
