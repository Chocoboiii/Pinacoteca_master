#Librerias
from Set_Paises  import paises
from datetime    import datetime
from enum        import Enum

fecha = "%d/%m/%Y" 

class Mecena():
    
    def __init__(self, id, nombre, pais, ciudad_nacimiento, fecha_fallecimiento):
        self.id = id
        self.nombre = nombre
        self.pais = pais
        self.ciudad_nacimiento = ciudad_nacimiento
        self.fecha_fallecimiento = fecha_fallecimiento
        self._ID_pintor          = set()

    # Decorador de ID
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        if id <= 0:
            print("ID No valido")
        else:
            self._id = id

    # Decorador de nombre
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        if not (x.isalpha() or x.isspace() for x in nombre):
            print("El nombre no corresponde a valores alfabéticos")
        else:
            self._nombre = nombre

    # Decorador de pais
    @property
    def pais(self):
        return self._pais

    @pais.setter 
    def pais(self, pais):
        if pais == '':
            print("Por favor, ingrese un país")
        elif pais not in paises:
            print("El país ingresado no se reconoce en la base de datos")
        else:
            self._pais = pais

    # Decorador de ciudad de nacimiento
    @property
    def ciudad_nacimiento(self):
        return self._ciudad_nacimiento

    @ciudad_nacimiento.setter 
    def ciudad_nacimiento(self, ciudad_nacimiento):
        if not (x.isalpha() or x.isspace() for x in ciudad_nacimiento):
            print("La ciudad de nacimiento no corresponde a valores alfabéticos")
        else:
            self._ciudad_nacimiento = ciudad_nacimiento

    # Decorador de fecha de fallecimiento
    @property 
    def fecha_fallecimiento(self):
        return self._fecha_fallecimiento
    
    @fecha_fallecimiento.setter 
    def fecha_fallecimiento(self, fecha_fallecimiento):
        if fecha_fallecimiento == '':
            self._fecha_fallecimiento = ''
            return
        try:
            #Validar el formato
            fecha_obj = datetime.strptime(fecha_fallecimiento, fecha)
            #Vemos que no sea una fecha mayor que la actual
            año_actual = datetime.now().year
            if fecha_obj.year > año_actual:
                print("La fecha ingresada no es correcta")
                return None
            self._fecha_fallecimiento = fecha_fallecimiento
        except:
            print("El formato de la fecha de creación no es correcto")
            return None
    

    #Metodo para relacionar el mecenas con otras clases
    def __relacion__(self, bd):
        while True:
            try: 
                print("Desea relacionar la Mecena añadida con Pintores:\n\tSI\t1\n\tNO\t0\n")
                ans = int(input("Seleccione una opcion: "))
                if ans == 1:
                    entidad = self.__menu_entidades__()
                    #SALIR EN CASO DE NO RELACIONAR
                    if entidad == self.__Menu__.CONTINUAR:
                        pass
                    
                    if entidad == self.__Menu__.PINTOR:
                        id_add = self.__ids__('pintor', bd)
                        for i in id_add:
                            self._ID_pintor.add(i)
                        
                elif ans == 0:
                    break
            except: 
                pass
    
    #Metodo para imprimir el menu de clases que se relacionan con el mecenas
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
    
    #Metodo para obtener ID
    def __ids__(self, entidad, bd):
        
        entidad_str = 'pintores'
            
        #Listas para añadir IDs
        ids = set(); id_add = set()
        #Con los IDs ya existentes en la base de datos, hacemos un set
        for obj in bd[entidad_str]:
            ids.add(obj.id)
        
        print('\tIngrese el ID de '+ entidad +' que le corresponde a la Mecena\n\t (0 - Salir)\n')
        
        while True:
            
            id_t = int(*self.__load_rel__(ids, id_add, entidad, bd, entidad_str))
            
            if id_t == 0:
                break
            else:
                id_add.add(id_t)
                bd[entidad_str][id_t-1]._ID_mecenas = self._id
        
        return id_add
    
    def __load_rel__(self, ids, id_add, entidad, bd, entidad_str):            
        
        while True:
            try: 
                id_t = {int(input("Ingrese ID: \t"))}
                if id_t == {0}:
                    return id_t
                if not(id_t.issubset(ids)):
                    print("ID de "+ entidad + " no existente, ingrese un ID existente")
                else:
                    return id_t
            except:
                print("ID de "+ entidad +" no existente, ingrese un ID existente")
                continue
    
    def __baja__(self, bd, id_t):
        
        self.__restartrel__(bd, id_t)
        self._borrado             = 1

    def __restartrel__(self, bd, id_t):
        for i in range(len(bd['pintores'])):
            try:
                bd['pintores'][i]._ID_mecenas.discard(self._id)
            except:
                pass
                
        self._nombre              = None
        self._pais                = None
        self._ciudad_nacimiento   = None
        self._fecha_fallecimiento = None
        self._ID_pintor           = None
    
    def __modificacion__(self, bd, id_t):
        self.__restartrel__(bd, id_t)
        
        while True:
            self.nombre              = input("\tIngrese Nombre:                 ")
            self.pais                = input("\tIngrese País:                   ")
            self.ciudad_nacimiento   = input("\tIngrese Ciudad de Nacimiento:   ")
            self.fecha_fallecimiento = input("\tIngrese Fecha de Fallecimiento: ")
            
            if not(self._nombre == None or self._pais == None or self._ciudad_nacimiento == None
                   or self._fecha_fallecimiento == None):
                break
        
        self._ID_pintor = set()
            
        self.__relacion__(bd)
    

    class __Menu__(Enum):
        PINTOR        = 1
        CONTINUAR     = 2
        
    def __str__(self):
        return (
                f" ID:                     {self._id}\n"
                f" Nombre:                 {self._nombre}\n"
                f" País:                   {self._pais}\n"
                f" Ciudad de nacimiento:   {self._ciudad_nacimiento}\n"
                f" Fecha de fallecimiento: {self._fecha_fallecimiento}\n"
                f" Mecena                  {self._nombre} patrocina al:\n"
                f" ID Pintor:              {self._ID_pintor}\n"
            )
    