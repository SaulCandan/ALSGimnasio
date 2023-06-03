import flask
import flask_login
from flask import request
import sirope
from model.monitor import Monitor
from model.cliente import Cliente
from model.serie import Serie
from model.ejercicio import Ejercicio
from datetime import datetime
import re

##BLUEPRINT
def get_blprint():
    crudcliente = flask.blueprints.Blueprint("crudcliente", __name__,
                                        url_prefix="/crudcliente",
                                        template_folder="templates",
                                        static_folder="static")
    
    syrp = sirope.Sirope()
    
    return crudcliente, syrp

crudcliente_blprint, srp = get_blprint()

#RUTA PRINCIPAL

@flask_login.login_required
@crudcliente_blprint.route("/")
def crudcliente():
    
    idUser = flask_login.current_user.get_id()
    oid_clientes = flask_login.current_user.get_oids_clientes()
    clientes = list(srp.multi_load(oid_clientes))
    
    #RECOGIDA PARAMETROS
    metodoCrud = request.args.get('metodoCrud', None)
    cliente_a_cambiar = request.args.get('cliente_a_cambiar', None)
    if metodoCrud == "Añadir":
        sust = {
            "idUser": idUser ,
            "clientes": getClientesMonitor() 
            }
        
        return flask.render_template("añadircliente.html",**sust)
    
    elif metodoCrud == "Modificar":  
        
        objeto_cliente_a_modificar = clientes[int(cliente_a_cambiar)]
        
        sust = {
        "idUser": idUser ,
        "clientes": getClientesMonitor() ,
        "objeto_cliente_a_modificar" : objeto_cliente_a_modificar,
        "cliente_a_cambiar" : cliente_a_cambiar
        }
        
        return flask.render_template("modificarcliente.html",**sust)
    
    elif metodoCrud == "Eliminar":  
        
        #ELIMINAR CLIENTE DEL ALMACENAMIENTO Y GUARDAR CAMBIOS EN USUARIO
        oidsclientes = list(oid_clientes)
        oidClienteEliminado = oidsclientes[int(cliente_a_cambiar)]
        flask_login.current_user.del_cliente_oid(oidClienteEliminado)
        srp.delete(oidClienteEliminado)
        srp.save(flask_login.current_user)
        
        sust = {
        "idUser": idUser ,
        "clientes": getClientesMonitor() 
        }
        
        return flask.render_template("crudcliente.html",**sust)
    elif metodoCrud == "Añadirserie": 
        
        objeto_cliente_a_modificar = clientes[int(cliente_a_cambiar)]
        sust = {
        "idUser": idUser ,
        "clientes": getClientesMonitor() ,
        "cliente_a_modificar" : objeto_cliente_a_modificar,
        "cliente_a_cambiar" : cliente_a_cambiar,
        "ejercicios": getEjercicios()
        }
        return flask.render_template("añadirserie.html",**sust)
    
    elif metodoCrud == "Visualizarserie": 
        
        objeto_cliente_a_modificar = clientes[int(cliente_a_cambiar)]
        series = list(srp.multi_load(objeto_cliente_a_modificar.get_oids_series()))
        for s in series:
            print(s.ejercicio)
        sust = {
        "idUser": idUser ,
        "clientes": getClientesMonitor() ,
        "cliente_a_modificar" : objeto_cliente_a_modificar,
        "cliente_a_cambiar" : cliente_a_cambiar,
        "series" : series,
        "ejercicios": getEjercicios()
        }
        return flask.render_template("visualizarserie.html",**sust)
    
    elif metodoCrud=="Eliminarserie":
        
        clientes_oid = flask_login.current_user.get_oids_clientes()
        clientes = list(srp.multi_load(clientes_oid))
        cliente = clientes[int(cliente_a_cambiar)]
        
        serie_a_cambiar = request.args.get('serie_a_cambiar', None)
        series_oid = cliente.get_oids_series()
        series = list(srp.multi_load(series_oid))
        serie = series_oid[int(serie_a_cambiar)]
        
        
        cliente.del_serie_oid(series_oid[int(serie_a_cambiar)])
        srp.delete(serie)
        srp.save(cliente)
        
        series.remove(series[int(serie_a_cambiar)])
        
        sust = {
        "idUser": idUser ,
        "clientes": getClientesMonitor() ,
        "cliente_a_modificar" : cliente,
        "cliente_a_cambiar" : cliente_a_cambiar,
        "series": series ,
        "ejercicios": getEjercicios() 
        }
        
        return flask.render_template("visualizarserie.html",**sust)
    
    else:  
        
        sust = {
        "idUser": idUser ,
        "clientes": getClientesMonitor() ,
        "metodoCrud": metodoCrud ,
        "cliente_a_cambiar": cliente_a_cambiar 
        
        }
        return flask.render_template("crudcliente.html",**sust)
    


#AÑADIR CLIENTE
@flask_login.login_required
@crudcliente_blprint.route("/añadircliente", methods=["POST"]) 
def añadircliente():
    
    idUser = flask_login.current_user.get_id()
    
    ##DATOS FORMULARIO
    txt_nombre = flask.request.form.get("txtNombre")
    txt_dni = flask.request.form.get("txtDni")
    txt_edad = flask.request.form.get("txtEdad")
   
    validado, mensaje = validar_campos_cliente(txt_nombre,txt_dni,txt_edad,None)
    if not validado:
        
        flask.flash(mensaje)
        sust = {
        "idUser": idUser ,
        "clientes": getClientesMonitor()
        }
        return flask.render_template(('añadircliente.html'),**sust)
        
    else:
        clienteAñadido = Cliente(txt_nombre,txt_dni,txt_edad)
    
        #AÑADO AL ALMACENAMIENTO EL NUEVO USUARIO
        flask_login.current_user.add_cliente_oid(srp.save(clienteAñadido))
        srp.save(flask_login.current_user)
        
        sust = {
        "idUser": idUser ,
        "clientes": getClientesMonitor()
        }
        
        return flask.render_template("crudcliente.html",**sust)

#MODIFICAR CLIENTE
@flask_login.login_required
@crudcliente_blprint.route("/modificarcliente", methods=["POST"]) 
def modificarcliente():
    
    print("Aqui estamos jiji")
    cliente_a_cambiar = request.args.get('cliente_a_cambiar', None)
    
    idUser = flask_login.current_user.get_id()
    oid_clientes = flask_login.current_user.get_oids_clientes()
    clientes = list(srp.multi_load(oid_clientes))
    
    txt_nombre = flask.request.form.get("txtNombre")
    txt_dni = flask.request.form.get("txtDni")
    txt_edad = flask.request.form.get("txtEdad")
    validado, mensaje = validar_campos_cliente(txt_nombre,txt_dni,txt_edad,clientes[int(cliente_a_cambiar)].dni)
    
    if not validado:
        flask.flash(mensaje)
        sust = {
        "idUser": idUser ,
        "clientes": getClientesMonitor() ,
        "objeto_cliente_a_modificar": clientes[int(cliente_a_cambiar)]
        
        }
        
        return flask.render_template('modificarcliente.html', **sust )
    else:
    

        
        clientes[int(cliente_a_cambiar)].nombre = txt_nombre
        clientes[int(cliente_a_cambiar)].dni = txt_dni
        clientes[int(cliente_a_cambiar)].edad = txt_edad
        
        srp.save(clientes[int(cliente_a_cambiar)])
        
        clientesmodificado = list(srp.multi_load(oid_clientes))
        
        sust = {
        "idUser": idUser ,
        "clientes": clientesmodificado ,
        "metodoCrud": None ,
        "cliente_a_cambiar": None 
        
        }
        
        return flask.render_template("crudcliente.html",**sust)
    
    #MODIFICAR CLIENTE

@flask_login.login_required
@crudcliente_blprint.route("/añadirserie", methods=["POST"]) 
def añadirserie():
    
    cliente_a_cambiar = request.args.get('cliente_a_cambiar', None)
    idUser = flask_login.current_user.get_id()
    oid_clientes = flask_login.current_user.get_oids_clientes()
    clientes = list(srp.multi_load(oid_clientes))
    cliente = clientes[int(cliente_a_cambiar)]
    
    
    txtejercicio = flask.request.form.get("txtejercicio")
    txtRepeticiones = flask.request.form.get("txtRepeticiones")
    txtFecha = flask.request.form.get("txtFecha")
    
    validado,mensaje = validar_campos_serie(txtFecha,txtRepeticiones)
    
    if not validado:
        flask.flash(mensaje)
        
        sust = {
        "idUser": idUser ,
        "clientes": getClientesMonitor() ,
        "cliente_a_modificar" : cliente,
        "cliente_a_cambiar" : cliente_a_cambiar,
        "ejercicios": getEjercicios()
        }
        
        return flask.render_template('añadirserie.html', **sust )
    
    
    serie_añadida = Serie(int(txtejercicio),txtRepeticiones,txtFecha)
    serie_oid = srp.save(serie_añadida)
    cliente.add_serie_oid(serie_oid)
    srp.save(cliente)
        
    clientesmodificado = list(srp.multi_load(oid_clientes))
        
    sust = {
    "idUser": idUser ,
    "clientes": clientesmodificado ,
    "cliente_a_cambiar": cliente_a_cambiar ,
    "ejercicios" : getEjercicios()
    
    }
        
    return flask.render_template("añadirserie.html",**sust)
    

def getClientesMonitor():
    oid_clientes = flask_login.current_user.get_oids_clientes()
    clientes = list(srp.multi_load(oid_clientes))
    return clientes

#VALIDA CAMPOS DE CLIENTE
def validar_campos_cliente(nombre,dni,edad,modif_Dniantiguo):
    validado= True
    toret = ""
        
    if not nombre or not dni or not edad:
        validado = False
        toret="Los campos no pueden estar vacios"
    
    elif not validar_dni(dni): 
        validado = False 
        toret="Formato dni incorrecto"
    
    elif not validar_dni_letra(dni):
        validado = False 
        toret="Letra del dni incorrecta"
    elif modif_Dniantiguo == dni:
        pass
    else :
        print("TEPILLE")
        clientesAlmacenados = srp.load_all(Cliente)
        for c in clientesAlmacenados: 
            if c.dni == dni:
                validado = False
                toret = "Ya hay un usuario con ese dni"
                 
    return validado,toret  
    
def validar_dni(dni):
    REGEXP = "[0-9]{8}[A-Z]"
    DIGITO_CONTROL = "TRWAGMYFPDXBNJZSQVHLCKE"
    INVALIDOS = {"00000000T", "00000001R", "99999999R"}
    
    return dni not in INVALIDOS and re.match(REGEXP, dni) is not None 

def validar_dni_letra(dni):
    DIGITO_CONTROL = "TRWAGMYFPDXBNJZSQVHLCKE"
    return DIGITO_CONTROL[int(dni[0:8]) % 23]

#VALIDA CAMPOS DE SERIE 
def validar_campos_serie(txtFecha,txtRepeticiones):
    validado= True
    toret = ""
    
    if not txtFecha or not txtRepeticiones:
        validado = False
        toret="No puede haner campos vacios"
        
    return validado,toret
    

def getEjercicios():
    return list(srp.load_all(Ejercicio))