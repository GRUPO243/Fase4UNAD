from abc import ABC, abstractmethod
# Esta importación se usa para la abstracción
import logging
# Esta importación se usa para configurar los niveles de error, automáticamente añade la fecha, la hora y la línea de código donde ocurrió el problema en el archivo de logs.
from datetime import datetime
# Esta imoportación se usa para la gestión de fechas  y tiempos

# A continuación, se definen las clases de excepción personalizadas mediante la herencia de la clase base (Exception) de Python. Estas clases permiten capturar errores específicos de validación de datos. Ante cualquier fallo durante la ejecución, la excepción será lanzada y capturada por el sistema de gestión de (logs), asegurando el registro detallado del evento sin interrumpir la continuidad del programa. 
class Validaciones (Exception):
    pass
# Validación de que los input no estén vacios
class VacioError (Validaciones):
    pass
# Validación de que (nombre) solo contenga string 
class NombreError (Validaciones):
    pass
# Validación de que (ID) sea númerico y que este en el rango asignado
class IdError (Validaciones):
    pass
# Validación de que la (edad) sea un entero y esté en el rango asignado
class EdadError (Validaciones):
    pass
# Validación de que (cargo) sea una de las opciones en la lista del programa
class CargoError (Validaciones):
    pass



#LE CAMBIEEEEEE ESTA LINEA





# A partir de esta linea se crea la clase abstracta (persona), que heredará a cliente sus atributos, en esta clase se realiza la validación correspondiente a (nombre) e (ID). Esta clase define la estructura base para cualquier individuo en el sistema y a su vez, no permite instanciación directa, (ABC). Gestiona la identidad (Nombre/ID)
class Persona(ABC):
    def __init__(self, nombre, ID):
        # Esta validación evita strings vacíos o con puros espacios
        if not nombre.strip() or not ID.strip():
            raise VacioError ("Error: El espacio no tiene información")
        # A continuación se valida que si algún caracter en el nombre es un digito, este genere un error 
        if any(char.isdigit() for char in nombre):
            raise NombreError("Error: El nombre no puede contener números.")
        # Debe ser numérico y de 6 dígitos
        if not ID.isdigit():
            raise IdError ("Error: El ID solo debe contener numeros")
        if int(ID) < 100000 or int(ID) > 999999:
            raise IdError("Error: El numero de identificación no es valido")
        self.__nombre = nombre
        self.__ID = ID 
        
    # Se crean los métodos getter para que Cliente pueda leer estos datos luego
    def get_nombre(self):
        return self.__nombre

    def get_id(self):
        return self.__ID
        
# Creación de la clase (Cliente), quien hereda de (Persona) el nombre e ID. Añade atributos específicos y aplica filtros de edad y cargos autorizados por Software FJ.      
class Cliente(Persona):
    def __init__(self, nombre, ID, edad, institucion, cargo):
        # Se valida primero que (edad, institución y cargo) no estén vacios antes de que se ejecute (nombre e ID) en esta clase
        if not edad.strip() or not institucion.strip() or not cargo.strip():
            raise VacioError ("Error: El espacio no tiene información")
        super().__init__(nombre, ID)
        cargo_valido = ["Estudiante", "Docente", "Asesor", "Asociado", "Comerciante", "Externo"]
        if int(edad) < 18 or int(edad) > 99:
            raise EdadError ("Error: La edad está fuera del rango permitido")
        if cargo not in cargo_valido:
            raise CargoError ("Error: El cargo no se encuentra en la lista")
            
        self.edad = edad
        self.institucion = institucion
        self.__cargo = cargo
        
    def get_cargo(self):
        return self.__cargo 
