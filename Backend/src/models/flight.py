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
        
    def __str__(self):
        return f"{self.codigo}"
        
    
    