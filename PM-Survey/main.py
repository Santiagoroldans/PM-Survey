from flask import Flask, render_template, request, redirect, url_for, flash
from db import db, analisis

app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        global data
        data = db.user(request.form['Codigo'])
        if data == 'Error':
            return redirect(url_for('login'))
        else:
            if len(request.form['Codigo']) == 6:
                if request.form['Codigo'] == str(data['Codigo']) and request.form['Password'] == str(data['Password']):
                    print('Login correcto')
                    return redirect(url_for('home'))
                else:
                    return redirect(url_for('login'))
            elif len(request.form['Codigo']) == 4:
                if request.form['Codigo'] == str(data['Codigo']) and request.form['Password'] == str(data['Password']):
                    print('Login correcto')
                    return redirect(url_for('Docente'))
                else:
                    return redirect(url_for('login'))
            else:
                return redirect(url_for('login'))
    else:
        return render_template('login.html')


@app.route('/Seguimiento')
def Seguimiento():
    dato = data
    notas_estudiantes = db.notas_estudiantes()
    return render_template('Seguimiento.html', notas=notas_estudiantes, data=dato)


@app.route('/Analisis')
def Analisis():
    grafica1 = analisis.graficas_docente('Nota')
    grafica2 = analisis.graficas_docente('Nota_2')
    grafica3 = analisis.graficas_docente('Nota_3')
    return render_template('Analisis.html', grafica1=grafica1, grafica2=grafica2, grafica3=grafica3)


@app.route('/Docente')
def Docente():
    dato = data
    return render_template('Docente.html', data=dato)


@app.route('/home')
def home():
    dato = data
    return render_template('home.html', data=dato)


@app.route('/Areas_Academicas')
def Areas_Academicas():
    dato = db.Areas_Academicas(data['Codigo'])
    return render_template('Areas_Academicas.html', data=dato)


@app.route('/Analisis_Escolar')
def Analisis_Escolar():
    dato = data
    codigo = dato['Codigo']
    grafica = analisis.grafica(codigo)
    promedio = analisis.prom(codigo)
    return render_template('Analisis_Escolar.html', grafica=grafica, promedio=promedio)


@app.route('/ayuda')
def ayuda():
    dato = data
    return render_template('ayuda.html', data=dato)


if __name__ == '__main__':
    app.run(debug=True)
