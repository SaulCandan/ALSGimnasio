class Serie: 

    def __init__(self, ejercicio, repeticiones, fecha ):
        self._ejercicio = ejercicio
        self._repeticiones = repeticiones
        self._fecha = fecha
        
    @property
    def ejercicio(self):
        return self._ejercicio
    
    @ejercicio.setter
    def ejercicio(self, n):
        self._ejercicio = n
        
    @property
    def repeticiones(self):
        return self._repeticiones
    
    @repeticiones.setter
    def repeticiones(self, r):
        self._repeticiones = r
        
    @property
    def fecha(self):
        return self._fecha
    
    @fecha.setter
    def fecha(self, n):
        self._fecha = n
        
    

