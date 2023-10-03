# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import base64
from datetime import datetime
"""Seleccionar INCD en variantes en el filtro de licencia por agente ver imagen en la doc"""

hoy = str(datetime.today().date())


tree = ET.parse('entradas/licencias.xml')
root = tree.getroot()
datos = root
licencias = []
for dep in datos.iter('dep'):
    for licencia in datos.iter('licencia'):
        cargo_lic = licencia[6].text
        licencias.append(cargo_lic)

l_tree = ET.parse('entradas/legajos_agentes.xml')
l_root = l_tree.getroot()
l_datos = l_root[2]

leg_dni = {}

for legajos in l_datos.iter('legajos'):
    leg_dni[legajos[0].text] = legajos[7].text


tree = ET.parse('entradas/cargos_docentes.xml')
root = tree.getroot()
datos = root[2]
salida = open(f'salidas/cargos_docentes_{hoy}.csv', 'w')

for cargos in datos.iter('cargos_agente'):
    en_licencia = ""
    if cargos[17].text in licencias:
        en_licencia = "Licencia por incompatibilidad"
        #print cargos[17].text

    agente = cargos[1].text.split(",")
    agente_nombre = f"{agente[1].title()} {agente[0]} - (DNI Nº  {cargos[5].text[3:-2]})".strip()
    print(agente_nombre)
    cuil = cargos[5].text
    cargo = cargos[11].text[:-1]
    if cargo == "AY1": cargo = "Ayudante de Cátedra"
    if cargo == "AY2": cargo = "Ayudante Alumno"
    if cargo == "JTP": cargo = "Jefe de Trabajos Prácticos"
    if cargo == "ADJ": cargo = "Profesor Adjunto"
    if cargo == "ASO": cargo = "Profesor Asociado"
    if cargo == "TIT": cargo = "Profesor Titular"
    dedicacion = cargos[11].text[-1:]
    if dedicacion == "1" : dedicacion = "Simple"
    if dedicacion == "S" : dedicacion = "Semiexclusiva"
    if dedicacion == "E" : dedicacion = "Exclusiva"
    if dedicacion == "B" : dedicacion = "Exclusiva B"
    if dedicacion == "A" : dedicacion = "Exclusiva A"
    if dedicacion == "C" : dedicacion = "Exclusiva C"
    if dedicacion == "N" : dedicacion = cargos[14].text+" Horas"
    caracter = cargos[9].text
    dependencia = cargos[10].text
    if caracter != "BECA":
        #la segunda forma serpara en tres columnas el apellido nombre y dni, la primera va todo junto
        fila = f"{agente_nombre} \t {cuil} \t  {cargo} \t {dedicacion}   \t  {caracter}  \t  {en_licencia}  \t {dependencia} \n"
        #fila = f"{agente[0]} \t {agente[1]} \t {cargos[5].text[3:-2]} \t {cuil} \t  {cargo} \t {dedicacion}   \t  {caracter}  \t  {en_licencia}  \t {dependencia} \n"
        salida.write(fila)    
salida.close()
