#Importar modulos 
import re
import pickle
import os
import sys
from   enum import Enum

#Importar las clases de la pinacoteca
from Cliente    import Cliente
from Pinacoteca import Pinacoteca
from Pintor     import Pintor
from Cuadro     import Cuadro
from Escuela    import Escuela
from Mecenas    import Mecena
from Venta      import Venta


#Crear la clase del sistema gestor de pinacotecas
class SGP():
    #Generar archivo de texto donde guardaremos los objetos
    BD_NOMBRE_ARCHIVO = "sgp_bd.txt"
    
    #Constructor
    def __init__(self) -> None:
        #Creamos un diccionario de listas donde guardamos los registros
        self._bd = {"pinacotecas":[], "clientes":[], "cuadros": [], "escuelas":[], "mecenas": [], "pintores": [], "ventas": []}
    
    # Diccionario de llaves string y clases
        self._entidades_clases = {
            "Cliente":    Cliente, 
            "Pinacoteca": Pinacoteca, 
            "Pintor":     Pintor, 
            "Cuadro":     Cuadro, 
            "Escuela":    Escuela, 
            "Mecena":     Mecena, 
            "Venta":      Venta
        }
        
    def ejecutar(self):
        #Si existe un archivo en la carpeta con el nombre sgp_bd.txt, lo cargamos
        if os.path.exists(self.BD_NOMBRE_ARCHIVO):
            self._leer_de_disco(self.BD_NOMBRE_ARCHIVO)
        
        #Imprimimos el menu de acciones
        while True:
            accion = self._menu_general()
            if accion == self.MenuGral.SALIR:
                self._salvar_en_disco("sgp_bd.txt")
                break
            entidad = self._menu_entidades()
            if entidad == self.MenuEntidades.REGRESAR:
                continue
           
            self._controlador(accion, entidad)
    
    #Metodo donde definimos el menu de acciones
    def _menu_general(self):
        seleccion = None
        print("\nMenu de acciones\n")
        while True:
            for elemento_menu in self.MenuGral:
                print("{} - {}".format(elemento_menu.value, elemento_menu.name))
            try:
                seleccion = int(input("Seleccione un opcion: "))
                seleccion = self.MenuGral(seleccion)
                return seleccion
            except EOFError as err:
                print("Programa terminado ... Adios\n")
                break
            except KeyboardInterrupt as err:
                print("Programa terminado ... Adios\n")
                break
            except ValueError as err:
                print("Seleccion incorrecta ... intentelo nuevamente\n")
                continue
            except KeyError as err:
                print("Seleccion incorrecta ... intentelo nuevamente\n")
                continue
    
    #Metodo donde definimos el menu de entidades
    def _menu_entidades(self):
        seleccion = None
        print("\nMenu de entidades\n")
        while True:
            for elemento_menu in self.MenuEntidades:
                print("{} - {}".format(elemento_menu.value, elemento_menu.name))
            try:
                seleccion = int(input("Seleccione una opcion: "))
                seleccion = self.MenuEntidades(seleccion)
                return self.MenuEntidades(seleccion)
            except EOFError as err:
                print("Programa terminado ... Adios\n")
                break
            except KeyboardInterrupt as err:
                print("Programa terminado ... Adios\n")
                break
            except ValueError as err:
                print("Seleccion incorrecta ... intentelo nuevamente\n")
                continue
            except KeyError as err:
                print("Seleccion incorrecta ... intentelo nuevamente\n")
                continue
        return seleccion
    
    #Controlador (Donde decimos a qué metodo nos referimos según el input del usuario) 
    def _controlador(self, accion, entidad):
        #Llamamos al metodo de altas 
        if accion == self.MenuGral.ALTAS:
            self._alta(entidad)
        #Llamamos al metodo de bajas
        elif accion == self.MenuGral.BAJAS:
            self._baja(entidad)
        #Llamamos al metodo de modificaciones 
        elif accion == self.MenuGral.MODIFICACIONES:
            self._modificaciones(entidad)
        #Llamamos al metodo de consultas 
        elif accion == self.MenuGral.CONSULTAS:
            self._consultas(entidad)
    
    #Metodo de altas
    def _alta(self, entidad):
        # Segun el input, llamamos a la clase indicada y extaraemos su nombre
        nombre_clase   = entidad.name.title()
        #globals crea un diccionario con todas las variables globales de la clase
        nueva_entidad  = globals()[nombre_clase]
        
        # Con vars hacemos un diccionario, las llaves son los nombres de los metodos y los valores son los predeterminados de las clases
        dicc_atributos = vars(nueva_entidad)
        # atributos es una lista solo con las llaves, los nombres, de los metodos de la clase
        atributos      = [atributo for atributo in dicc_atributos.keys() if not re.match("^__.+__$", atributo)]
        
        
        # Segun la clase, cambiamos el nombre para la lista creada (Realmente lo unico que hace es hacer plural el nombre para que coincida con las listas de la linea 26)
        if nombre_clase.lower() == "pintor":
            lista_entidad = self._bd[nombre_clase.lower() + "es"]
        else:
            lista_entidad = self._bd[nombre_clase.lower() + "s"]
        
        # Asignamos ID automaticamente para cada clase
        if lista_entidad:
            #Buscamos el ultimo ID asignado en la lista y hacemos +1 para el siguiente a registrar
            ultimo_registro = lista_entidad[-1]
            ultimo_id = ultimo_registro.id
            nuevo_id = ultimo_id + 1
        else:
            # Si está vacía, pues 1
            nuevo_id = 1
        
        # Pedimos que ingresen los valores de la clase
        while True:
            try:
                print("\nIntroduzca los valores de {}:\n".format(nombre_clase))
                atributo_valor = {}
                # Según los atributos disponibles, el for hara un bucle hasta que se termine los atributos
                for atributo in atributos:
                    if atributo == "id":
                        print("\tID: ", nuevo_id)
                        continue  # El ID se asigna automaticamente, entonces lo ignoramos
                    #Recibimos el input del usuario
                    atributo_valor[atributo] = input("\t{}: ".format(atributo.title()))
                    #Creamos una tupla de listas, donde guardamos el ID y los inputs
                values    = tuple([nuevo_id,] + list(atributo_valor.values()))
                # Hacemos una nueva clase, desempaquetando la tupla values
                new_class = nueva_entidad(*values)
                # Definimos una bandera como 2
                flag = 2
                
                for atributo in atributos:
                    #Si hay un atributo que sea None, definimos la bandera como 1, que hace que no salga el ciclo
                    if getattr(new_class, atributo) is None:
                        flag = 1
                        break
                try:
                    new_class.__relacion__(self._bd)
                except:
                    pass
                
                if flag == 2: #En el momento que no redefinamos la bandera como 1, salimos del ciclo
                    break
                
            except AttributeError: #Si hay un error, 1 y se bucla
                flag = 1
                continue

        print(new_class)
        #Despues de imprimir, llamamos al metodo agregar lista
        self._agregar_a_lista(new_class, nombre_clase)
    #Definimos el metodo de bajas
    def _baja(self, entidad):
        #Lo mismo de hacer plural la clase para que coincida con el nombre de las listas de la linea 26
        if entidad.name.lower() == "pintor":
            entidad_str = entidad.name.lower() + "es"
        else:
            entidad_str = entidad.name.lower() + "s"
        while True:
            try:
                # Esperamos el input del usuario que nos diga que objeto borrar
                id_baja = int(input("\tIngrese ID de " + entidad.name.lower() + " a borrar (0 - Salir): \t"))
                #Si nos da un 0, salimos
                if id_baja == 0:
                    break
                #Si nos da un numero mayor que cero, borramos el objeto con el ID dado
                elif id_baja >= 0:
                    #Llamamos al metodo de baja de la clase
                    self._bd[entidad_str][id_baja-1].__baja__(self._bd, id_baja)
                else:
                    raise
                #Si el ID no existe en nuestra base, imprimimos que hubo un error
            except:
                print("ID ingresado erroneo")
    # Definimos el metodo de modificaciones
    def _modificaciones(self, entidad):
        #Lo de las listas de la linea 26
        if entidad.name.lower() == "pintor":
            entidad_str = entidad.name.lower() + "es"
        else:
            entidad_str = entidad.name.lower() + "s"
        while True:
            try:
                #Recibimos el input del usuario
                id_mod = int(input("\tIngrese ID de " + entidad.name.lower() + " a Modificar (0 - Salir): \t"))
                #Si recibimos 0, slaimos
                if id_mod == 0:
                    break
                #Si nos da un numero mayor que cero, moddificamos el objeto con el ID dado
                elif id_mod >= 0:
                    #Llamamos al metodo de modificaciones de la clase
                    self._bd[entidad_str][id_mod-1].__modificacion__(self._bd, id_mod)
                    print(self._bd[entidad_str][id_mod-1])
                    break
                else:
                    raise
            except:
                #Si el ID no existe en nuestra base, imprimimos que hubo un error
                print("ID ingresado erroneo")
        
#Definimos el metodo de consultas
    def _consultas(self, entidad):
        #Listas de la linea 26
        if entidad.name.lower() == "pintor":
            entidad_str = entidad.name.lower() + "es"
        else:
            entidad_str = entidad.name.lower() + "s"
        #For que imprime todos los objetos en la lista
        for obj in self._bd[entidad_str]:
            try:
                #Si hay una bandera de que algo se borro, lo saltamos
                if obj._borrado == 1:
                    pass
            except:
                print(obj)
                
        
    #Metodo de añadir a la base de datos
    def _agregar_a_lista(self, objeto, nombre_clase):
        if nombre_clase.lower() == "pintor":
            nombre_clase = nombre_clase.lower() + "es"
        else: 
            nombre_clase = nombre_clase.lower() + "s"
            #Con append agregamos el objeto a la lista de la clase
        self._bd[nombre_clase].append(objeto)
    
    #Metodo para guardar el archivo
    def _salvar_en_disco(self, nombre_archivo):
        with open(nombre_archivo, "wb") as archivo:
            pickle.dump(self._bd, archivo)
    
    #Metodo para leer el archivo (Si existe dicho archivo)
    def _leer_de_disco(self, nombre_archivo):
        with open(nombre_archivo, "rb") as archivo:
            self._bd = pickle.load(archivo)
    
    #Subclase del menu de acciones
    class MenuGral(Enum):
        ALTAS          = 1
        BAJAS          = 2
        MODIFICACIONES = 3
        CONSULTAS      = 4
        SALIR          = 5
    
    #Subclase del menu de clases
    class MenuEntidades(Enum):
        CLIENTE     = 1
        CUADRO      = 2
        ESCUELA     = 3
        MECENA      = 4
        PINACOTECA  = 5
        PINTOR      = 6
        VENTA       = 7
        REGRESAR    = 8