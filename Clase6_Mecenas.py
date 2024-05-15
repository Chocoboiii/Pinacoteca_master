#IMPORTAR LIBRERIAS 
from ClaseMadre_Persona import Persona as p
from Set_Paises import paises
from datetime    import datetime
from enum        import Enum

formato_fecha = "%d/%m/%Y" 

class Mecena(p):
    
    def __init__(self, id = 0, nombre = '', pais = '', ciudad_nacimiento = '', fecha_fallecimiento = '',_ID_pintor = set()):
        super().__init__(id, nombre, pais, ciudad_nacimiento, fecha_fallecimiento)
        self._ID_pintor          = set()
    

    #METODO PARA RELACIONAR LA PINCOTECA CON OTRAS IDENTIDATES
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
        
        entidad_str = 'pintores'
            
        #SE CREAN LISTAS TEMPORALES PARA AÑADIR Y REGISTRAR LOS ID'S
        ids = set(); id_add = set()
        #SE OBTIENE UN SET CON LOS ID'S EXISTENTES EN LA BD
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
        self._ciudad_nacimiento  = None
        self._fecha_fallecimiento = None
        self._ID_pintor           = None
    
    def __modificacion__(self, bd, id_t):
        self.__restartrel__(bd, id_t)
        
        while True:
            self.nombre              = input("\tIngrese Nombre:                 ")
            self.pais                = input("\tIngrese País:                   ")
            self.ciudad_nacimiento  = input("\tIngrese Ciudad de Nacimiento:   ")
            self.fecha_fallecimiento = input("\tIngrese Fecha de Fallecimiento: ")
            
            if not(self._nombre == None or self._pais == None or self._ciudad_nacimiento == None
                   or self._fecha_fallecimiento == None):
                break
        
        self._ID_pintor = set()
            
        self.__relacion__(bd)
    
    #SUBCLASE DE ACCIONES ASOCIADAS A UN NUMERO
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
                f" LA MECENA {self._nombre} patrocina al:\n"
                f" ID Pintor:              {self._ID_pintor}\n"
            )
    
'''
try:
    prueba = Mecena(1, "Prisciliano", "México", "Tepic", "05/09/2023")
    print(prueba)
except:
    pass
'''