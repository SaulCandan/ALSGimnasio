class Cliente:

    def __init__(self, nombre, dni, edad):
        self._nombre = nombre
        self._dni = dni
        self._edad = edad
        self._series_oids = []
        
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, n):
        self._nombre = n

    @property
    def dni(self):
        return self._dni
    
    @dni.setter
    def dni(self, n):
        self._dni = n
    
    @property
    def edad(self):
        return self._edad
    
    @edad.setter
    def edad(self, n):
        self._edad = n
    
    @property
    def oids_series(self):
        if not self.__dict__.get("_series_oids"):
            self._series_oids = []
        return self._series_oids
    
    def get_oids_series(self):
        return self.oids_series
    
    def add_serie_oid(self, serie):
        self.oids_series.append(serie)
        
    def del_serie_oid(self, serie_oid):
        self.oids_series.remove(serie_oid)
        
    