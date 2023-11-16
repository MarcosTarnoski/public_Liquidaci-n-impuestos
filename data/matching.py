# Proyect imports
from data.directory import directory

compras = {
    'errorFields' : ["Otras Alicuotas",
                     "IVA RETENIDO",
                     "Impuestos Internos",
                     "Percepción IIBB (ventas) Buenos Aires",
                     "Percepción IIBB CABA (Ventas) CABA",
                     "Otro",
                     "Percepcion IIBB (ventas) Buenos Aires",
                     "Otras Percepciones",
                     "Percepcion Santa Fe Santa Fe",
                     "Percepcion IIBB CABA (ventas) CABA"
    ],
    'pathTct' : f'{directory}\\paperworks\\Libro1.xlsx',
    'nDocAfip' : 'Nro. Doc. Vendedor',
    'nComprobante' : 'Nº Compra',
    'exportPath' : f'{directory}\\IVA Compras - ',
    'pathAfip' : f'{directory}\\paperworks\\Comprobantes de Compras - CUIT ',
    'fechaTct' : 'Fecha Emisión'
}

ventas = {
    'errorFields' : ["Percepcion IIBB CABA (ventas) CABA",
                     "Percepción IIBB CABA (Ventas) CABA",
                     "Otros","Percepcion IIBB (Compras) Buenos Aires",
                     "Percepcion IIBB CABA (Compras)",
                     "Otras Percepciones",
                     "IMP IIBB SIRCREB",
                     "Percepcion IIBB Mendoza Mendoza",
                     "IIBB PERCEPCION MENDOZA Mendoza",
                     "IVA RETENIDO",
                     "Percepcion Santa Fe Santa Fe",
                     "Percepción IIBB CABA (Compras)",
                     "Percepciones IVA Buenos Aires"
    ],
    'pathTct' : f'{directory}\\paperworks\\Libro2.xlsx',
    'nDocAfip' : 'Nro. Doc. Comprador',
    'nComprobante' : 'Nº Factura',
    'exportPath' : f'{directory}\\IVA Ventas - ',
    'pathAfip' : f'{directory}\\paperworks\\Comprobantes de Ventas - CUIT ',
    'fechaTct' : 'Fecha de Emisión'
}


notas = {"NOTAS": ["VERDE: coincidencia EXACTA de campos 'N°FC', 'CUIT'. 'TOTAL' e 'IVA' coincidencia EXACTA o coincidencia con TOLERANCIA de +-1.50", 
                   "NARANJA: 'CUIT' o 'N° FACTURA' diferentes. Coincidencia dentro de tolerancia +-1.50 campos 'TOTAL' e 'IVA'",
                   "AMARILLO: 'TOTAL' y/o 'IVA' fuera del rango de tolerancia. Coincidencia EXACTA de 'N°FC', 'CUIT'",
                   "POTENCIAL ERROR: hay importes en 'Percepcion IIBB CABA (ventas) CABA','Percepción IIBB CABA (Ventas) CABA', 'Otros', 'Percepcion IIBB (Compras) Buenos Aires', 'Percepcion IIBB CABA (Compras)', 'Otras Percepciones','IMP IIBB SIRCREB (en ventas)','Percepcion IIBB Mendoza Mendoza','IIBB PERCEPCION MENDOZA Mendoza','IVA RETENIDO','Percepcion Santa Fe Santa Fe','Percepción IIBB CABA (Compras)','Percepciones IVA Buenos Aires', 'Impuestos Internos','Otro','Otros','Otras Percepciones','Percepcion Santa Fe Santa Fe'",
                   "VALORES DUPLICADOS: si se detectan valores duplicados, eliminar aquellos que no correspondan y volver a ejecutar Liquidación. Este error compara columnas 'Tipo Factura', 'N°FC'y 'CUIT' de tablas AFIP y TACTICA (no revisa importes ya que puede haber error de decimales en la carga de facturas)",
                   "Se generará txt de aquellos registros de táctica que en 'Clasificación' = 'A CARGAR AFIP'",
                   "Cerrar archivos Excel antes de ejecutar el programa"
        ]
}
