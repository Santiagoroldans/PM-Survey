from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
import plotly.graph_objects as go

url = "https://olumfqjodbfaoauorecf.supabase.co/"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9sdW1mcWpvZGJmYW9hdW9yZWNmIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTY5NTIzNTYsImV4cCI6MjAxMjUyODM1Nn0.G_RihDE6_I2yJ0u6KdILqV-OE5601kGDx7OFtU5gpsA"

supabase = create_client(url, key)


def Areas_Academicas(codigo):
    response = supabase.table('notas_general').select('*').eq('Codigo', codigo).execute()
    data_json = response.data[0]
    return data_json


def user(Codigo):
    Code = Codigo
    if len(Code) == 6:
        response = supabase.table('estudiantes').select('*').eq('Codigo', Code).execute()
        try:
            data_json = response.data[0]
            return data_json
        except IndexError:
            return 'Error'
    elif len(Code) == 4:
        response = supabase.table('docentes').select('*').eq('Codigo', Code).execute()
        try:
            data_json = response.data[0]
            return data_json
        except IndexError:
            return 'Error'


def notas_estudiantes():
    url = "https://olumfqjodbfaoauorecf.supabase.co/"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9sdW1mcWpvZGJmYW9hdW9yZWNmIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTY5NTIzNTYsImV4cCI6MjAxMjUyODM1Nn0.G_RihDE6_I2yJ0u6KdILqV-OE5601kGDx7OFtU5gpsA"

    supabase = create_client(url, key)
    response = supabase.table('notas_individuales').select('*').execute()
    data_json = response.data
    notas_estudiantes = {}

    for estudiante in data_json:
        nombre_estudiante = estudiante['Nombre']
        notas_estudiante = [estudiante[key] for key in estudiante.keys() if key.startswith('Nota')]
        notas_estudiantes[nombre_estudiante] = notas_estudiante

    return notas_estudiantes

