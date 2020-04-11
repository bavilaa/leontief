# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 18:55:41 2020

@author: Bruno
"""

#reload(sys)
#sys.setdefaultencoding("utf-8")

# 
#   __________
# / ___  ___ \
# / / @ \/ @ \ \
# \ \___/\___/ /\
# \____\/____/||
#   /     /\\\\\//
#  |     |\\\\\\
#  \      \\\\\\
#  \______/\\\\
# _||_||_
# -- --
#Y si ...

#%% Carga de Librerías
import pandas as pd
import sys
import numpy as np
#%%

#Cargando datos numericos de la matriz:
#Parametros fijos
archivo = "2017_MIP_111x111.xlsx" #Hay una formula en celda DY123 en el archivo original debe eliminarse para evitar problemas
year = 2017
#Vector Hojas, pendiente.
hojas = ["1" , "5" , "7" ,  "9" , "11" ,"13", "15" , "17", "19" , "21"]
hoja = "1"
#numero a saltar de lineas
skip = 8
excel = pd.read_excel("mips/" + archivo ,sheet_name=hoja, skiprows=skip)

#%%
#Rename

#excel = excel.rename(columns= {'1': 'Producto'}
#Renombrando la primera columna
#excel.rename( columns={'Unnamed: 1':'Producto'}, inplace=True )
excel = excel.rename( columns={'Unnamed: 1':'Producto',
                              'Unnamed: 116':'Consumo_hogares',
                               'Unnamed: 118':'Consumo_IPSFL',
                               'Unnamed: 120':'Consumo_Gob',
                               'Unnamed: 122':'FBKF',
                               'Unnamed: 124':'Var_Existencias',
                               'Unnamed: 126':'Exportaciones',
                              'Unnamed: 128': 'Produccion_PB'})

#Eliminando Total
excel = excel[excel.Producto!="Total"]
#%%
#Vector de Producción (X)
X = excel[['Produccion_PB']]
#Eliminado nulos
X = X.dropna()
#Resetiando Indice
X = X.reset_index(drop=True)

#%%
#Cargando Coeficientes de de la Matriz Inversa de Leontief
#Cargando datos numericos de la matriz:
#Parametros fijos
archivo = "2017_MIP_111x111.xlsx"
year = 2017
#Vector Hojas, pendiente.
hojas = ["1" , "5" , "7" ,  "9" , "11" ,"13", "15" , "17", "19" , "21"]
hoja = "3"
#numero a saltar de lineas
skip = 6
leontief = pd.read_excel("mips/" + archivo ,sheet_name=hoja, skiprows=skip)
#%%
#Eliminar todas las rilas que sean nan (filas vacías del excel)
leontief = leontief.dropna(how="all")
#Eliminar la primera columna
leontief = leontief.drop(leontief.columns[0], axis=1)
leontief = leontief.drop(leontief.columns[0], axis=1)
#Eliinando la ultima fila con totales de los coeficientes:
leontief.drop(leontief.tail(1).index,inplace=True) # drop last n rows
#Resetiando Index
leontief = leontief.reset_index(drop=True)
#%%
y = excel[['Consumo_hogares' , 'Consumo_IPSFL' , 'Consumo_Gob',
     'FBKF' , 'Var_Existencias' , 'Exportaciones' 
     ]]

y = y.dropna()
#Reetiando Index
y = y.reset_index(drop=True)
#C = Consumo de Hogares
#CIPS = Consumo IPSFL
#G = Consumo gobierno
#I = FBKB
#S = Var Existencias
#EX = Exportaciones
C_p = y[['Consumo_hogares']]
CIPS_p = y[['Consumo_IPSFL']]
G_p = y[['Consumo_Gob']]
I_p = y[['FBKF']]
S_p = y[['Var_Existencias']]
EX_p = y[['Exportaciones']]
#%%
#Consumo Total
y2 = y.copy()
y2['Y'] = y2.sum(axis=1)
y2 = y2[['Y']]
#Se resetea el indice, ya que las columnas de la matriz deben llamarse igual que el vector
y2.index = y2.index + 1

#%%
# Validacion que la multiplicacion de la inversa de Leontief sea la produccion original:
Xval = leontief.dot(y2)
Z = Xval['Y'] - X['Produccion_PB']
Z
#%%
# 2.- Obteniendo VA total en una columna para calcular coeficiente de VA
#%%
VA = excel[excel.Producto=="Valor agregado "]


