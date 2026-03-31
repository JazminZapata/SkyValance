class Flight:
    
    def __init__(self, codigo, origen, destino, horaSalida, precioBase, pasajeros,promocion, alerta):

        self.codigo = codigo
        self.origen = origen
        self.destino = destino
        self.horaSalida = horaSalida
        self.precioBase = precioBase
        self.pasajeros = pasajeros
        self.promocion = promocion
        self.alerta = alerta
        # Asignamos un atributo adicional que es el número del vuelo, que se extrae del código para facilitar la comparación entre vuelos (por ejemplo, para la inserción en el árbol)
        self.codigo_comp = self._extraerNumero(codigo)
    
    # Method to return the string representation of the flight, we will use the code as the identifier of the flight
        
    def __str__(self):
      return f"{self.codigo}"
  
    #  función interna
    def _extraerNumero(self, texto):
        numeros = ''.join(filter(str.isdigit, texto))

        if numeros:
            return int(numeros)

        return texto  # por si no tiene números       
    
    