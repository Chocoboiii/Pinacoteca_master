
from Set_Paises  import paises
from enum        import Enum
from datetime    import datetime

fecha = "%d/%m/%Y" 

class Escuela:
    
    def __init__(self, id = 0, nombre = '', pais = ''):
        self.id         = id
        self.nombre     = nombre
        self.pais       = pais
        self._ID_pintor = set()
    

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        if id <= 0:
            print("ID No valido")
            return None
        self._id = id
    

    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, nombre): 
        if nombre == '':
            self._nombre = ''
            return
        if not (x.isalpha() or x.isspace() for x in nombre):
            print("El nombre no corresponde a valores alfabeticos")
            return None
        self._nombre = nombre 
    
 
    @property
    def pais(self):
        return self._pais
    
    @pais.setter 
    def pais(self, pais):
        if pais == '':
            self._pais = ''
            return
        paist = set([pais])
        if paist.issubset(paises):
            self._pais = pais
        else:
            print("El país ingresado no se reconoce en la base de datos")
            return None
        
  
    def __relacion__(self, bd):
        while True:
            try: 
                print("Desea relacionar la Escuela añadida con Alumnos:\n\tSI\t1\n\tNO\t0\n")
                ans = int(input("Seleccione una opcion: "))
                if ans == 1:
                    entidad = self.__menu_entidades__()
                    
                    if entidad == self.__Menu__.CONTINUAR:
                        pass
                    
                    if entidad == self.__Menu__.ALUMNOS:
                        id_add = self.__ids__('pintor', bd)
                        for i in id_add:
                            self._ID_pintor.add(i)
                        
                elif ans == 0:
                    break
            except: 
                pass
    
    
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
    
    
    def __ids__(self, entidad, bd):
        
        entidad_str = 'pintores'
            
        
        ids = set(); id_add = set()
        
        for obj in bd[entidad_str]:
            ids.add(obj.id)
        
        print('\tIngrese el ID de '+ entidad +' que le corresponde al Cuadro\n\t (0 - Salir)\n')
        
        while True:
            
            id_t = int(*self.__load_rel__(ids, id_add, entidad, bd, entidad_str))
            
            if id_t == 0:
                break
            else:
                id_add.add(id_t)
                bd[entidad_str][id_t-1]._ID_F_Escuela[0] = self._id
                ing_esc = input("INGRESE FECHA EN LA QUE ESTUVO EN LA ESCUELA: \t")
                
                fecha_obj = datetime.strptime(ing_esc, fecha)
                
                año_actual = datetime.now().year
                
                nacimiento = (datetime.strptime(bd[entidad_str][id_t-1]._fecha_nacimiento, fecha)).year
                if not(bd[entidad_str][id_t-1]._fecha_defuncion == ''):
                    defuncion = (datetime.strptime(bd[entidad_str][id_t-1]._fecha_defuncion, fecha)).year
                    if fecha_obj.year >= defuncion or fecha_obj.year <= nacimiento:
                        print("Inconsistencia en la fecha")
                    self._ID_F_Escuela[1] =  ing_esc
                    break
                elif fecha_obj.year > año_actual or fecha_obj.year <= nacimiento:
                    print("Inconsistencia en la fecha")
                else:
                    bd[entidad_str][id_t-1]._ID_F_Escuela[1] =  ing_esc
        
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
        self._borrado   = 1
    
    def __restartrel__(self, bd, id_t):
        for i in range(len(bd['pintores'])):
            try:
                if bd['pintores'][i]._ID_F_Escuela[0] == id_t:
                    bd['pintores'][i]._ID_F_Escuela = None
            except:
                pass
                
        self._nombre    = None
        self._pais      = None
        self._ID_pintor = None
    
    def __modificacion__(self, bd, id_t):
        self.__restartrel__(bd, id_t)
        
        while True:
            self.nombre     = input("\tIngrese Nombre: ")
            self.pais       = input("\tIngrese País:   ")
            
            if not(self._nombre == None or self._pais == None):
                break
        
        self._ID_pintor = set()
            
        self.__relacion__(bd)
    

    class __Menu__(Enum):
        ALUMNOS       = 1
        CONTINUAR     = 2
    
    def __str__(self):
        return (
                f" ID:          {self._id}\n"
                f" Nombre:      {self._nombre}\n"
                f" País:        {self._pais}\n"
                f" Estudiantes: {self._ID_pintor}"
                f" Escuela:     {self._nombre} se relaciona con:\n"
                f" ID Pintor:   {self._ID_pintor}\n"
            )