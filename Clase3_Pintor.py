#IMPORTAR LIBRERIAS
from ClaseMadre_Persona import Persona as p
from datetime    import datetime
from Set_Paises import paises
from enum        import Enum

formato_fecha = "%d/%m/%Y"

class Pintor(p):
     
    def __init__(self, id, nombre, pais, ciudad_nacimiento, fecha_fallecimiento, fecha_nacimiento = None, _ID_maestro = None, _ID_alumnos = set(), _ID_mecenas = set(), _ID_F_Escuela = [None,''], _ID_cuadros = set()):
        super().__init__(id, nombre, pais, ciudad_nacimiento, fecha_fallecimiento )
        #ID'S QUE SE RELACIONAN AQUÍ
        self._fecha_nacimiento = None
        self._ID_maestro       = None
        self._ID_alumnos       = set()
        self._ID_mecenas       = set()
        self._ID_F_Escuela     = [None,'']
        #ID QUE SE RELACIONAN EN OTRA CLASE
        self._ID_cuadros       = set()
        
    #METODO PARA RELACIONAR LA PINCOTECA CON OTRAS IDENTIDATES
    def __relacion__(self, bd):
        while True:
            try: 
                print("Desea relacionar al pintor añadido con un Maestro, Alumnos, Mecenas o Escuelas:\n\tSI\t1\n\tNO\t0\n")
                ans = int(input("Seleccione una opcion: "))
                if ans == 1:
                    entidad = self.__menu_entidades__()
                    #SALIR EN CASO DE NO RELACIONAR
                    if entidad == self.__Menu__.CONTINUAR:
                        pass
                    
                    if entidad == self.__Menu__.MAESTRO:
                        entidad = 'pintor'
                        id_add =  self.__ids__(entidad, bd, 'U')
                        if not(id_add == 0):
                            self._ID_maestro = id_add
                            
                    if entidad == self.__Menu__.ALUMNOS:
                        entidad = 'pintor'
                        add_id  = self.__ids__(entidad, bd, 'M')
                        for i in add_id:
                            self._ID_alumnos.add(i)
                            
                    if entidad == self.__Menu__.MECENAS:
                        add_id = self.__ids__(entidad, bd, 'M')
                        for i in add_id:
                            self._ID_mecenas.add(i)
                        
                    if entidad == self.__Menu__.ESCUELA:
                        id_add = self.__ids__(entidad, bd, 'U')
                        #INGRESAR FECHA A LA QUE FUE A LA ESCUELA
                        if not(id_add == 0):
                            while True:
                                try:
                                    self._ID_F_Escuela[0] = id_add
                                    ing_esc = input("INGRESE FECHA EN LA QUE ESTUVO EN LA ESCUELA: \t")
                                    #VALIDAR QUE TENGA EL FORMATO CORRECTO
                                    fecha_obj = datetime.strptime(ing_esc, formato_fecha)
                                    #VALIDAR QUE EL AÑO NO SEA MAYOR AL ACTUAL Y QUE NO SEA ANTES DE SU FECHA DE NACIMIENTO Y DE FALLECIMIENTO
                                    año_actual = datetime.now().year
                                    nacimiento = (datetime.strptime(self.fecha_nacimiento, formato_fecha)).year
                                    if not(self.fecha_fallecimiento == ''):
                                        fallecimiento = (datetime.strptime(self.fecha_fallecimiento, formato_fecha)).year
                                        if fecha_obj.year >= fallecimiento or fecha_obj.year <= nacimiento:
                                            print("Inconsistencia en la fecha")
                                        self._ID_F_Escuela[1] =  ing_esc
                                        break
                                    elif fecha_obj.year > año_actual or fecha_obj.year <= nacimiento:
                                        print("Inconsistencia en la fecha")
                                    else:
                                        self._ID_F_Escuela[1] =  ing_esc
                                        break
                                except:
                                    print("El formato de la fecha de fallecimiento no es correcto")
                                    continue
                    if entidad == self.__Menu__.CUADROS:
                        add_id = self.__ids__(entidad, bd, 'M')
                        for i in add_id:
                            self._ID_cuadros.add(i)
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
    def __ids__(self, entidad, bd, type_r):
        
        #SE CREA EL NOMBRE DE LA ENTIDAD PARA OBTENER LOS ID'S REGISTRADOS EN LA BD
        #VALIDAR QUE LA ENTIDAD PINTOR TENGA SU CORRECTO PLURAL
        if entidad == 'pintor':
            entidad_str = entidad + 'es'
        else:
            entidad_str = entidad.name.lower() + 's'
        #SE CREAN LISTAS TEMPORALES PARA AÑADIR Y REGISTRAR LOS ID'S
        ids = set(); id_add = set()
        #SE OBTIENE UN SET CON LOS ID'S EXISTENTES EN LA BD
        for obj in bd[entidad_str]:
            ids.add(obj.id)
        
        #VALIDAR EL TIPO DE RELACIÓN, SI ES QUE LA ENTIDAD LE CORRESPONDE UN ESTUDIANTE
        if type_r == 'U':
            try:
                print('\tIngrese el ID de {} que le corresponde al Pintor\n\t (0 - Salir)\n'.format(entidad.name.lower()))
            except:
                print('\tIngrese el ID del Maestro que le corresponde al Pintor\n\t (0 - Salir)\n')
            id_t = self.__load_rel__(ids, id_add, entidad, bd)
            id_add = int(*id_t)
            if id_add == 0:
                return id_add
            if entidad_str == 'pintores':
                bd[entidad_str][int(*id_t)-1]._ID_alumnos.add(self._id)
            else:
                 bd[entidad_str][int(*id_t)-1]._ID_pintor.add(self._id)             
          
        #VALIDAR SI ES QUE A LA ENTIDAD LE CORRESPONDEN MUCHOS ESTUDIANTES
        elif type_r == 'M':
            try:
                print('\tIngrese los IDs de los {} que corresponden al Pintor\n\t (0 - Salir)\n'.format(entidad.name.lower()))
            except:
                print('\tIngrese el ID de los Alumnos que le corresponden al Pintor\n\t (0 - Salir)\n')
            while True:
                id_t = self.__load_rel__(ids, id_add, entidad, bd)
                if id_t == {0}:
                    break
                id_add.add(*id_t)
                if entidad_str == 'pintores':
                    bd[entidad_str][int(*id_t)-1]._ID_maestro = self._id
                else:
                    bd[entidad_str][int(*id_t)-1]._ID_pintor.add(self._id)   
                
        return id_add
    
    def __load_rel__(self, ids, id_add, entidad, bd ):            
        try:
            if entidad == 'pintor':
                entidad_str = 'pintor'            
        except:
            entidad_str = entidad.name.lower()
        while True:
            try: 
                id_t = {int(input("Ingrese ID: \t"))}
                if id_t == {0}:
                    return id_t
                if not(id_t.issubset(ids)):
                    print("ID de "+ entidad_str + " no existente, ingrese un ID existente")
                else:
                    return id_t
            except:
                print("ID de "+entidad_str +" no existente, ingrese un ID existente")
                continue
    
    def __baja__(self, bd, id_t):
        
        self.__restartrel__(bd, id_t)
        self._borrado         = 1
        
    def __restartrel__(self, bd, id_t):
        for i in range(len(bd['pintores'])):
            try:
                if bd['pintores'][i]._ID_maestro == id_t:
                    bd['pintores'][i]._ID_maestro = None
            except:
                pass
            
            try:
                bd['pintores'][i]._ID_alumnos.discard(self._id)
            except:
                pass
        
        for i in range(len(bd['escuelas'])):
            try:
                bd['escuelas'][i]._ID_pintor.discard(self._id)
            except:
                pass
            
        for i in range(len(bd['mecenas'])):
            try:
                bd['mecenas'][i]._ID_pintor.discard(self._id)
            except:
                pass
        
        for i in range(len(bd['cuadros'])):
            try:
                if bd['cuadros'][i]._ID_pintor == id_t:
                    bd['cuadros'][i]._ID_pintor == None
            except:
                pass

        self._nombre               = None
        self._fecha_nacimiento     = None
        self._fecha_fallecimiento  = None
        self._ciudad_nacimiento   = None
        self._pais                 = None
        self._ID_maestro           = None
        self._ID_alumnos           = None
        self._ID_mecenas           = None
        self._ID_F_Escuela         = None
        self._ID_cuadros           = None
    
    def __modificacion__(self, bd, id_t):
        self.__restartrel__(bd, id_t)
        
        while True:
            self.nombre           = input("\tIngrese Nombre:              ")
            self.fecha_nacimiento = input("\tIngrese Fecha de Nacimiento: ")
            self.fecha_fallecimiento  = input("\tIngrese Fecha de Fallecimiento:  ")
            self.ciudad_nacimiento           = input("\tIngrese Ciudad de Nacimiento:              ")
            self.pais             = input("\tIngrese País: ")
            
            if not(self._nombre == None or self._fecha_nacimiento == None or self._fecha_fallecimiento == None 
                   or self._ciudad_nacimiento == None or self._pais == None):
                break
        
        #ID'S QUE SE RELACIONAN AQUÍ
        self._ID_maestro      = None
        self._ID_alumnos      = set()
        self._ID_mecenas      = set()
        self._ID_F_Escuela    = [None,'']
        #ID QUE SE RELACIONAN EN OTRA CLASE
        self._ID_cuadros      = set()
            
        self.__relacion__(bd)
    
    #SUBCLASE DE ACCIONES ASOCIADAS A UN NUMERO
    class __Menu__(Enum):
        MAESTRO       = 1
        ALUMNOS       = 2
        MECENAS       = 3
        ESCUELA       = 4
        CUADROS       = 5
        CONTINUAR     = 6
    
    def __str__(self) -> str:
        return (
            f" ID:                  {self._id}\n"
            f" Nombre:              {self._nombre}\n"
            f" Fecha de Nacimiento: {self._fecha_nacimiento}\n"
            f" Fecha de fallecimiento:  {self._fecha_fallecimiento}\n"
            f" Ciudad de nacimiento:              {self._ciudad_nacimiento}\n"
            f" Pais:                {self._pais}\n"
            f" EL PINTOR: {self.nombre} se relaciona con:\n"
            f" El Maestro:          {self._ID_maestro}\n"
            f" Los Alumnos:         {self._ID_alumnos}\n"
            f" La Fecha de escuela: {self._ID_F_Escuela}\n"
            f" Las Mecenas:         {self._ID_mecenas}\n"
            f" Los cuadros:         {self._ID_cuadros}\n"
        )

'''
try:        
    prueba = Pintor(1, "Jose", "05/09/2001", "23/02/2002", "Tepic", "México")
    print(prueba)
except:
    pass
'''