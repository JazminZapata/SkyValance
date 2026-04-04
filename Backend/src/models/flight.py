class Flight:

    def __init__(
        self,
        codigo,
        origen,
        destino,
        horaSalida,
        precioBase,
        pasajeros,
        promocion,
        alerta,
    ):

        self.codigo = codigo
        self.origen = origen
        self.destino = destino
        self.horaSalida = horaSalida
        self.precioBase = precioBase
        self.pasajeros = pasajeros
        self.promocion = promocion
        self.alerta = alerta
        # Asignamos un atributo adicional que es el número del vuelo, que se extrae del código para facilitar la comparación entre vuelos (por ejemplo, para la inserción en el árbol)
        self.codigo_comp = Flight.extractNum(codigo)

    # Method to return the string representation of the flight, we will use the code as the identifier of the flight

    def __str__(self):
        return f"{self.codigo}"

    # Definir get priority para calcular la prioridad del vuelo
    # "“Se incluyó la prioridad como un atributo adicional en la serialización del árbol para soportar decisiones operativas sin afectar la estructura AVL.”"
    def getPriority(self):
        return None

    def getIngresoBase(self, precioFinal):
        return self.pasajeros * precioFinal

    
    #  función interna (estatica para poderla usar en flightService) para extraer el número del código del vuelo, asumiendo que el código tiene un formato como "FL1234" y queremos extraer el número 1234 para comparaciones numéricas
    @staticmethod
    def extractNum(text):
        nums = ''.join(filter(str.isdigit, text)) # filtra los números y los junta en un string

        if nums:
            return int(nums)

        return text

