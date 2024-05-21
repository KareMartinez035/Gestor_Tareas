from flask import Flask
from app import db
import datetime

#Modelo es para instanciar la app con la bbdd

class Tareas(db.Model): #Declara atributos y métodos de un objeto
    id_Tareas= db.Column(db.Interger,Primary_key=True)
    Nombre= db.Column(db.String(200), nullable=False)
    Fecha_Inicio= db.Column(db.DateTime,default=datetime.utcnow)
    Fecha_final=db.Column(db.DateTime)
    Estado=db.Column(db.String(20,default='Por asignar'))