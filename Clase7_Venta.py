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
    
    #DECORADRO DE PRECIO
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
    
    #FECHA DE VENTA
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
    
       
    #METODO PARA RELACIONAR LA PINCOTECA CON OTRAS IDENTIDATES
    def __relacion__(self, bd):
        while True:
            try: 
                self._ID_cuadros  = self.__ids__('cuadro', bd)
                self._ID_clientes = self.__ids__('cliente', bd)
                break
            except: 
                pass
    

    
    #METODO PARA OBTENER ID
    def __ids__(self, entidad, bd):
        entidad_str = entidad + 's'
            
        #SE CREAN LISTAS TEMPORALES PARA AÑADIR Y REGISTRAR LOS ID'S
        ids = set(); id_add = set()
        #SE OBTIENE UN SET CON LOS ID'S EXISTENTES EN LA BD
        for obj in bd[entidad_str]:
            ids.add(obj.id)
        
        while True:
            print('\tIngrese el ID de '+ entidad +' que le corresponde a la Venta\n\t (0 - Salir)\n')
               
            id_add = int(*self.__load_rel__(ids, id_add, entidad, bd, entidad_str))
            
            if id_add == 0:
                break
            else:
                if entidad == 'cuadro':
                    if bd[entidad_str][id_add-1]._ID_venta == None:
                        bd[entidad_str][id_add-1]._ID_venta = self._id
                        break
                    else:
                        print('Otra venta ya ha sigo asignada al '+ entidad)
                else:
                    bd[entidad_str][id_add-1]._ID_venta.add(self._id)  
                    break
        return id_add
    
    def __load_rel__(self, ids, id_add, entidad, bd, entidad_str):            
        
        while True:
            try: 
                id_t = {int(input("\tIngrese ID: \t"))}
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
        self._borrado      = 1
        
    def __restartrel__(self, bd, id_t):
        for i in range(len(bd['clientes'])):
            try:
                bd['clientes'][i]._ID_venta.discard(self._id)
            except:
                pass
        
        for i in range(len(bd['cuadros'])):
            try:
                if bd['cuadros'][i]._ID_venta == id_t:
                    bd['cuadros'][i]._ID_venta = None
            except:
                pass
        
        self._precio       = None
        self._fecha        = None
        self._ID_cuadros   = None
        self._ID_clientes  = None
    
    def __modificacion__(self, bd, id_t):
        self.__restartrel__(bd, id_t)
        
        while True:
            self.precio       = input("\tIngrese Precio:  ")
            self.fecha        = input("\tIngrese Fecha:   ")
            
            if not(self._precio == None or self.fecha == None):
                break
        
        self._ID_cuadros  = 0
        self._ID_clientes = 0
            
        self.__relacion__(bd)
        
    def __str__(self):
        return (
                f" ID:             {self._id}\n"
                f" Precio:         ${self._precio}.00\n"
                f" Fecha de venta: {self.fecha}\n"
                f" LA VENTA {self._id} se relaciona con:\n"
                f" ID Cuadro:      {self._ID_cuadros}\n"
                f" ID Cliente:     {self._ID_clientes}\n"
            )

'''
try:
    prueba = Venta(1, "Arte", 1500.32, "05/09/2023", "Rodrigo")
    print(prueba)
except:
    pass
'''
     