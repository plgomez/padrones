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

salida_nodo = open(f'salidas/no_docentes_{hoy}.csv', 'w')

tree = ET.parse('entradas/cargos_no_docentes.xml')
root = tree.getroot()
datos = root[2]

permanentes = []
for cargos in datos.iter('cargos_agente'):
    agente = cargos[1].text
    cuil = cargos[5].text
    dni = cuil[3:-2]
    caracter = cargos[9].text
    cargo = cargos[11].text
    dependencia = cargos[10].text
    dedicacion = cargos[11].text
    if caracter == "PERM":
        ag = {}
        ag['nombre'] = agente
        ag['cuil'] = cuil
        ag['dni'] = dni
        ag['caracter'] = caracter
        ag['dependencia'] = dependencia
        ag['cargo'] = cargo
        ag['dedicacion'] = dedicacion
        permanentes.append(ag)
    

for docente in permanentes:
    fila = (f"{docente['nombre']}  \t  {docente['dni']} \t {docente['cargo']} \t {docente['caracter']} \n")
    salida_nodo.write(fila)    
salida_nodo.close()
