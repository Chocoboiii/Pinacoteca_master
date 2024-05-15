#IMPORTAR LIBRERIAS 
import re
import pickle
import os
import sys
from   enum import Enum

#IMPORTAR CLASES QUE CONFORMAN A LA BASE DE DATOS DE LA PINOTECA
from Clase1_Cliente    import Cliente
from Clase2_Pinacoteca import Pinacoteca
from Clase3_Pintor     import Pintor
from Clase4_Cuadro     import Cuadro
from Clase5_Escuela    import Escuela
from Clase6_Mecenas    import Mecena
from Clase7_Venta      import Venta


#CREAR CLASE PARA EL SISTEMA GESTOR DE LA PINOTECA
class SGP():
    #GENERAR NOMBRE DEL ESPACIO PARA LA BD
    BD_NOMBRE_ARCHIVO = "sgp_bd.txt"
    
    #INICIALIZAR CONSTRUCTOR
    def __init__(self) -> None:
        #SE CREA UN DICCIONARIO DE LISTAS DONDE SE GUARDARAN LOS REGISTROS CORRESPONDIENTES DE LA BASE DE DATOS
        self._bd = {"pinacotecas":[], "clientes":[], "cuadros": [], "escuelas":[], "mecenas": [], "pintores": [], "ventas": []}
    
    # Mapa de nombres de entidades a clases
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
        #VALIDAR SI ES QUE EXISTE UN REGISTRO CREADO PREVIAMENTE, PARA CARGARLO O CREAR UNO NUEVO
        if os.path.exists(self.BD_NOMBRE_ARCHIVO):
            self._leer_de_disco(self.BD_NOMBRE_ARCHIVO)
        
        #PRESENTAR EL MENU DE ACCIONES PARA MANIPULAR LA BASE DE DATOS
        while True:
            accion = self._menu_general()
            if accion == self.MenuGral.SALIR:
                self._salvar_en_disco("sgp_bd.txt")
                break
            entidad = self._menu_entidades()
            if entidad == self.MenuEntidades.REGRESAR:
                continue
           
            self._controlador(accion, entidad)
    
    #METODO PARA IMPRIMIR EL MENU GENERAL DEL SISTEMA GESTOR
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
                print("Seleccion incorrecta ... intentelo nuevamente")
                continue
    
    #METODO PARA IMPRIMIR EL MENU DE ENTIDADES SE CONFORMAN EL SISTEMA GESTOR
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
    
    #METODO DE CONTROLADOR 
    def _controlador(self, accion, entidad):
        #ACCESO A DAR ALTA DE UN REGISTRO 
        if accion == self.MenuGral.ALTAS:
            self._alta(entidad)
        #ACCESO A DAR DE BAJA UN REGISTRO 
        elif accion == self.MenuGral.BAJAS:
            self._baja(entidad)
        #ACCESO A MODIFICAR UN REGISTRO 
        elif accion == self.MenuGral.MODIFICACIONES:
            self._modificaciones(entidad)
        #ACCESO CONSULTAR UN REGISTRO 
        elif accion == self.MenuGral.CONSULTAS:
            self._consultas(entidad)
    
    #METODO ALTA DE REGISTRO
    def _alta(self, entidad):
        # LLAMAMOS A LA CLASE CON SU TITULO
        nombre_clase   = entidad.name.title()
        nueva_entidad  = globals()[nombre_clase]
        
        # CREAMOS UNA NUEVA ENTIDAD DE ESA CLASE
        dicc_atributos = vars(nueva_entidad)
        atributos      = [atributo for atributo in dicc_atributos.keys() if not re.match("^__.+__$", atributo)]
        
        
        # IDENTIFICAR LA LISTA CORRESPONDIENTE A LA ENTIDAD
        if nombre_clase.lower() == "pintor":
            lista_entidad = self._bd[nombre_clase.lower() + "es"]
        else:
            lista_entidad = self._bd[nombre_clase.lower() + "s"]
        
        # ASIGNAR AUTOMATICAMENTE EL ID A LA NUEVA ENTIDAD
        if lista_entidad:
            #OBTENER EL ÚLTIMO ID REGISTRADO EN LA LISTA
            ultimo_registro = lista_entidad[-1]
            ultimo_id = ultimo_registro.id
            nuevo_id = ultimo_id + 1
        else:
            # SI LA LISTA ESTA VACÍA ASIGNAR AUTOMATICAMENTE EL ID
            nuevo_id = 1
        
        # PEDIR AL USUARIO QUE INGRESE LOS VALORES DE LOS ATRIBUTOS
        while True:
            try:
                print("\nIntroduzca los valores del {}:\n".format(nombre_clase))
                atributo_valor = {}
                
                for atributo in atributos:
                    if atributo == "id":
                        print("\tID: ", nuevo_id)
                        continue  # SALTAR EL ATRIBUTO ID, YA QUE SE ASIGNA AUTOMÁTICAMENTE
                    atributo_valor[atributo] = input("\t{}: ".format(atributo.title()))  
                    
                values    = tuple([nuevo_id,] + list(atributo_valor.values()))
                new_class = nueva_entidad(*values)
                flag = 2
                
                for atributo in atributos:
                    if getattr(new_class, atributo) is None:
                        flag = 1
                        break
                try:
                    new_class.__relacion__(self._bd)
                except:
                    pass
                
                if flag == 2:
                    break
                
            except AttributeError:
                flag = 1
                continue
        print(new_class)
        self._agregar_a_lista(new_class, nombre_clase)
    
    def _baja(self, entidad):
        if entidad.name.lower() == "pintor":
            entidad_str = entidad.name.lower() + "es"
        else:
            entidad_str = entidad.name.lower() + "s"
        while True:
            try:
                id_baja = int(input("\tIngrese ID de " + entidad.name.lower() + " a borrar (0 - Salir): \t"))
                
                if id_baja == 0:
                    break
                elif id_baja >= 0:
                    self._bd[entidad_str][id_baja-1].__baja__(self._bd, id_baja)
                else:
                    raise
            except:
                print("ID ingresado erroneo")
    
    def _modificaciones(self, entidad):
        if entidad.name.lower() == "pintor":
            entidad_str = entidad.name.lower() + "es"
        else:
            entidad_str = entidad.name.lower() + "s"
        while True:
            try:
                id_mod = int(input("\tIngrese ID de " + entidad.name.lower() + " a Modificar (0 - Salir): \t"))
                
                if id_mod == 0:
                    break
                elif id_mod >= 0:
                    self._bd[entidad_str][id_mod-1].__modificacion__(self._bd, id_mod)
                    print(self._bd[entidad_str][id_mod-1])
                    break
                else:
                    raise
            except:
                print("ID ingresado erroneo")
        

    def _consultas(self, entidad):
        if entidad.name.lower() == "pintor":
            entidad_str = entidad.name.lower() + "es"
        else:
            entidad_str = entidad.name.lower() + "s"
            
        for obj in self._bd[entidad_str]:
            try:
                if obj._borrado == 1:
                    pass
            except:
                print(obj)
                
        
    #AÑADIR EL REGISTRO A LA BASE DE DATOS
    def _agregar_a_lista(self, objeto, nombre_clase):
        if nombre_clase.lower() == "pintor":
            nombre_clase = nombre_clase.lower() + "es"
        else: 
            nombre_clase = nombre_clase.lower() + "s"
            
        self._bd[nombre_clase].append(objeto)
    
    #METODO PARA GUARDAR ARCHIVO DE BASE DE DATOS
    def _salvar_en_disco(self, nombre_archivo):
        with open(nombre_archivo, "wb") as archivo:
            pickle.dump(self._bd, archivo)
    
    #METODO PARA LEER ARCHIVO DE BASE DE DATOS
    def _leer_de_disco(self, nombre_archivo):
        with open(nombre_archivo, "rb") as archivo:
            self._bd = pickle.load(archivo)
    
    #SUBCLASE DE ACCIONES ASOCIADAS A UN NUMERO
    class MenuGral(Enum):
        ALTAS          = 1
        BAJAS          = 2
        MODIFICACIONES = 3
        CONSULTAS      = 4
        SALIR          = 5
    
    #SUBCLASE DE ACCIONES ASOCIADAS A LAS ENTIDADES DE LA BASE DE DATOS
    class MenuEntidades(Enum):
        CLIENTE     = 1
        CUADRO      = 2
        ESCUELA     = 3
        MECENA      = 4
        PINACOTECA  = 5
        PINTOR      = 6
        VENTA       = 7
        REGRESAR    = 8