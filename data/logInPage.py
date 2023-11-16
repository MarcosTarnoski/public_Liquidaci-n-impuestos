ADRESSES_COMPRAS = ['testmail1@gmail.com.ar', 'testmail2@gmail.com.ar']
ADRESSES_VENTAS = ['testmail4@gmail.com.ar','testmail3@gmail.com.ar']

def switch_empresa(numero):
    switch = {
        '1': ['ID1', 'CUIT1', 'DECORMEC SA', {'adressCompras':ADRESSES_COMPRAS,'adressVentas': ADRESSES_VENTAS}],
        '2': ['ID2', 'CUIT2', 'WENTEK SA', {'adressCompras':ADRESSES_COMPRAS,'adressVentas': ADRESSES_VENTAS}],
        '3': ['ID3', 'CUIT3', 'MI ESQUINA SA', {'adressCompras':ADRESSES_COMPRAS,'adressVentas':['testmail3@gmail.com.ar']}],
        '4': ['ID4', 'CUIT4', 'IKAIKA S.A.', {'adressCompras':['testmail1@gmail.com.ar', 'testmail3@gmail.com.ar'],'adressVentas':['testmail1@gmail.com.ar','testmail3@gmail.com.ar']}],
        '5': ['ID5', 'CUIT5', 'PEBEIRE S.A.', {'adressCompras':ADRESSES_COMPRAS,'adressVentas': ADRESSES_VENTAS}]
    }
    return switch[numero]