#IMPORTAR LIBRERIAS
from enum import Enum

class Pinacoteca():
    def __init__(self, id = 0, nombre = '', direccion = '', ciudad = '', largo = 0, ancho = 0):
        self.id        = id 
        self.nombre    = nombre
        self.direccion = direccion
        self.ciudad    = ciudad
        self.largo     = largo
        self.ancho     = ancho
        self._area     = float(self._ancho) * float(self._largo)
        #ID'S QUE SE RELACIONAN EN ESTA CLASE
        self._ID_cuadros   = set()
        self._ID_clientes  = set()
        #ID QUE SE RELACIONAN EN OTRA CLASE
        self._ID_ventas    = set()
             
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
    
    #DECORDADORES PARA NOMBRE
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, nombre): #TODO Validar el nombre con valores alfabeticos
        if nombre == '':
            self._nombre = ''
            return
        if not nombre.isalpha():
            print("El nombre no corresponde a valores alfabeticos")
            return None
        self._nombre = nombre
        
    #DECORADORES PARA DIRECCIÓN
    @property
    def direccion(self): 
        return self._direccion
    
    @direccion.setter
    def direccion(self, direccion): #TODO Validar la direccion con caracteres alfanuméricos
        if direccion == '':
            self._direccion = ''
            return
        if not direccion.isalnum():
            print("La dirección no corresponde a un valor alfanunmérico")
            return None
        self._direccion = direccion
    
    #DECORADORES PARA CIUDAD
    @property
    def ciudad(self):
        return self._ciudad
    
    @ciudad.setter 
    def ciudad(self, ciudad):
        if ciudad == '':
            self._ciudad = ''
            return
        if not ciudad.isalnum():
            print("La ciudad no corresponde a valores alfabeticos")
            return None
        self._ciudad = ciudad
        
    #DECORADORES PARA LARGO
    @property
    def largo(self):
        return self._largo
    
    @largo.setter 
    def largo(self, largo):
        if largo == 0:
            self._largo = 0
            return
        try:    
            float(largo)
            self._largo = largo
        except: 
            print("El largo ingresado no es correcto")
            return None
        
    #DECORADORES PARA ANCHO
    @property 
    def ancho(self):
        return self._ancho
    
    @ancho.setter
    def ancho(self, ancho):
        if ancho == 0:
            self._ancho = 0
            return
        try:
            float(ancho)
            self._ancho = ancho
        except:
            print("El ancho ingresado no es correcto")
            return None
    
    #METODO PARA RELACIONAR LA PINCOTECA CON OTRAS IDENTIDATES
    def __relacion__(self, bd):
        while True:
            try: 
                print("Desea relacionar la pinacoteca añadida con Cuadros, Clientes o Ventas:\n\tSI\t1\n\tNO\t0\n")
                ans = int(input("Seleccione una opcion: "))
                if ans == 1:
                    entidad = self.__menu_entidades__()
                    #SALIR EN CASO DE NO RELACIONAR
                    if entidad == self.__Menu__.CONTINUAR:
                        pass
                    if entidad == self.__Menu__.CUADRO:
                        id_add = self.__ids__(entidad, bd)
                        for i in id_add:
                            self._ID_cuadros.add(i)
                    if entidad == self.__Menu__.CLIENTE:
                        id_add = self.__ids__(entidad, bd)
                        for i in id_add:
                            self._ID_clientes.add(i)
                elif ans == 0:
                    break
            except: 
                pass
    
    #METODO PARA IMPRIMIR EL MENU DE ENTIDADES SE RELACIONAN CON LA PINACOTECA
    def __menu_entidades__(self):
        seleccion = None
        print("\nQue desea relacionar: \n")
        while True:
            for elemento in self.__Menu__:
                print("{} - {}".format(elemento.value, elemento.name))
            try:
                seleccion = int(input("Seleccione una opcion: "))
                seleccion = self.__Menu__(seleccion)
                return self.__Menu__(seleccion)
            except:
                print("Seleccion incorrecta ... intentelo nuevamente\n")
                continue
    
    #METODO PARA OBTENER ID
    def __ids__(self, entidad, bd):
        print('\tIngrese los IDs de los {} que corresponden a la Pinacoteca\n\t (0 - Salir)\n'.format(entidad._name_.lower()))
        #SE CREA EL NOMBRE DE LA ENTIDAD PARA OBTENER LOS ID'S REGISTRADOS EN LA BD
        entidad_str = entidad.name.lower() + 's'
        #SE CREAN LISTAS TEMPORALES PARA AÑADIR Y REGISTRAR LOS ID'S
        ids = set(); id_add = set()
        #SE OBTIENE UN SET CON LOS ID'S EXISTENTES EN LA BD
        for obj in bd[entidad_str]:
            ids.add(obj.id)
            
        while True:
            try: 
                id_t = {int(input("Ingrese ID: \t"))}
                if id_t == {0}:
                    break
                elif not(id_t.issubset(ids)):
                    print("ID de {} no existente, ingrese un ID existente".format(entidad._name_.lower()))
                else:
                    id_add.add(*id_t)
                    bd[entidad_str][int(*id_t)-1]._ID_pinacoteca.add(self._id)
            except:
                print("ID de {} no existente, ingrese un ID existente".format(entidad._name_.lower()))
                continue
        return id_add
        
    
    #SUBCLASE DE ACCIONES ASOCIADAS A UN NUMERO
    class __Menu__(Enum):
        CUADRO        = 1
        CLIENTE       = 2
        CONTINUAR     = 2
        
    def __baja__(self, bd, id_t):
        
        self.__restartrel__(bd, id_t)
        self._borrado         = 1
        
    def __restartrel__(self, bd, id_t):
        
        for i in range(len(bd['clientes'])):
            try:
                bd['clientes'][i]._ID_pinacoteca.discard(self._id)
            except:
                pass
        
        for i in range(len(bd['cuadros'])):
            try:
                if id_t == bd['cuadros'][i]._ID_pinacoteca:
                    bd['cuadros'][i]._ID_pinacoteca = None
            except:
                pass
            
        for i in range(len(bd['ventas'])):
            try:
                if id_t == bd['ventas'][i]._ID_pinacoteca:
                    bd['ventas'][i]._ID_pinacoteca = None
            except:
                pass

        self._nombre       = None
        self._direccion    = None
        self._ciudad       = None
        self._largo        = None
        self._ancho        = None
        self._area         = None
        self._ID_cuadros   = None
        self._ID_clientes  = None
        self._ID_ventas    = None
    
    def __modificacion__(self, bd, id_t):
        self.__restartrel__(bd, id_t)
        
        while True:
            self.nombre    = input("\tIngrese Nombre:    ")
            self.direccion = input("\tIngrese Dirección: ")
            self.ciudad    = input("\tIngrese Ciudad:    ")
            self.largo     = input("\tIngrese Largo:     ")
            self.ancho     = input("\tIngrese Ancho:     ")
            
            if not(self._nombre == None or self._direccion == None or self._ciudad == None 
                   or self._largo == None or self._ancho == None):
                break
        
        self._area = float(self._ancho) * float(self._largo)
        #ID'S QUE SE RELACIONAN EN ESTA CLASE
        self._ID_cuadros   = set()
        self._ID_clientes  = set()
        #ID QUE SE RELACIONAN EN OTRA CLASE
        self._ID_ventas    = set()
            
        self.__relacion__(bd)
    
    
    def __str__(self) -> str:
        return (
            f" ID:               {self._id}\n"
            f" Nombre:           {self._nombre}\n"
            f" Dirección:        {self._direccion}\n"
            f" Ciudad:           {self._ciudad}\n"
            f" Metros cuadrados: {self._area}\n"
            f" La Pinacoteca se relaciona con:\n"
            f" Los Cuadros:      {self._ID_cuadros}\n"
            f" Los Clientes:     {self._ID_clientes}\n"
            f" Las Ventas:       {self._ID_ventas}\n"
        )