"""Univercidad interamericana de Panama
Sistemas de encuestas

Proyecto Final de Programacion de Computadoras 4

Integrantes:

Omar Gonzalez
Franklin Vanegas
Vladimir Batista
Grimaldo Castro

"""

from flask import Flask, flash, url_for, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

"""Creacion de base de datos"""

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///encuestas.sqlite3'
app.config['SECRET_KEY'] = 'uippc3'

db = SQLAlchemy(app)

"""Creacion de tabla en base de datos"""

class encuesta(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    pregunta = db.Column(db.String(100))
    opcion1 = db.Column(db.String(50))
    opcion2 = db.Column(db.String(50))
    voto1 = db.Column(db.Integer)
    voto2 = db.Column(db.Integer)
    cantidad = db.Column(db.Integer)

    """" Creacion de valores """

    def __init__(self, pregunta, opcion1, opcion2, voto1,voto2,cantidad):
        self.pregunta = pregunta
        self.opcion1 = opcion1
        self.opcion2 = opcion2
        self.voto1 = voto1
        self.voto2 = voto2
        self.cantidad = cantidad

"""Llamado de pagina principal"""
@app.route('/')
def principal():
    print(encuesta.query.all())
    return render_template('principal.html', encuesta=encuesta.query.all())

"""Llamado de pagina nueva encuesta
   Modulo de nueva encuesta"""
@app.route('/nueva_encuesta/', methods=['GET','POST'])
def nueva_encuesta():
    if request.method == 'POST':
        if not request.form['pregunta']:
            flash('Por favor debe introducir una pregunta', 'error')

        elif  not request.form['opcion1'] or not request.form['opcion2']:
            flash('Debes colocar dos opciones,Error')


        elif not request.form['opcion2']:
            flash('Debe introducir la opcion 2!')

        else:
            voto1 = 0
            voto2 = 0
            cantidad = 0
            data_ = encuesta(request.form['pregunta'],request.form['opcion1'],request.form['opcion2'],voto1,voto2,cantidad)
            db.session.add(data_)
            db.session.commit()
            flash('Se crea encuesta exitosamente!')
            return redirect(url_for('principal'))



    return render_template('nueva_encuesta.html')

"""Llamado de pagina votacion"""
@app.route('/votar/', methods = ['GET','POST'])
def votar():
    if request.method == 'POST':
        opc = request.form['id']
        print(opc)
        u = encuesta.query.get(opc)
        print(u)
        return render_template('votacion.html',u=encuesta.query.get(opc))

"""Modulo de contador de las encuestas"""
@app.route('/conteo/',methods = ['GET','POST'])
def conteo():
    if request.method == 'POST':
        opc = request.form['opc']
        #
        id = request.form['id']
        u = encuesta.query.get(id)
        print(u)
        if opc == 'a':
            flag = int(u.voto1)
            flag = flag + 1
            u.voto1 = flag
            cant = int(u.cantidad)
            cant = cant + 1
            u.cantidad = cant
            db.session.commit()

        else:
            flag = int(u.voto2)
            flag = flag + 1
            u.voto2 = flag
            cant = int(u.cantidad)
            cant = cant + 1
            u.cantidad = cant
            db.session.commit()

    return redirect(url_for('principal'))



"""Inicio de programa"""

if __name__=='__main__':
    app.run()
    db.create_all()



