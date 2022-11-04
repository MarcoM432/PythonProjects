#variables globales sin hacer uso de palabra "global"

from unicodedata import name


variable_global ="Hola mundo"

def custom_function():
    print(variable_global)

print("Fuera: "+ variable_global)

#llamar a la funcion para ejecutarla

custom_function()


variable_global1 ="Hola mundo"

def custom_function1():
    variable_global1 = "Marco Mulgado"
    print(variable_global1)

print("Fuera: "+ variable_global1)

#llamar a la funcion para ejecutarla

custom_function1()

#Variables Globales
name ="MS"
def use_global_function_value():
    global name
    name = "Marco Marco Marco"


use_global_function_value()
print("Name: "+ name)
print(name)