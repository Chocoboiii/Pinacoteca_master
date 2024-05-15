"""
Name 
    SGP: Sistema Gestor de Pinacotecas

Description
    El Sistema Gestor de Pinacotecas ayuda a gestionar la administración de diferentes
    pinacotecas. Principalmente la gestión de de cuadros, pintores, mecenas, clientes,
    escuelas, maestros y ventas.
    Para que el programa funcione, necesita la instalacion del modulo country_list,
    Busque el simbolo del sistema y escriba "pip install country_list" para instalarlo
    
"""
#PROGRAMA PRINCIPAL DE LA BASE DE DATOS DE UNA PINACOTECA

#IMPORTAR LA CLASE QUE FUNGE COMO SISTEMA GESTOR DE PINACOTECA
from Clase0_SGP import SGP


WELCOME_HEADER = "Sistema Gestor de Pinacotecas"
INSTRUCTION = "Por favor seleccione una de las siguientes opciones:"

def main():
    print("\n{header}\n".format(header=WELCOME_HEADER))
    
    #SE CREA UNA CLASE SGP
    sgp = SGP()
    
    #SE LLAMA AL METODO "ejecutar()" DE LA CLASE sgp CREADA
    sgp.ejecutar()

   
if __name__ == "__main__":
    main()