from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature
from flask_mail import Mail,Message


app =Flask(__name__)

#Configutar la conexión a la base de datos
app.config['SECRET_KEY']='123456789'
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
db= mysql.connector.connect(
    host="localhost",
    user= "root",
    password= "",
    database= "gestor_tareas"
)

#Crear un objeto y llamar una función para la bd
cursor=db.cursor()
app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='masilka.km@gmail.com'
app.config['MAIL_PASSWORD']='fevd bmtt ddxv vjdb'
app.config['MAIL_USE_TLS']=False #Este funciona para bloquear los posibles ataques
app.config['MAIL_USE_SSL']=True #Este funciona de igual manera, el cual permite el envio del correo
app.config['MAIL_DEFAULT_SENDER']=('Karen', 'masilka.km@gmail.com')
mail=Mail(app)

#FUNCION PARA ENVIAR CORREO
def enviar_correo(email):
    #se genera un token para el correo proporcionado
    token= serializer.dumps(email, salt='Restablecer_contraseña')   #LOS TOKEN SON ÚNICOS #SE IMPORTAN MÁS LIBRERIAS
    
    #SE CREA LA URL 
    enlace=url_for('restablecer_contraseña',token=token, _external=True) 
    
    #SE CREA EL MENSAJE QUE LLEVARA EL CORREO
    mensaje= Message(subject='Restablecimiento de contraseña',recipients=[email],body=f'Para restablecer contraseña, click en el siguiente enlace: {enlace}')# En este caso se envia el correo con el enlace para restablecer la contraseña

    mail.send(mensaje)

        

#FUNCION PARA RESTABLECER LA CONTRASEÑA
@app.route('/restablecer_contraseña/<token>',methods=['GET', 'POST'])
def restablecer_contraseña(token):
   

     if request.method=='POST':
        Nueva_Contraseña=request.form['Nueva_Contraseña']
        confirmar_contraseña=request.form['confirmar_contraseña']
        print(Nueva_Contraseña)
        print(confirmar_contraseña)

        #verificar que las contraseñas sean iguales
        if Nueva_Contraseña != confirmar_contraseña:
          return print('Las contraseñas no coinciden')
        #VERIFICAR CORREO DEL TOKEN
        
        passwordnuevo=generate_password_hash(Nueva_Contraseña)

        #Actualizar en la base de datos
        cursor=db.cursor()
        email= serializer.loads(token,salt='Restablecer_contraseña', max_age=3600)
        consulta="UPDATE usuarios SET Contrasena_Usuario =%s WHERE Email_usuario =%s"
        cursor.execute(consulta,(passwordnuevo,email))
        db.commit()
        print(consulta)
        return redirect(url_for('login'))


     return render_template('restablecer_contraseña.html')

#RECUPERAR CONTRASEÑA
@app.route('/recuperar_contraseña',methods=['GET', 'POST'])
def recuperar_contraseña():
    if request.method=='POST':
    
        email=request.form.get('email')
        enviar_correo(email)

        return redirect(url_for('login'))
    
    return render_template('recuperar_contraseña.html')

########################## INICIO DE SESSION ###################################
# Verificar credenciales según el rol
@app.route('/',methods=['GET', 'POST'])
def login():
    Usuario=request.form.get('Usuario_name')
    Contrasena=request.form.get('Contrasena_Usuario')

    cursor=db.cursor(dictionary=True)
    query = "SELECT Nombre_usuario,Apellidos_usuario, Genero, Usuario_name,Contrasena_Usuario,Rol FROM usuarios WHERE Usuario_name = %s "
    cursor.execute(query,(Usuario,))
    usuarios=cursor.fetchone()

    if(usuarios and check_password_hash(usuarios['Contrasena_Usuario'],Contrasena)):
        # Crear Sesion
        session['Usuario']=usuarios['Usuario_name']
        session['Nombre']=usuarios['Nombre_usuario']
        session['Apellido']=usuarios['Apellidos_usuario']
        session['Rol']=usuarios['Rol']
        session['Genero']=usuarios['Genero']

        if usuarios['Rol'] == 'Administrador':
            return render_template('Principalad.html', Genero=usuarios['Genero'], nombre_usuario=usuarios['Nombre_usuario'], apellido_usuario=usuarios['Apellidos_usuario'], Rol=usuarios['Rol'])
        else:
            return render_template('Principalusu.html', Genero=usuarios['Genero'], nombre_usuario=usuarios['Nombre_usuario'], apellido_usuario = usuarios['Apellidos_usuario'], Rol=usuarios['Rol'])    
    else:
        print("Credenciales invalidas, Intenta nuevamente")
    return render_template('index.html')
    
#Crear ruta para salir
@app.route('/salir')
def salir():
    session.pop('Usuario', None)
    return redirect(url_for('login'))

#No almacenar el  cache de le pagina
@app.after_request
def add_header(response):
    response.headers['Cache-Control']='no-cache,no-store,must-revalidate, max-age=0'
    response.headers['Pragma']='no-cache'
    response.headers['Expires']=0
    return response

#Crear ruta
@app.route('/RegistroUsuario', methods=['GET', 'POST'])
def RegistroUsuario():
    if request.method== 'POST':
        NombreUsuario=request.form.get('Nombre_usuario')
        ApellidoUsuario=request.form.get('Apellidos_usuario')
        Genero=request.form.get('Genero')
        EmailUsuario=request.form.get('Email_usuario')
        Usuario=request.form.get('Usuario_name')
        ContrasenaUsuario=request.form.get('Contraseña_Usuario')
        RolUsuario=request.form.get('Rol')
        cencriptar=generate_password_hash(ContrasenaUsuario)

        #verificar usuario y email
        cursor=db.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE Usuario_name= %s OR Email_usuario= %s", (Usuario,EmailUsuario))
        resultado=cursor.fetchone()
        if resultado:
            print("Correo o Usuario ya registrado")
            render_template('RegistroUsuario.html')

        #insertar los usuarios a laa bd
        else:
            cursor.execute("INSERT INTO usuarios (Nombre_usuario, Apellidos_usuario, Genero, Email_usuario, Usuario_name, Contrasena_Usuario, Rol) VALUES(%s,%s,%s,%s,%s,%s,%s)",(NombreUsuario,ApellidoUsuario,Genero,EmailUsuario,Usuario,cencriptar,RolUsuario))
            db.commit()
            print("Registro de usuario Exitoso")
            return redirect(url_for('RegistroUsuario'))
        
    return render_template('RegistroUsuario.html')


# Visualizar todos los usuarios
@app.route('/MostrarUsuario', methods=['GET','POST'])
def MostrarUsuario():
    cursor=db.cursor()
    cursor.execute("SELECT Id_Usuarios, Nombre_usuario, Apellidos_usuario, Genero, Email_usuario, Usuario_name, Rol FROM usuarios")
    usuario=cursor.fetchall()

    return render_template('Principalad.html', usuarios=usuario, mostrar_usuarios=True, mostrar_bienvenida = True)

@app.route('/eliminar_usuario/<int:Id_Usuarios>',methods=['GET'])
def eliminar_usuario(Id_Usuarios):
    cursor=db.cursor()
    cursor.execute('DELETE FROM usuarios WHERE Id_Usuarios= %s',(Id_Usuarios,))
    db.commit()
    print("Usuario eliminado")
    return redirect(url_for('MostrarUsuario'))


@app.route('/editar_usuario/<int:Id_Usuarios>',methods=['GET','POST'])
def editar_usuario(Id_Usuarios):

    if request.method=='POST':
        nombreUsu=request.form['Nombre_Usuario']
        apelliUsu=request.form['Apellido_Usuario']
        GeneroUsu=request.form['Genero']
        emailUsu=request.form['email']
        nicknameUsu=request.form['Usuario_name']

    # Actualizar los datos del formulario

        cursor=db.cursor()
        sql='UPDATE usuarios SET Nombre_usuario= %s, Apellidos_usuario=%s, Genero=%s, Email_usuario=%s, Usuario_name=%s WHERE Id_Usuarios= %s'
        cursor.execute(sql,(nombreUsu,apelliUsu,GeneroUsu,emailUsu,nicknameUsu, Id_Usuarios))
        db.commit()
        print("Usuario actualizado")
        return redirect(url_for('MostrarUsuario'))

    else:
        cursor=db.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id_Usuarios=%s",(Id_Usuarios,))
        data=cursor.fetchall()
        cursor.close()
    
        return render_template('Modalusu.html',usuario=data[0])


##################### Todo relacionado a las tareas #####################

#Creación de rutas
@app.route('/RegistroTareas', methods=['GET','POST']) #SE DECLARAN LOS MÉTODOS
#función de registrar tareas
def RegistrarTareas():
#Consulta para obtener el id del usuario a traves del nombre del usuario
    
    if request.method=='POST':
        #Variables donde se llama los campos del formulario

        NombreTarea=request.form.get('Nombre')
        FechaInicio=request.form.get('Fecha_Inicio')
        FechaFinal=request.form.get('Fecha_final')
        EstadoTar=request.form.get('Estado')
        nickname= request.form.get('usuario')
        
       
        cursor=db.cursor()
        #verificar que el nombre de la tarea no esta registrado
        cursor.execute('SELECT * FROM tareas WHERE Nombre = %s',(NombreTarea,))
        Existe=cursor.fetchall()

        if Existe:
            print("Nombre de la tarea ya se encuentra registrado")
            return render_template('RegistroTareas.html')
        

    #Insertar las tareas a la tabla de tareas
        cursor.execute("INSERT INTO tareas(Nombre, Fecha_Inicio, Fecha_final,Estado,usuario) VALUES(%s,%s,%s,%s,%s)",(NombreTarea,FechaInicio,FechaFinal,EstadoTar,nickname))
        db.commit()

        print("Tarea registrada")
    return render_template('RegistroTareas.html', Rol=session['Rol'])


#Mostrar Todas las tareas registradas desde Administrador

@app.route('/buscar_tarea', methods=['POST'])
def buscar_tarea():
    busqueda=request.form.get('busqueda')

    cursor=db.cursor(dictionary=True)
    consulta="SELECT * FROM tareas WHERE id_Tareas= %s OR Nombre LIKE %s"
    cursor.execute(consulta,(busqueda, "%" + busqueda +"%"))
    tareas=cursor.fetchall()

    return render_template('Resultado_tarea.html', tareas=tareas, busqueda=busqueda)

@app.route('/MostrarTareas', methods=['GET','POST'])
def MostrarTareas():
    cursor=db.cursor()
    if session['Rol']=='Administrador':
        cursor.execute("SELECT * FROM tareas")
        tarea=cursor.fetchall()
        return render_template('Principalad.html', tareas=tarea, Rol=session['Rol'], mostrar_tareasAd=True, mostrar_bienvenida = True)
    else:
        cursor.execute("SELECT * FROM tareas WHERE usuario = %s",(session['Usuario'],))
        tarea=cursor.fetchall()
        return render_template('Principalusu.html', tareas=tarea, Rol=session['Rol'], mostrar_tareasAd=True, mostrar_bienvenida = True)

@app.route('/eliminar_tarea/<int:id_Tareas>',methods=['GET'])
def eliminar_tarea(id_Tareas):
    cursor=db.cursor()
    cursor.execute('DELETE FROM tareas WHERE id_Tareas= %s',(id_Tareas,))
    db.commit()
    print("Tarea eliminada")
    return redirect(url_for('MostrarTareas'))

@app.route('/editar_tarea/<int:id_Tareas>',methods=['GET' , 'POST'])
def editar_tarea(id_Tareas):
    
    if request.method=='POST':
        #codigotar=request.form['codigo']
        nombretar=request.form['nombreTar']
        fechini=request.form['finicio']
        fechter=request.form['ffinal']
        estadotar=request.form['estadotar']

    # Actualizar los datos del formulario
        cursor=db.cursor()
        sql="UPDATE tareas SET Nombre= %s, Fecha_Inicio=%s, Fecha_final=%s, Estado=%s WHERE id_Tareas=%s"
        cursor.execute(sql,(nombretar,fechini,fechter,estadotar, id_Tareas))
        print("Tarea Actualizada")
        db.commit()
        return redirect(url_for('MostrarTareas'))

    else:
        cursor=db.cursor()
        cursor.execute("SELECT * FROM tareas WHERE id_Tareas=%s",(id_Tareas,))
        data=cursor.fetchall()
        cursor.close()
    
        return render_template('Modaltareas.html',tareas=data[0])


if __name__=='__main__': #INVESTIGAR
    app.run(debug=True)
    app.add_url_rule('/',view_func=login)