#Crea la clase Persona, clase padre de Pintor y Mecenas
import datetime
class Persona:
    
    def __init__(self, id, nombre):
        self._id = id
        self._nombre = nombre
        self._pais = None
        self._ciudad = None
        self._fallecimiento = None
        
#Getter    
    @property
    def id(self):
        return self._id
    
#Setter, verificaciones    
    @id.setter
    def id(self,id):
        if id>0:             #ejemplo de verificación
            self._id = id

#Getter    
    @property
    def nombre(self):
        return self._nombre
    
#Setter, verificaciones    
    @nombre.setter
    def nombre(self,nombre):
        if not isinstance(nombre, str):
            raise ValueError("Escriba el nombre sin caracteres especiales")         #verificación
            
#Getter    
    @property
    def pais(self):
        return self._pais
    
#Setter, verificaciones    
    @pais.setter
    def pais(self,pais):
        if not isinstance(pais, str):
            raise ValueError("Escriba el país sin caracteres especiales") 

#Getter    
    @property
    def ciudad(self):
        return self._ciudad
    
#Setter, verificaciones    
    @ciudad.setter
    def ciudad(self,ciudad):
        if not isinstance(ciudad, str):
            raise ValueError("Escriba la ciudad sin caracteres especiales") 

#Getter    
    @property
    def fallecimiento(self):
        return self._fallecimiento
    
#Setter, verificaciones    
    @fallecimiento.setter
    def fallecimiento(self, fallecimiento):
        if fallecimiento is not None:
            try:
                # Attempt to parse the input value as a date
                fecha_parchada = datetime.date.strptime(fallecimiento, "%Y-%m-%d").date()
                self.fallecimiento = fecha_parchada
            except ValueError:
                raise ValueError("Invalid date format. Please use YYYY-MM-DD.")
        else:
            self._date_of_birth = None