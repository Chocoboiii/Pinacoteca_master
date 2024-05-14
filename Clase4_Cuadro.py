#IMPORTAR LIBRERIAS
from datetime import datetime
from enum     import Enum

formato_fecha = "%d/%m/%Y" 
tecnicas_pintura = { "acuarela", "óleo", "acrílico", "tempera", "pastel", "fresco", "collage",
                    "impresionismo", "puntillismo", "gouache" }
class Cuadro:
    
    
    def __init__(self, id = 0, nombre = '', largo = 0, ancho = 0, 
                 fecha_creacion = '', tecnica = ''):
        self.id             = id
        self.nombre         = nombre
        self.largo          = largo
        self.ancho          = ancho
        self.fecha_creacion = fecha_creacion
        self.tecnica        = tecnica
        self._ID_pintor     = None
        self._ID_pinacoteca = None
        self._ID_venta      = None
        
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
        
    #DECORADOR NOMBRE
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
    
    #DECORADOR FECHA DE CREACION
    @property 
    def fecha_creacion(self):
        return self._fecha_creacion
    
    @fecha_creacion.setter 
    def fecha_creacion(self, fecha_creacion):
        if fecha_creacion == '':
            self._fecha_creacion = ''
            return
        try:
            #VALIDAR QUE TENGA EL FORMATO CORRECTO
            fecha_obj = datetime.strptime(fecha_creacion, formato_fecha)
            #VALIDAR QUE NO SEA UNA FECHA FUTURA A LA 
            año_actual = datetime.now().year
            if fecha_obj.year > año_actual:
                print("la fecha ingresada no es correcta")
                return None
            self._fecha_creacion = fecha_creacion
        except:
            print("El formato de la fecha de creación no es correcto")
            return None
        
    #DECORADOR DE TECNICA DE PINTURA
    @property
    def tecnica(self):
        return self._tecnica
    
    @tecnica.setter 
    def tecnica(self, tecnica):
        if tecnica == '':
            self._tecnica = ''
            return
        tecnicat = set([tecnica])
        if tecnicat.issubset(tecnicas_pintura):
            self._tecnica = tecnica
        else:
            print("La tecnica ingresada no se reconoce, las tecnicas aceptadas son {}".format(tecnicas_pintura))
            return None
    
    #METODO PARA RELACIONAR LA PINCOTECA CON OTRAS IDENTIDATES
    def __relacion__(self, bd):
        while True:
            try: 
                print("Desea relacionar al pintor añadido con un Pintor, Pinacoteca o Venta:\n\tSI\t1\n\tNO\t0\n")
                ans = int(input("Seleccione una opcion: "))
                if ans == 1:
                    entidad = self.__menu_entidades__()
                    #SALIR EN CASO DE NO RELACIONAR
                    if entidad == self.__Menu__.CONTINUAR:
                        pass
                    
                    if entidad == self.__Menu__.PINTOR:
                        id_add = self.__ids__('pintor', bd)
                        if id_add == 0:
                            pass
                        else:
                            self._ID_pintor = id_add
                        
                    if entidad == self.__Menu__.PINACOTECA:
                        id_add = self.__ids__('pinacoteca', bd)
                        if id_add == 0:
                            pass
                        else:
                            self._ID_pinacoteca = id_add  
                        
                    if entidad == self.__Menu__.VENTA:
                        id_add = self.__ids__('venta', bd)
                        if id_add == 0:
                            pass
                        else:
                            self._ID_venta = id_add   
                        
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
        
        if entidad == 'pintor':
            entidad_str = 'pintores'
        else:
            entidad_str = entidad + 's'
            
        #SE CREAN LISTAS TEMPORALES PARA AÑADIR Y REGISTRAR LOS ID'S
        ids = set(); id_add = set()
        #SE OBTIENE UN SET CON LOS ID'S EXISTENTES EN LA BD
        for obj in bd[entidad_str]:
            ids.add(obj.id)
        
        print('\tIngrese el ID de '+ entidad +' que le corresponde al Cuadro\n\t (0 - Salir)\n')

        id_add = int(*self.__load_rel__(ids, id_add, entidad, bd, entidad_str))
        
        if id_add == 0:
            pass
        else:
            bd[entidad_str][id_add-1]._ID_cuadros.add(self._id)
        
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
        self._borrado = 1
        
    def __restartrel__(self, bd, id_t):
        for i in range(len(bd['pintores'])):
            try:
                bd['pintores'][i]._ID_cuadros.discard(self._id)
            except:
                pass
        
        for i in range(len(bd['pinacotecas'])):
            try:
                bd['pinacotecas'][i]._ID_cuadros.discard(self._id)
            except:
                pass
        
        for i in range(len(bd['ventas'])):
            try:
                if bd['ventas'][i]._ID_cuadros == id_t:
                    bd['ventas'][i]._ID_cuadros = None
            except:
                pass

        self._nombre         = None
        self._largo          = None
        self._ancho          = None
        self._fecha_creacion = None
        self._tecnica        = None
        self._ID_pintor      = None
        self._ID_pinacoteca  = None
        self._ID_venta       = None
    
    def __modificacion__(self, bd, id_t):
        self.__restartrel__(bd, id_t)
        
        while True:
            self.nombre         = input("\tIngrese Nombre:            ")
            self.largo          = input("\tIngrese Largo:             ")
            self.ancho          = input("\tIngrese Ancho:             ")
            self.fecha_creacion = input("\tIngrese Fecha de Creación: ")
            self.tecnica        = input("\tIngrese Técnica:           ")
            
            if not(self._nombre == None or self._largo == None or self._ancho == None 
                   or self._fecha_creacion == None or self._tecnica == None):
                break
        
        self._ID_pintor     = None
        self._ID_pinacoteca = None
        self._ID_venta      = None
            
        self.__relacion__(bd)
    
    #SUBCLASE DE ACCIONES ASOCIADAS A UN NUMERO
    class __Menu__(Enum):
        PINTOR        = 1
        PINACOTECA    = 2
        VENTA         = 3
        CONTINUAR     = 4

    def __str__(self) -> str:
        return (
            f" ID:                {self._id}\n"
            f" Nombre:            {self._nombre}\n"
            f" Largo:             {self._largo} cm\n"
            f" Ancho:             {self._ancho} cm\n"
            f" Fecha de creación: {self._fecha_creacion}\n"
            f" Tecnica:           {self._tecnica}\n"
            f" El cuadro {self._nombre} se relaciona con:\n"
            f" ID Pintor:         {self._ID_pintor}\n"
            f" ID Pinacoteca:     {self._ID_pinacoteca}\n"
            f" ID Venta:          {self._ID_venta}\n"
        )

'''
try:        
    prueba = Cuadro(1,"Pinta",23, 321, "02/12/2024", "acuarela", "2")
    print(prueba)
except:
    pass
FALTA:
    
    VALIDAR:
        1. QUE EXISTA EN LA BASE DE DATOS
        2. QUE EL ID NO SE REPITA
'''