#!/usr/bin/python
# -*- coding: cp1252 -*-

# Autor: Gabriel MaciÃ¡
# Fecha: 23/12/2015

# ./plot.py <file1> ... <fileN>
# Procesa los ficheros csv salida de ndump y construye una grafica con sus valores. 
# Uso tipico: ./plot.py routerR1.csv routerR2.csv routerR3.csv borderRouter.csv


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import argparse
import os

parser = argparse.ArgumentParser (description='Plot a graph from a csv nfdump file')
parser.add_argument(dest='fileName', metavar='fileName', action='store', help='file to process', nargs='+')
args = parser.parse_args()

dflist = []
for file in args.fileName: 
    l = open(file).readline()
    if l == 'No matched flows\n' or os.path.getsize(file)== 0:
        print "[-] Fichero vacio: " + file
    else:
        print '[+] Procesando fichero: ' + file
        # Leemos el fichero .csv, poniendo como indice la columna con la fecha para poder después hacer el 
        # resampling con el metodo resample. 
        df = pd.read_csv (file, parse_dates={'date': [0]}, header=None, usecols=[0], index_col=[0])
        df[file[:-4]] = 1
        # Para poder hacer resample, df debe tener como indice las fechas. Después de hacerlo reseteamos el indice
        # para poder llamar posteriormente a merge con la columna date. 
        df = df.resample('1Min', how='sum').reset_index()
 #       print df.head()
        dflist.append(df)
        print 'Ok'

# Dependiendo del numero de ficheros procesados, hacemos un merge de todos o no. Al final es importante
# volver a colocar el indice con la columna date, para que la gráfica muestre las fechas. 

if len(dflist)>1:
    # Agrupamos los dataframe de todos los ficheros, rellenando con 0s los NaN y poniendo al final
    # el indice a la columna date para que aparezca en la grafica en el eje x. 
    df_final = reduce(lambda left,right: pd.merge(left,right,on='date',how='outer'), dflist).fillna(0).set_index('date')
     
elif len(dflist) == 1:
    df_final = dflist[0].set_index('date')
else:
    print "No hay datos validos en los ficheros indicados"
    exit()
    
print df_final
df_final.plot(marker='o')
plt.show()
