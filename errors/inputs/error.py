class inputError(Exception):
    def __init__(self):
        self.message ="\n-VALOR INVALIDO- El valor ingresado debe ser un número entero presente en las opciones.\n"
        # print("\n-VALOR INVALIDO- El valor ingresado debe ser un número entero presente en las opciones.\n")

    def __str__(self):
        return(self.message)
