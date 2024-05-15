from Set_Paises import paises
from datetime import datetime
from enum import Enum

formato_fecha = "%d/%m/%Y"

class Persona:
    def _init_(self, id, nombre, pais, ciudad_nacimiento, fecha_fallecimiento):
        self._id = id
        self._nombre = nombre
        self._pais = pais
        self._ciudad_nacimiento = ciudad_nacimiento
        self._fecha_fallecimiento = fecha_fallecimiento

    # Property decorator for ID
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if value <= 0:
            print("ID No valido")
        else:
            self._id = value

    # Property decorator for nombre
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, value):
        if not (x.isalpha() or x.isspace() for x in value):
            print("El nombre no corresponde a valores alfabéticos")
        else:
            self._nombre = value

    # Property decorator for pais
    @property
    def pais(self):
        return self._pais

    @pais.setter 
    def pais(self, value):
        if value == '':
            print("El país no puede estar vacío")
        elif value not in paises:
            print("El país ingresado no se reconoce en la base de datos")
        else:
            self._pais = value

    # Property decorator for ciudad de nacimiento
    @property
    def ciudad_nacimiento(self):
        return self._ciudad_nacimiento

    @ciudad_nacimiento.setter 
    def ciudad_nacimiento(self, value):
        if not value.isalpha():
            print("La ciudad de nacimiento no corresponde a valores alfabéticos")
        else:
            self._ciudad_nacimiento = value

    # Property decorator for fecha de fallecimiento
    @property 
    def fecha_fallecimiento(self):
        return self._fecha_fallecimiento

    @fecha_fallecimiento.setter 
    def fecha_fallecimiento(self, value):
        if value == '':
            print("La fecha de fallecimiento no puede estar vacía")
        else:
            try:
                fecha_obj = datetime.strptime(value, formato_fecha)
                año_actual = datetime.now().year
                if fecha_obj.year > año_actual:
                    print("La fecha ingresada no es correcta")
                else:
                    self._fecha_fallecimiento = value
            except ValueError:
                print("El formato de la fecha de fallecimiento no es correcto")

# Example usage