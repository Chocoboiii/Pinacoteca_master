#IMPORTAR LIBRERIAS
from datetime    import datetime
from Set_Paises  import paises
from enum        import Enum

fecha = "%d/%m/%Y"

class Pintor():
     
    def __init__(self, id, nombre, pais, ciudad_nacimiento, fecha_nacimiento, 
                 fecha_fallecimiento): 
        self.id = id
        self.nombre = nombre
        self.pais = pais
        self.ciudad_nacimiento = ciudad_nacimiento
        self.fecha_nacimiento = fecha_nacimiento
        self.fecha_fallecimiento = fecha_fallecimiento        
        self._ID_maestro       = None
        self._ID_alumnos       = set()
        self._ID_mecenas       = set()
        self._ID_F_Escuela     = [None,'']
        self._ID_cuadros       = set()


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

    # Decorador de fecha de nacimiento
    @property 
    def fecha_nacimiento(self):
        return self._fecha_nacimiento
    
    @fecha_nacimiento.setter 
    def fecha_nacimiento(self, fecha_nacimiento):
        if fecha_nacimiento == '':  # Valida si está vacia la fecha
            self._fecha_nacimiento=''
            return
        else:
            try:
                #Validar el formato
                fecha_obj = datetime.strptime(fecha_nacimiento, fecha)
                if fecha_obj:
                    self._fecha_nacimiento = fecha_nacimiento
            except:
                print("El formato de la fecha de creación no es correcto")
                return None
        
    # Decorador de fecha de fallecimiento
    @property 
    def fecha_fallecimiento(self):
        return self._fecha_fallecimiento
    
    @fecha_fallecimiento.setter 
    def fecha_fallecimiento(self, fecha_fallecimiento):
        if fecha_fallecimiento == '':  # Valida si está vacia la fecha
            self._fecha_fallecimiento=''
            return
        else:
            try:
                #Validar el formato
                fecha_obj = datetime.strptime(fecha_fallecimiento, fecha)
                #Valildación contra fecha actual 
                año_actual = datetime.now().year
                if self.fecha_nacimiento and self.fecha_fallecimiento:
                    if self.fecha_nacimiento > self.fecha_fallecimiento:
                        print("la fecha ingresada no es correcta, debe ser después de la fecha de nacimiento")
                    return None
                else:
                    self._fecha_fallecimiento = fecha_fallecimiento
            except:
                print("El formato de la fecha de creación no es correcto")
                return None
        
    #Metodo para relacionar el pintor con otras clases
    def __relacion__(self, bd):
        while True:
            try: 
                print("Desea relacionar al pintor añadido con un Maestro, Alumnos, Mecenas o Escuelas:\n\tSI\t1\n\tNO\t0\n")
                #Esperamos un input, si nos da 1, seguimos
                ans = int(input("Seleccione una opcion: "))
                if ans == 1:
                    entidad = self.__menu_entidades__()
                    #Si nos da continuar, salimos
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
                    #Caso Escuela
                    if entidad == self.__Menu__.ESCUELA:
                        id_add = self.__ids__(entidad, bd, 'U')
                        #Si estuvo en una escuela, pedimos la fecha en la que estuvo
                        if not(id_add == 0):
                            while True:
                                try:
                                    self._ID_F_Escuela[0] = id_add
                                    ing_esc = input("INGRESE FECHA EN LA QUE ESTUVO EN LA ESCUELA: \t")
                                    #Validar el formato
                                    fecha_obj = datetime.strptime(ing_esc, fecha)
                                    #Valildación de la fecha contra la actual, la de nacimiento y fallecimiento 
                                    año_actual = datetime.now().year
                                    nacimiento = (datetime.strptime(self.fecha_nacimiento, fecha)).year
                                    if not(self.fecha_fallecimiento == ''):
                                        #Si la fecha de fallecimiento no está vacía, continuamos
                                        fallecimiento = (datetime.strptime(self.fecha_fallecimiento, fecha)).year
                                        #Si la fecha de escuela es mayor que la de fallecimiento o menor que la de nacimiento, decimos error
                                        if fecha_obj.year >= fallecimiento or fecha_obj.year <= nacimiento:
                                            print("Inconsistencia en la fecha")
                                        self._ID_F_Escuela[1] =  ing_esc
                                        break
                                    elif fecha_obj.year > año_actual or fecha_obj.year <= nacimiento:
                                        #Si la fecha es mayor que el año actual, decimos error
                                        print("Inconsistencia en la fecha")
                                    else:
                                        self._ID_F_Escuela[1] =  ing_esc
                                        break
                                except:
                                    #Si el formato es incorrecto, no lo guardamos, pero no rompemos
                                    print("El formato de la fecha de fallecimiento no es correcto")
                                    continue
                    #Caso Cuadros
                    if entidad == self.__Menu__.CUADROS:
                        add_id = self.__ids__(entidad, bd, 'M')
                        for i in add_id:
                            #Añadimos el ID de los cuadros
                            self._ID_cuadros.add(i)
                elif ans == 0:
                    break
            except: 
                pass
    
    #Metodo para imprimir el menu de clases que se relacionan con el pintor
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
    def __ids__(self, entidad, bd, type_r):
        
        #Se hace plural el nombre para que pueda acceder a las listas de la base de datos
        if entidad == 'pintor':
            entidad_str = entidad + 'es'
        else:
            entidad_str = entidad.name.lower() + 's'
        #Listas para añadir IDs
        ids = set(); id_add = set()
        #Se obtienen los IDs ya registrados en la base de datos
        for obj in bd[entidad_str]:
            ids.add(obj.id)
        
        #Si lo definimos como alumno
        if type_r == 'U':
            try:
                print('\tIngrese el ID de {} que le corresponde al Pintor\n\t (0 - Salir)\n'.format(entidad.name.lower()))
            except:
                print('\tIngrese el ID del Maestro que le corresponde al Pintor\n\t (0 - Salir)\n')
            id_t = self.__load_rel__(ids, id_add, entidad, bd)
            id_add = int(*id_t)
            if id_add == 0:
                #Si el ID es 0, lo regresamos como está
                return id_add
            if entidad_str == 'pintores':
                #Si el nombre de la entidad es 'pintores, añadimos ese ID en ID alumnos
                bd[entidad_str][int(*id_t)-1]._ID_alumnos.add(self._id)
            else:
                #De lo contrario, añadimos el ID del pintor al objeto relacionado
                bd[entidad_str][int(*id_t)-1]._ID_pintor.add(self._id)             
          
        #Si lo definen como maestro
        elif type_r == 'M':
            try:
                print('\tIngrese los IDs de los {} que corresponden al Pintor\n\t (0 - Salir)\n'.format(entidad.name.lower()))
            except:
                print('\tIngrese el ID de los Alumnos que le corresponden al Pintor\n\t (0 - Salir)\n')
            while True:
                id_t = self.__load_rel__(ids, id_add, entidad, bd)
                if id_t == {0}:
                    #Si el ID es 0, salimos
                    break
                id_add.add(*id_t)
                if entidad_str == 'pintores':
                    #Si el nombre de la entidad es 'pintores, añadimos ese ID en ID maestro
                    bd[entidad_str][int(*id_t)-1]._ID_maestro = self._id
                else:
                    #De lo contrario, añadimos el ID del pintor al objeto relacionado
                    bd[entidad_str][int(*id_t)-1]._ID_pintor.add(self._id)   
                
        return id_add
    #Definimos nuestro metodo de relacion
    def __load_rel__(self, ids, id_add, entidad, bd ):            
        try:
            if entidad == 'pintor':
                entidad_str = 'pintor'            
        except:
            entidad_str = entidad.name.lower()
        while True:
            try: 
                #Esperamos el input de un ID existente
                id_t = {int(input("Ingrese ID: \t"))}
                if id_t == {0}:
                    #Si nos arroja 0, salimos
                    return id_t
                if not(id_t.issubset(ids)):
                    #Si el ID ingresado no esta en nuestro set de IDs disponibles, imprimimos error
                    print("ID de "+ entidad_str + " no existente, ingrese un ID existente")
                else:
                    return id_t
            except:
                #Si es cualquier cosa menos un entero perteneciente al set, error
                print("ID de "+entidad_str +" no existente, ingrese un ID existente")
                continue
    #Definimos baja
    def __baja__(self, bd, id_t):
        #Llamamos nuestro restart y levantamos una bandera que indica que algo se borro
        self.__restartrel__(bd, id_t)
        self._borrado      = 1
    #Definimos nuestro restart   
    def __restartrel__(self, bd, id_t):
        #Con este metodo vamos a quitar el ID de pintor de los pintores
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
        #Con este metodo vamos a quitar el ID de pintor de las escuelas
        for i in range(len(bd['escuelas'])):
            try:
                bd['escuelas'][i]._ID_pintor.discard(self._id)
            except:
                pass
        #Con este metodo vamos a quitar el ID de pintor de los mecenas    
        for i in range(len(bd['mecenas'])):
            try:
                bd['mecenas'][i]._ID_pintor.discard(self._id)
            except:
                pass
        #Con este metodo vamos a quitar el ID de pintor de otros pintores
        for i in range(len(bd['cuadros'])):
            try:
                if bd['cuadros'][i]._ID_pintor == id_t:
                    bd['cuadros'][i]._ID_pintor == None
            except:
                pass
        #Despues, vaciamos el objeto
        self._nombre               = None
        self._fecha_nacimiento     = None
        self._fecha_fallecimiento  = None
        self._ciudad_nacimiento    = None
        self._pais                 = None
        self._ID_maestro           = None
        self._ID_alumnos           = None
        self._ID_mecenas           = None
        self._ID_F_Escuela         = None
        self._ID_cuadros           = None
    #Definimos modificaciones
    def __modificacion__(self, bd, id_t):
        self.__restartrel__(bd, id_t)
        
        while True:
            #Cambiamos los valores con el input del usuario
            self.nombre                      = input("\tIngrese Nombre:              ")
            self.fecha_nacimiento            = input("\tIngrese Fecha de Nacimiento: ")
            self.fecha_fallecimiento         = input("\tIngrese Fecha de Fallecimiento:  ")
            self.ciudad_nacimiento           = input("\tIngrese Ciudad de Nacimiento:              ")
            self.pais                        = input("\tIngrese País: ")
            
            if not(self._nombre == None or self._fecha_nacimiento == None or self._fecha_fallecimiento == None 
                   or self._ciudad_nacimiento == None or self._pais == None):
                break
        
        ##Reiniciamos las relaciones y llamamos el metodo de relacion
        self._ID_maestro      = None
        self._ID_alumnos      = set()
        self._ID_mecenas      = set()
        self._ID_F_Escuela    = [None,'']
        self._ID_cuadros      = set()
            
        self.__relacion__(bd)
    
    #Subclase de menu de entidades relacionadas
    class __Menu__(Enum):
        MAESTRO       = 1
        ALUMNOS       = 2
        MECENAS       = 3
        ESCUELA       = 4
        CUADROS       = 5
        CONTINUAR     = 6
    #Con este metodo imprimimos los valores del objeto
    def __str__(self) -> str:
        return (
            f" ID:                                {self._id}\n"
            f" Nombre:                            {self._nombre}\n"
            f" Pais:                              {self._pais}\n"     
            f" Ciudad de nacimiento:              {self._ciudad_nacimiento}\n"       
            f" Fecha de nacimiento:               {self._fecha_nacimiento}\n"
            f" Fecha de fallecimiento:            {self._fecha_fallecimiento}\n"
            f" Pintor:                            {self._nombre} se relaciona con:\n"
            f" Maestro:                           {self._ID_maestro}\n"
            f" Alumnos:                           {self._ID_alumnos}\n"
            f" Fecha de escuela:                  {self._ID_F_Escuela}\n"
            f" Mecenas:                           {self._ID_mecenas}\n"
            f" Cuadros:                           {self._ID_cuadros}\n"
        )

