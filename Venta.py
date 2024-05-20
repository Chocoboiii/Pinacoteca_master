#IMPORTAR LIBRERIAS
from datetime    import datetime

formato_fecha = "%d/%m/%Y"

class Venta():
     
    def __init__(self, id = 0, precio = '', fecha = ''):
        self.id           = id 
        self.precio       = precio
        self.fecha        = fecha
        self._ID_cuadros  = 0
        self._ID_clientes = 0
        
    
    #Decorador de ID
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        if id <= 0:
            print("ID No valido")
            return None
        self._id = id
    
    #Decorador de precio
    @property
    def precio(self):
        return self._precio
    
    @precio.setter
    def precio(self, precio):
        try:
            float(precio)
            self._precio = precio
        except:
            print("El precio ingresado es incorrecto")            
            return None
    
    #Decorador de fecha
    @property
    def fecha(self):
        return self._fecha
    
    @fecha.setter
    def fecha(self, fecha): #TODO Validar que la fecha tenga el formato dd//mm/aaaa 
        try:
            #VALIDAR QUE TENGA EL FORMATO CORRECTO
            fecha_obj = datetime.strptime(fecha, formato_fecha)
            #VALIDAR QUE NO SEA UNA FECHA FUTURA A LA 
            año_actual = datetime.now().year
            if fecha_obj.year > año_actual:
                print("La fecha ingresada no es correcta")
                return None
            self._fecha = fecha
        except:
            print("El formato de la fecha de venta no es correcto")
            return None
    
       
    #Metodo para relacionar venta
    def __relacion__(self, bd):
        while True:
            try: 
                self._ID_cuadros  = self.__ids__('cuadro', bd)
                self._ID_clientes = self.__ids__('cliente', bd)
                break
            except: 
                pass
    #Metodo para obtener IDs de los objetos ya creados
    def __ids__(self, entidad, bd):
        entidad_str = entidad + 's'
            
        #Listas para añadir IDs
        ids = set(); id_add = set()
        #Con los IDs ya existentes en la base de datos, hacemos un set
        for obj in bd[entidad_str]:
            ids.add(obj.id)
        
        while True:
            print('\tIngrese el ID de '+ entidad +' que le corresponde a la Venta\n\t (0 - Salir)\n')
               
            id_add = int(*self.__load_rel__(ids, id_add, entidad, bd, entidad_str))
            #Si nos arroja un 0, salimos
            if id_add == 0:
                break
            else:
                #Caso de relacionar cuadro
                if entidad == 'cuadro':
                    #Si el cuadro no tiene un ID de venta en sus valores, se lo añadimos
                    if bd[entidad_str][id_add-1]._ID_venta == None:
                        bd[entidad_str][id_add-1]._ID_venta = self._id
                        break
                    else:
                        #Si ya tiene un ID de venta, decimos que no se puede
                        print('Otra venta ya ha sigo asignada al '+ entidad)
                else: #En cualquier otro caso, añadir el ID de venta a los otros objetos
                    bd[entidad_str][id_add-1]._ID_venta.add(self._id)  
                    break
        return id_add
    #Definimos nuestro metodo de relacion
    def __load_rel__(self, ids, id_add, entidad, bd, entidad_str):             
        while True:
            try: 
                #Esperamos el input de un ID existente
                id_t = {int(input("\tIngrese ID: \t"))}
                if id_t == {0}:
                    #Si nos arroja 0, salimos
                    return id_t
                if not(id_t.issubset(ids)):
                    #Si el ID ingresado no esta en nuestro set de IDs disponibles, imprimimos error
                    print("ID de "+ entidad + " no existente")
                else:
                    return id_t
            except:
                #Si es cualquier cosa menos un entero perteneciente al set, error
                print("ID de "+ entidad +" no existente")
                continue
    #Definimos baja
    def __baja__(self, bd, id_t):
        #Llamamos nuestro restart y levantamos una bandera que indica que algo se borro
        self.__restartrel__(bd, id_t)
        self._borrado      = 1
    #Definimos nuestro restart    
    def __restartrel__(self, bd, id_t):
        #Con este metodo vamos a quitar el ID de venta de los clientes
        for i in range(len(bd['clientes'])):
            try:
                bd['clientes'][i]._ID_venta.discard(self._id)
            except:
                pass
        #Y con este vamos a quitar el ID de venta de los cuadros
        for i in range(len(bd['cuadros'])):
            try:
                if bd['cuadros'][i]._ID_venta == id_t:
                    bd['cuadros'][i]._ID_venta = None
            except:
                pass
        #Despues, vaciamos el objeto
        self._precio       = None
        self._fecha        = None
        self._ID_cuadros   = None
        self._ID_clientes  = None
    #Definimos modificaciones
    def __modificacion__(self, bd, id_t):
        self.__restartrel__(bd, id_t)
        
        while True:
            #Cambiamos el precio y la fecha con el input del usuario
            self.precio       = input("\tIngrese Precio:  ")
            self.fecha        = input("\tIngrese Fecha:   ")
            #Si no se dejan vacios, salimos
            if not(self._precio == None or self.fecha == None):
                break
        #Reiniciamos las relaciones y llamamos el metodo de relacion
        self._ID_cuadros  = 0
        self._ID_clientes = 0
        self.__relacion__(bd)
    #Con este metodo imprimimos los valores del objeto
    def __str__(self):
        return (
                f" ID:             {self._id}\n"
                f" Precio:         ${self._precio}.00\n"
                f" Fecha de venta: {self.fecha}\n"
                f" Venta           {self._id} se relaciona con:\n"
                f" ID Cuadro:      {self._ID_cuadros}\n"
                f" ID Cliente:     {self._ID_clientes}\n"
            )