class Ejercicio: 

    def __init__(self, nombre, descripcion ):
        self._nombre = nombre
        self._descripcion = descripcion
        
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, n):
        self._nombre = n
        
    @property
    def descripcion(self):
        return self._descripcion
    
    @descripcion.setter
    def descripcion(self, r):
        self._descripcion = r
        