# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from datetime import datetime

l_tree = ET.parse('entradas/legajos_agentes.xml')
l_root = l_tree.getroot()
l_datos = l_root[2]

leg_dni = {}
for legajos in l_datos.iter('legajos'):
    leg_dni[legajos[0].text] = legajos[7].text

hoy = str(datetime.today().date())

salida_tit_fbcb = open(f'salidas/titulares_fbcb_{hoy}.csv', 'w')
salida_tit_ess = open(f'salidas/titulares_ess_{hoy}.csv', 'w')
salida_adj_fbcb = open(f'salidas/adjuntos_fbcb_{hoy}.csv', 'w')
salida_adj_ess = open(f'salidas/adjuntos_ess_{hoy}.csv', 'w')
salida_auxiliares = open(f'salidas/auxiliares_{hoy}.csv', 'w')

TITULARES = ['TIT', 'ASO']
ADJUNTOS = ['ADJ']
AUXILIARES = ['JTP', 'AY1']

titulares_ess = []
titulares_fbcb = []
adjuntos_ess = []
adjuntos_fbcb = []
auxiliares = []
ordinarios = []

tree = ET.parse('entradas/cargos_docentes.xml')
root = tree.getroot()
datos = root[2]

for cargos in datos.iter('cargos_agente'):
    agente = cargos[1].text
    cuil = cargos[5].text
    dni = cuil[3:-2]
    caracter = cargos[9].text
    cargo = cargos[11].text[:-1]
    dependencia = cargos[10].text
    dedicacion = cargos[11].text[-1:]
    if caracter == "ORDI":
        ag = {}
        ag['nombre'] = agente
        ag['cuil'] = cuil
        ag['dni'] = dni
        ag['caracter'] = caracter
        ag['dependencia'] = dependencia
        ag['cargo'] = cargo
        ag['dedicacion'] = dedicacion
        ordinarios.append(ag)
    

for docente in ordinarios:
    if docente['cargo'] in TITULARES:
        dni = docente['dni']
        if docente['dependencia'] == "317":
            titulares_ess.append(dni)
            fila = (f"{docente['nombre']}  \t  {docente['dni']} \t {docente['cargo']} \t {docente['dependencia']} \n")
            salida_tit_ess.write(fila)    

        if docente['dependencia'] == "309":
            titulares_ess.append(dni)
            fila = (f"{docente['nombre']}  \t  {docente['dni']} \t {docente['cargo']} \t {docente['dependencia']} \n")
            salida_tit_fbcb.write(fila)    

for docente in ordinarios:
    dni = docente['dni']
    if docente['cargo'] in ADJUNTOS and (dni not in titulares_ess) and (dni not in titulares_fbcb):
        if docente['dependencia'] == "317":
            adjuntos_ess.append(dni)
            fila = (f"{docente['nombre']}  \t  {docente['dni']} \t {docente['cargo']} \t {docente['dependencia']} \n")
            salida_adj_ess.write(fila)    
        if docente['dependencia'] == "309":
            adjuntos_fbcb.append(dni)
            fila = (f"{docente['nombre']}  \t  {docente['dni']} \t {docente['cargo']} \t {docente['dependencia']} \n")
            salida_adj_fbcb.write(fila)    

for docente in ordinarios:
    dni = docente['dni']
    if docente['cargo'] in AUXILIARES and dni not in adjuntos_ess and dni not in adjuntos_fbcb and dni not in titulares_ess and dni not in titulares_fbcb and dni not in auxiliares:
        auxiliares.append(docente['dni'])
        fila = (f"{docente['nombre']}  \t  {docente['dni']} \t {docente['cargo']} \t {docente['dependencia']} \n")
        salida_auxiliares.write(fila)    

salida_tit_fbcb.close()
salida_tit_ess.close()
salida_adj_fbcb.close()
salida_adj_ess.close()
salida_auxiliares.close()
