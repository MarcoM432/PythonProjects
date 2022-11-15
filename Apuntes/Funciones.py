adjective = "fantastico"

def use_global_variable():
    print("Python es " + adjective)

use_global_variable()

#Jerarquia de las variables en las funciones

adjective = "divertido"

def use_local_variable_value():
    adjective = "fantastico"
    print("Python is " + adjective)

use_local_variable_value()
