dataframes = {"Resumen IVA":"df DIFERENCIA", "Libro Táctica":"df TACTICA", "Libro AFIP": "df AFIP"}

for sheet in dataframes.keys():
    print("NOMBRE HOJA: ", sheet)
    print("dataframe: ", dataframes[sheet])
