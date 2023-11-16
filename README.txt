PRELIQUIDACION IVA APP

El aplicativo permite realizar la preliquidación del IVA. Tiene como objetivo conocer las diferencias entre el portal IVA de AFIP y el ERP y corregir parte de estas discrepancias.
Ingresa a AFIP, descarga libros digitales, los compara con los del sistema, detecta errores, los reporta a COMPRAS y VENTAS via mail. Luego sube archivos txt a AFIP con las facturas que están en el ERP pero faltan en el portal.

Instrucciones de uso.
- Ejecutar archivo main.py y proceder según sea solicitado. 
- Previo a dicha ejecución, en la carpeta 'paperworks' se deben colocar los archivos de trabajo necesarios:
    Libro1 --> LIBRO IVA COMPRAS TACTICA
    Libro2 --> LIBRO IVA VENTAS TACTICA
    reginfo_cv_compras_alicuotas_YYYYMM --> CITI COMPRAS
    reginfo_cv_compras_cbte_YYYYMM --> CITI COMPRAS
    reginfo_cv_ventas_alicuotas_YYYYMM --> CITI VENTAS
    reginfo_cv_ventas_cbte_YYYYMM --> CITI VENTAS
    Los nombres de los txt son los que genera Táctica.
- En la carpeta 'docs' se encuentra el instructivo con el detalle de las funcionalidades.


