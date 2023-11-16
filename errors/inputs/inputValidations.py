# Standard library imports

# Third party imports

# Proyect imports
from errors.inputs.error import inputError
from menu.menu import invalid_input


# Convierto los datos a entero para poder verificar que esten en el rango de opciones. Antes evaluaba con isinstance() method si se trataba de entero, pero no tiene sentido hacerlo ya que sería redundante porque ya de por si necesito convertilo a entero para verificar que este en el rango.

# DATA MENU VALIDATION
def validation_data_menu(empresa, mes):
    try:
        empresa = int(empresa)
        mes = int(mes)
        if validate_range_main(empresa, mes):
            return True
        else:
            raise inputError()
    except inputError as error:
        print(error.message)
    except ValueError:
        invalid_input()

def validate_range_main(empresa, mes):
    return empresa > 0 and empresa < 6 and mes > 0 and mes < 13

# BANK MENU VALIDATION
def validation_operations_menu(input, number):
    try:
        input = int(input)
        if validate_range_operations(input, number):
            return True
        else:
            raise inputError()
    except inputError as error:
        print(error.message)
    except ValueError:
        invalid_input()

def validate_range_operations(input, number):
    return input > 0 and input < number



# FUNCTION MENU VALIDATION




# ROAD TO OPTIMIZACION
# MAIN MENU VALIDATION
# def validation_main_menu(empresa, mes, year):
#     integers = validate_integer([empresa, mes, year])
#     # print(integers)
#     condition = validate_range_main(integers)
#     return validate_value(condition)
#
# def validate_range_main(integers):
#     # empresa = integers[0] / mes = integers[1] / year = integers[2]
#     return integers[0] > 0 and integers[0] < 6 and integers[1] > 0 and integers[1] < 13 and integers[2] > 0 and integers[2] < 3
#
#
#
#
# # BANK MENU VALIDATION
# def validation_bank_menu(input):
#     integer = validate_integer(input)
#     condition = validate_range_bank(integer)
#     return validate_value(condition)
#
# def validate_range_bank(integer):
#     return integer > 0 and integer < 3
#
#
#
# # FUNCTIONS MENU VALIDATION
#
#
#
#
#
#
# # Aux functions
#
# # validation integer
# def validate_integer(inputs):
#         # print(inputs)
#         integers = []
#         for value in inputs:
#             try:
#                 # print(value)
#                 value = int(value)
#                 # suma = 'asd' + 'asd1111'
#                 # print(integers)
#             except ValueError:
#                 invalid_input()
#             integers.append(value)
#         return integers
#
# # validation value
# def validate_value(condition):
#     try:
#         if condition:
#             return True
#         else:
#             raise inputError()
#     except inputError as error:
#         print(error.message)
