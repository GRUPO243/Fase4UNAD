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

# En esta seccion se realizan las importaciones necesarias para el funcionamiento del modulo de servicios

# Se importa ABC y abstractmethod para crear clases abstractas
from abc import ABC, abstractmethod

# Se importa logging para registrar errores en el archivo log
import logging

# CONFIGURACIÓN DEL LOG

# Configuración del archivo de logs donde se almacenarán
# los errores generados durante la ejecución del programa
logging.basicConfig(
    filename = "log.txt",
    level = logging.ERROR,
    format = "%(asctime)s - %(levelname)s - %(message)s"
)

# EXCEPCIONES PERSONALIZADAS

# Clase principal para las validaciones de servicios
class ServicioError(Exception):
    pass

# Validación para espacios vacíos
class ServicioVacioError(ServicioError):
    pass

# Validación para valores numéricos inválidos
class ValorServicioError(ServicioError):
    pass

# CLASE ABSTRACTA SERVICIO

# Esta clase abstracta representa la estructura general
# de cualquier servicio ofrecido por Software FJ.
# No puede ser instanciada directamente.
class Servicio(ABC):

    def __init__(self, nombre):

        # Validación para evitar nombres vacíos
        if not nombre.strip():
            raise ServicioVacioError("Error: El servicio no puede estar vacío")

        self.nombre = nombre

    # Método abstracto para calcular costos
    @abstractmethod
    def calcular_costo(self):
        pass

    # Método abstracto para describir servicios
    @abstractmethod
    def descripcion(self):
        pass

# CLASE SALA

# Esta clase representa el servicio de reserva de salas.
# Hereda de la clase abstracta Servicio.
class Sala(Servicio):

    def __init__(self, nombre, horas):

        # Se hereda el atributo nombre desde Servicio
        super().__init__(nombre)

        # Validación de horas
        if horas <= 0:
            raise ValorServicioError("Error: Las horas deben ser mayores a 0")

        self.horas = horas

    # Implementación del cálculo del costo
    def calcular_costo(self):
        return self.horas * 50000

    # Descripción del servicio
    def descripcion(self):
        return f"Sala '{self.nombre}' reservada por {self.horas} horas"

# CLASE EQUIPO

# Esta clase representa el servicio de alquiler de equipos.
class Equipo(Servicio):

    def __init__(self, nombre, dias):

        super().__init__(nombre)

        # Validación de días
        if dias <= 0:
            raise ValorServicioError("Error: Los días deben ser mayores a 0")

        self.dias = dias

    # Implementación del cálculo del costo
    def calcular_costo(self):
        return self.dias * 30000

    # Descripción del servicio
    def descripcion(self):
        return f"Equipo '{self.nombre}' alquilado por {self.dias} días"

# CLASE ASESORIA

# Esta clase representa el servicio de asesorías especializadas.
class Asesoria(Servicio):

    def __init__(self, nombre, horas):

        super().__init__(nombre)

        # Validación de horas
        if horas <= 0:
            raise ValorServicioError("Error: Las horas deben ser mayores a 0")

        self.horas = horas

    # Implementación del cálculo del costo
    def calcular_costo(self):
        return self.horas * 80000

    # Descripción del servicio
    def descripcion(self):
        return f"Asesoría '{self.nombre}' realizada por {self.horas} horas"

# MÉTODO ADICIONAL (SOBRECARGA SIMULADA)

# Esta función permite calcular el costo aplicando descuentos.
# Ayuda a cumplir el requisito de métodos sobrecargados.
def calcular_costo_descuento(servicio, descuento = 0):

    # Validación del descuento
    if descuento < 0 or descuento > 1:
        raise ValorServicioError("Error: El descuento debe estar entre 0 y 1")

    return servicio.calcular_costo() * (1 - descuento)

# PRUEBA DE SERVICIOS

if __name__ == "__main__":

    while True:
        try:
            # Menú principal
            print("\nSeleccione el servicio que desea crear:")
            print("1. Reserva de Sala")
            print("2. Alquiler de Equipo")
            print("3. Asesoría Especializada")
            print("4. Salir")

            opcion = input("Ingrese una opción: ")

            # Opción para salir del programa
            if opcion == "4":
                print("Programa finalizado.")
                break

            # OPCIÓN 1: SERVICIO DE SALA
            if opcion == "1":
                nombre = input("Ingrese el nombre de la sala: ")
                horas = int(input("Ingrese el número de horas: "))

                servicio = Sala(nombre, horas)

            # OPCIÓN 2: SERVICIO DE EQUIPO
            elif opcion == "2":
                nombre = input("Ingrese el nombre del equipo: ")
                dias = int(input("Ingrese el número de días: "))

                servicio = Equipo(nombre, dias)

            # OPCIÓN 3: SERVICIO DE ASESORÍA
            elif opcion == "3":
                nombre = input("Ingrese el nombre de la asesoría: ")
                horas = int(input("Ingrese el número de horas: "))

                servicio = Asesoria(nombre, horas)

            # OPCIÓN INVÁLIDA
            else:
                print("Error: Opción no válida.")
                continue

            # Mostrar información del servicio creado
            print("\nServicio creado correctamente.")
            print(servicio.descripcion())
            print("Costo total:", servicio.calcular_costo())

            # Preguntar si desea aplicar descuento
            aplicar = input("¿Desea aplicar descuento? (s/n): ").lower()

            if aplicar == "s":
                descuento = float(
                    input("Ingrese el descuento (ejemplo 0.2 para 20%): ")
                )

                total_descuento = calcular_costo_descuento(
                    servicio, descuento
                )

                print("Costo con descuento:", total_descuento)

        except ValueError:
            # Error cuando el usuario digita texto donde se
            # esperaba un número
            logging.error("Error: Se esperaba un valor numérico.")
            print("Error: Debe ingresar un valor numérico.")

        except ServicioError as e:
            # Error generado por las validaciones del sistema
            logging.error(e)
            print(e)

        except Exception as e:
            # Captura cualquier otro error inesperado
            logging.error(e)
            print("Error inesperado:", e)