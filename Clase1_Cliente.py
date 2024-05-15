#IMPORTAR LIBRERIAS
from datetime import datetime
from enum import Enum


formato_fecha = "%d/%m/%Y"

#CLASE CLIENTE, SE RELACIONA CON VENTA
class Cliente():  
    
    def __init__(self, id = 0, nombre = '', fecha_nacimiento = '', residencia = ''):
        self.id               = id
        self.nombre           = nombre
        self.fecha_nacimiento = fecha_nacimiento
        self.residencia       = residencia
        self._ID_pinacoteca   = set()
        self._ID_venta        = set()
    
    #DECORADOR DE ID
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        if id <= 0:
            print("ID No valido")
            return None
        self._id = id
    
    #DECORADOR DE NOMBRE
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, nombre):
        if nombre == '':
            self._nombre = ''
            return
        if not nombre.isalpha():
            print("El nombre no corresponde a valores alfabeticos")
            return None
        self._nombre = nombre
    
    #DECORADOR DE FECHA DE NACIMIENTO
    @property 
    def fecha_nacimiento(self):
        return self._fecha_nacimiento
    
    @fecha_nacimiento.setter 
    def fecha_nacimiento(self, fecha_nacimiento):
        if fecha_nacimiento == '':
            self._fecha_nacimiento = ''
            return
        try:
            #VALIDAR QUE TENGA EL FORMATO CORRECTO
            fecha_obj = datetime.strptime(fecha_nacimiento, formato_fecha)
            #VALIDAR QUE EL CLIENTE SEA MAYOR DE EDAD
            año_actual = datetime.now().year
            if fecha_obj.year > (año_actual-18):
                print("El cliente no es mayor de edad")
                return None
            self._fecha_nacimiento = fecha_nacimiento
        except:
            print("El formato de la fecha de nacimiento no es correcto")
            return None
    
    #DECORADOR DE RESIDENCIA
    @property
    def residencia(self):
        return self._residencia
    
    @residencia.setter
    def residencia(self, residencia):
        if residencia == '':
            self._residencia = ''
            return
        if not residencia.isalpha():
            print("La residencia no corresponde a valores alfabeticos")
            return None
        self._residencia = residencia
    
    #METODO PARA RELACIONAR LOS CLIENTES CON PINACOTECAS
    def __relacion__(self, bd):
        while True:
            try: 
                print("Desea relacionar al Cliente añadido con alguna Pinacoteca:\n\tSI\t1\n\tNO\t0\n")
                ans = int(input("Seleccione una opcion: "))
                if ans == 1:
                    add_id = self.__ids__('pinacoteca', bd)
                    for i in add_id:
                        self._ID_pinacoteca.add(i)
                elif ans == 0:
                    break
            except: 
                pass
        
    #METODO PARA OBTENER ID
    def __ids__(self, entidad, bd):
        print('\tIngrese los IDs de la {}\n\t (0 - Salir)\n'.format(entidad))
        #SE CREA EL NOMBRE DE LA ENTIDAD PARA OBTENER LOS ID'S REGISTRADOS EN LA BD
        entidad_str = entidad + 's'
        #SE CREAN LISTAS TEMPORALES PARA AÑADIR Y REGISTRAR LOS ID'S
        ids = set(); id_add = set();
        #SE OBTIENE UN LISTA CON LOS ID'S EXISTENTES EN LA BD
        for obj in bd[entidad_str]:
            ids.add(obj.id)

        while True:
            id_t = {(int(input("\tIngrese ID: \t")))}
            if id_t.issubset({0}):
                break
            elif not(id_t.issubset(ids)):
                print("ID de {} no existente, ingrese un ID existente".format(entidad))
            else:
                id_add.add(*id_t)
                bd[entidad_str][int(*id_t)-1]._ID_clientes.add(self._id)
                
        return id_add
        
    def __baja__(self, bd, id_t):
        
        self.__restartrel__(bd)
        self._borrado         = 1
    
    def __restartrel__(self, bd):
        
        for i in range(len(bd['pinacotecas'])):
            try:
                bd['pinacotecas'][i]._ID_clientes.discard(self._id)
            except:
                pass
            
        self._nombre           = None
        self._fecha_nacimiento = None
        self._residencia       = None
        self._ID_pinacoteca    = None
        self._ID_venta         = None
    
    def __modificacion__(self, bd, id_t):
        self.__restartrel__(bd)
        
        while True:
            self.nombre           = input("\tIngrese Nombre:              ")
            self.fecha_nacimiento = input("\tIngrese Fecha de Nacimiento: ")
            self.residencia       = input("\tIngrese Residencia:          ")
            if not(self._nombre == None or self._fecha_nacimiento == None or self._residencia == None):
                break
        self._ID_pinacoteca   = set()
        self._ID_venta        = set()
            
        self.__relacion__(bd)
       
    def __str__(self) -> str:
        return (
                f" ID:                  {self._id}\n"
                f" Nombre:              {self._nombre}\n"
                f" Fecha de Nacimiento: {self._fecha_nacimiento}\n"
                f" Residencia:          {self._residencia}\n"
                f" El cliente pertence a:\n"
                f" La(s) pinacotecas:   {self._ID_pinacoteca}\n"
                f" Las ventas:          {self._ID_venta}"
            )

 


'''
try:
    prueba = Cliente()._alta()
    
    print(prueba)
except:
    pass   
ERRORES
    AttributeError
    NameError
    TypeError
'''
