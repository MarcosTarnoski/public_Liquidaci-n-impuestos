# Proyect imports
from data.directory import directory

#En realdidad los path corresponden a la parte de los libros y no a la navegacion hasta llegar al portal, osea son de distintas paginas.
#pero asi se simplifica un poco el codigo de los tests. Sino se hacia mas compleja en vano la parte de "test_upload_txts"

compras = {
'btnLibro':'btnLibroCompras',
'urlLibro':'https://serviciosjava2.afip.gob.ar/liva/jsp/verCompras.do?t=21',
'pathTxtCte':f'{directory}\\LIBRO_IVA_DIGITAL_COMPRAS_CBTE.txt',
'pathTxtAlic':f'{directory}\\LIBRO_IVA_DIGITAL_COMPRAS_ALICUOTAS.txt'
}

ventas = {
'btnLibro':'btnLibroVentas',
'urlLibro':'https://serviciosjava2.afip.gob.ar/liva/jsp/verVentas.do?t=31',
'pathTxtCte':f'{directory}\\LIBRO_IVA_DIGITAL_VENTAS_CBTE.txt',
'pathTxtAlic':f'{directory}\\LIBRO_IVA_DIGITAL_VENTAS_ALICUOTAS.txt'
}
