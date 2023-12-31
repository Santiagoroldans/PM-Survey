import plotly.graph_objects as go
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
import plotly.express as px
import pandas as pd

url = "https://olumfqjodbfaoauorecf.supabase.co/"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9sdW1mcWpvZGJmYW9hdW9yZWNmIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTY5NTIzNTYsImV4cCI6MjAxMjUyODM1Nn0.G_RihDE6_I2yJ0u6KdILqV-OE5601kGDx7OFtU5gpsA"
supabase = create_client(url, key)


def grafica(codigito):
    codigo = codigito

    response = supabase.table('notas_general').select('Matematicas', 'Fisica', 'Etica', 'Ingles', 'Filosofia',
                                                      'Codigo').eq('Codigo', codigo).execute()
    data_json = response.data[0]

    notas_del_estudiante = []

    for k in data_json:
        notas_del_estudiante.append(data_json[k])

    notas_del_estudiante.remove(codigo)

    df = pd.DataFrame(dict(
        Nota=notas_del_estudiante,
        Materia=['Matematicas', 'Fisica', 'Etica', 'Ingles', 'Filosofia']))

    fig = px.line_polar(df, r='Nota', theta='Materia', line_close=True)

    return fig.to_html(full_html=False)


def prom(Codigo):
    codigo = Codigo
    response = supabase.table('notas_general').select('Matematicas', 'Fisica', 'Etica', 'Ingles', 'Filosofia',
                                                      'Codigo').eq('Codigo',
                                                                   codigo).execute()
    data_json = response.data[0]

    notas_del_estudiante = []

    for k in data_json:
        notas_del_estudiante.append(data_json[k])

    notas_del_estudiante.remove(codigo)

    promedio = (sum(notas_del_estudiante)) / (len(notas_del_estudiante))
    nota_nueva = 3 * (len(notas_del_estudiante) + 1) - sum(notas_del_estudiante)

    if promedio < 3:
        msg = "Vas perdiendo, tonto"
        if nota_nueva > 5:
            print(msg)
            print("Tienes que sacarte mas de un 5 jaja")
        else:
            print(msg)
            print("Tienes que sacarte", nota_nueva)
    elif promedio >= 3:
        msg = "Vas ganando, tonto"
        print(msg)

    return round(promedio, 2)


def graficas_docente(Nota):
    notas_individuales = supabase.table('notas_individuales').select(Nota, 'Nombre').execute()

    x = list(notas_individuales)

    tabla = pd.DataFrame(x[0][1])
    g = 0
    p = 0
    for i in tabla[Nota]:
        if i < 3:
            p = p + 1
        elif i >= 3:
            g = g + 1
    labels = ['Ganadores', 'Perdedores']
    values = [g, p]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3, marker_colors=['#44EB6D', '#EB4452'])])

    return fig.to_html()


def grafica_admin():
    response = supabase.table('notas_general').select('Matematicas', 'Fisica', 'Etica', 'Ingles', 'Filosofia').execute()
    tabla = list(response)
    u = tabla[0][1]

    p = 0
    g = len(u)
    for i in u:
        for j in i:
            if i[j] < 3:
                p += 1
                break
    g -= p
    fig = go.Figure([go.Bar(x=['Ganando', 'Perdiendo'], y=[g, p], marker_color=['#44EB6D', '#EB4452'])])

    return fig.to_html()


def eliminar(id):
    supabase.table('items').delete().eq('id', id).execute()
    return True