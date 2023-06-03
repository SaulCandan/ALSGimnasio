import flask
import flask_login
import sirope
from flask_login import login_manager
import json
import sys
import os


sys.path.append(os.path.join(sys.path[0], '../..'))
sys.path.append(os.path.join(sys.path[0], '../../..'))
from model.monitor import Monitor
from model.ejercicio import Ejercicio

import views.crudcliente.crudclienteview as crudclienteview

ruta = os.path.realpath(__file__)
size = len(ruta)
src= ruta[:size - 18]

os.chdir(src)
@staticmethod
def recupera_ejercicios(fn):
    toret = []
    with open(fn, "r") as f:
        ejers = json.load(f)
    for d in ejers:
        n = Ejercicio("","")
        n.__dict__ = d
        toret.append(n)
        
    return toret
    
def create_app():
    lmanager = flask_login.login_manager.LoginManager()
    fapp = flask.Flask(__name__, instance_relative_config=True)
    syrp = sirope.Sirope()
    
    try:
        ejercicios_list = recupera_ejercicios("instance/ejercicios.json")
        for e in ejercicios_list:
            syrp.save(e)
    except:
        print("El archivo ejercicios.json no existe o está vacío")
        
    
    
    fapp.config.from_file("config.json", load=json.load)
    lmanager.init_app(fapp)
    fapp.register_blueprint(crudclienteview.crudcliente_blprint)
    
    
    return fapp, lmanager, syrp


#Inicializamos
app, lm, srp = create_app()

@lm.user_loader
def user_loader(idUser):
    return Monitor.find(srp, idUser)

@app.route('/')
def get_index():
    flask_login.logout_user()
    return flask.render_template("index.html")

@app.route('/logout')
def logout():
    flask.flash("User logged out")
    return flask.redirect('/')

@lm.unauthorized_handler
def unauthorized_handler():
    flask.flash("Unauthorized")
    return flask.redirect("/")

@app.route("/login", methods=["POST"])
def login():
    
    idUser_txt = flask.request.form.get("input_idUser")
    password_txt = flask.request.form.get("input_password")
     
    if not idUser_txt:
            flask.flash("¡Es necesario el login previo!")
            return flask.redirect("/")
        
    else:
        if not password_txt:
            flask.flash("¿Y la contraseña?")
            return flask.redirect("/")
        
        usr = Monitor.find(srp, idUser_txt)
        if not usr:
            usr = Monitor(idUser_txt, password_txt)
            srp.save(usr)
            flask.flash("Usuario registrado")
            return flask.redirect("/")
        
        elif not usr.chk_password(password_txt):
            flask.flash("Contraseña incorrecta")
            return flask.redirect("/")
   
        flask_login.login_user(usr)
    
    return flask.redirect("/crudcliente")



#Runeamos
print("Empezamos...") 
print(os.getcwd())

app.run()