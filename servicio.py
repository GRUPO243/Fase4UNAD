 servicio.py

# IMPORTACIONES

# ABC permite crear clases abstractas (que no se pueden instanciar directamente)
# abstractmethod obliga a que las clases hijas implementen ciertos métodos
from abc import ABC, abstractmethod

# logging permite registrar errores en un archivo (log.txt)
import logging

# Configuración del archivo de logs
# Se guardarán los errores con fecha, hora y tipo de error
logging.basicConfig(
    filename="log.txt",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# EXCEPCIÓN PERSONALIZADA
class ServicioError(Exception):
    """
    Clase de excepción personalizada para manejar errores en los servicios.
    Hereda de Exception para poder usar try/except.
    """
    pass


# CLASE ABSTRACTA
class Servicio(ABC):
    """
    Clase base abstracta.
    Define la estructura que deben seguir todos los servicios.
    No se puede crear un objeto directamente de esta clase.
    """

    def __init__(self, nombre):
        # Validación: el nombre no puede estar vacío o solo con espacios
        if not nombre.strip():
            raise ServicioError("El nombre del servicio no puede estar vacío")

        # Atributo común para todos los servicios
        self.nombre = nombre

    @abstractmethod
    def calcular_costo(self):
        """
        Método abstracto.
        Cada servicio debe implementar su propia forma de calcular el costo.
        """
        pass

    @abstractmethod
    def describir(self):
        """
        Método abstracto.
        Cada servicio debe describirse de forma diferente.
        """
        pass


# SERVICIO 1: SALA
class Sala(Servicio):
    """
    Clase que representa el servicio de alquiler de salas.
    Hereda de Servicio.
    """

    def __init__(self, nombre, horas):
        # Llama al constructor de la clase padre (Servicio)
        super().__init__(nombre)

        # Validación: las horas deben ser mayores a 0
        if horas <= 0:
            raise ServicioError("Las horas deben ser mayores a 0")

        self.horas = horas

    def calcular_costo(self):
        """
        Implementación del método abstracto.
        Calcula el costo según las horas.
        """
        return 50000 * self.horas

    def describir(self):
        """
        Describe el servicio.
        """
        return f"Sala '{self.nombre}' reservada por {self.horas} horas"


# SERVICIO 2: EQUIPO
class Equipo(Servicio):
    """
    Clase que representa el alquiler de equipos.
    """

    def __init__(self, nombre, dias):
        super().__init__(nombre)

        # Validación: los días deben ser mayores a 0
        if dias <= 0:
            raise ServicioError("Los días deben ser mayores a 0")

        self.dias = dias

    def calcular_costo(self):
        """
        Calcula el costo según los días.
        """
        return 30000 * self.dias

    def describir(self):
        """
        Describe el servicio.
        """
        return f"Equipo '{self.nombre}' alquilado por {self.dias} días"


# SERVICIO 3: ASESORÍA
class Asesoria(Servicio):
    """
    Clase que representa el servicio de asesorías.
    """

    def __init__(self, nombre, horas):
        super().__init__(nombre)

        # Validación: las horas deben ser mayores a 0
        if horas <= 0:
            raise ServicioError("Las horas deben ser mayores a 0")

        self.horas = horas

    def calcular_costo(self):
        """
        Calcula el costo según las horas.
        """
        return 80000 * self.horas

    def describir(self):
        """
        Describe el servicio.
        """
        return f"Asesoría '{self.nombre}' por {self.horas} horas"


# MÉTODO EXTRA (SOBRECARGA)
def calcular_costo_descuento(servicio, descuento=0):
    """
    Función que calcula el costo con descuento.
    Simula sobrecarga de métodos (porque cambia el comportamiento).
    
    Parámetros:
    - servicio: objeto de tipo Servicio
    - descuento: valor entre 0 y 1 (ej: 0.2 = 20%)
    """

    # Validación del descuento
    if descuento < 0 or descuento > 1:
        raise ServicioError("El descuento debe estar entre 0 y 1")

    return servicio.calcular_costo() * (1 - descuento)


# PRUEBAS (SIMULACIÓN)
# Este bloque solo se ejecuta si corres este archivo directamente
if __name__ == "__main__":

    print("=== PRUEBAS DE SERVICIOS ===")

    # Caso válido
    try:
        s1 = Sala("Sala VIP", 2)
        print(s1.describir())
        print("Costo:", s1.calcular_costo())
    except ServicioError as e:
        logging.error(e)
        print("Error:", e)

    # Otro caso válido
    try:
        s2 = Equipo("Laptop", 3)
        print(s2.describir())
        print("Costo:", s2.calcular_costo())
    except ServicioError as e:
        logging.error(e)
        print("Error:", e)

    # Otro caso válido
    try:
        s3 = Asesoria("Marketing", 1)
        print(s3.describir())
        print("Costo:", s3.calcular_costo())
    except ServicioError as e:
        logging.error(e)
        print("Error:", e)

    # Error: valor negativo
    try:
        s4 = Sala("Sala mala", -1)
    except ServicioError as e:
        logging.error(e)
        print("Error:", e)

    # Error: nombre vacío
    try:
        s5 = Equipo("", 2)
    except ServicioError as e:
        logging.error(e)
        print("Error:", e)

    # Prueba con descuento
    try:
        total_desc = calcular_costo_descuento(s1, 0.2)
        print("Costo con descuento:", total_desc)
    except ServicioError as e:
        logging.error(e)
        print("Error:", e)

    print("=== FIN DE PRUEBAS ===")