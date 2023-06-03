import sirope
import flask_login
import werkzeug.security as safe

class Monitor(flask_login.UserMixin):
    
    def __init__(self, idUser, password):
        self._idUser = idUser
        self._password = safe.generate_password_hash(password)
        self._clientes_oids = []
    
    @property
    def idUser(self):
        return self._idUser
    
    @property
    def oids_clientes(self):
        if not self.__dict__.get("_clientes_oids"):
            self._clientes_oids = []
        return self._clientes_oids

    def get_id(self):
        return self.idUser

    def chk_password(self, pswd):
        return safe.check_password_hash(self._password, pswd)
    
    def get_oids_clientes(self):
        return self.oids_clientes
    
    def add_cliente_oid(self, cliente_oid):
        self.oids_clientes.append(cliente_oid)
        
    def del_cliente_oid(self, cliente_oid):
        self.oids_clientes.remove(cliente_oid)
 
    @staticmethod
    def current_user():
        usr = flask_login.current_user
        if usr.is_anonymous:
            flask_login.logout_user()
        usr = None
        return usr
    
    @staticmethod
    def find(s: sirope.Sirope, idUser: str) -> "Monitor":
        return s.find_first(Monitor, lambda u: u.idUser == idUser)