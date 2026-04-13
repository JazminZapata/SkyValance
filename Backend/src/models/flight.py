class Flight:

    def __init__(self, codigo, origen, destino, horaSalida, precioBase, pasajeros, promocion, alerta):
        self._codigo = codigo
        self._origen = origen
        self._destino = destino
        self._horaSalida = horaSalida
        self._precioBase = precioBase
        self._pasajeros = pasajeros
        self._promocion = promocion
        self._alerta = alerta
        # We add an extra attribute with the flight number extracted from the code
        # to make comparisons easier when inserting into the tree
        self._codigo_comp = Flight.extractNum(codigo)

    # Method to return the string representation of the flight, we will use the code as the identifier of the flight
    def __str__(self):
        return f"{self._codigo}"

    # Getters
    def getCodigo(self): 
        return self._codigo
    
    def getOrigen(self): 
        return self._origen
    
    def getDestino(self): 
        return self._destino
    
    def getHoraSalida(self): 
        return self._horaSalida
    
    def getPrecioBase(self): 
        return self._precioBase
    
    def getPasajeros(self): 
        return self._pasajeros
    
    def getPromocion(self): 
        return self._promocion
    
    def getAlerta(self): 
        return self._alerta
    
    def getCodigoComp(self): 
        return self._codigo_comp

    # Setters
    def setOrigen(self, value): 
        self._origen = value
        
    def setDestino(self, value): 
        self._destino = value
        
    def setHoraSalida(self, value): 
        self._horaSalida = value
        
    def setPrecioBase(self, value): 
        self._precioBase = value
        
    def setPasajeros(self, value): 
        self._pasajeros = value
        
    def setPromocion(self, value): 
        self._promocion = value
        
    def setAlerta(self, value): 
        self._alerta = value

    def getIngresoBase(self, precioFinal):
        return self._pasajeros * precioFinal

    # Static method to extract the number from the flight code
    # For example: "FL1234" -> 1234, used for numeric comparisons in the tree
    @staticmethod
    def extractNum(text):
        text = str(text)  # handle both strings and numbers
        nums = ''.join(filter(str.isdigit, text)) # filters digits and joins them into a string
        if nums:
            return int(nums)
        return text