from flask import Flask, render_template, request, redirect, url_for
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
            if request.form['Codigo'] == '00000' and request.form['Password'] == '12345600':
                print('Login correcto')
                return redirect(url_for('AnalisisAdmin'))
            elif len(request.form['Codigo']) == 6:
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
    notas_estudiantes = db.notas_estudiantes()[0]
    numero = db.notas_estudiantes()[1]
    print(numero)
    return render_template('Seguimiento.html', notas=notas_estudiantes, data=dato, numero=numero)

@app.route('/Seguimiento/eliminar/{{ elemento.id }}')
def eliminar_elemento(elemento_id):
    hola = analisis.eliminar(elemento_id)
    return redirect('/')


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

@app.route('/AnalisisAdmin')
def AnalisisAdmin():
    sis = analisis.grafica_admin()
    return render_template('AnalisisAdmin.html', analisis=sis)


@app.route('/ayuda')
def ayuda():
    dato = data
    return render_template('ayuda.html', data=dato)


if __name__ == '__main__':
    app.run(debug=True)
