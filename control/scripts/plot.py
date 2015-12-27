#!/usr/bin/python
# -*- coding: cp1252 -*-

# Autor: Gabriel Maciá
# Fecha: 23/12/2015

# ./plot.py <file1> ... <fileN>
# Procesa los ficheros csv salida de ndump y construye una grafica con sus valores. 
# Uso tipico: ./plot.py routerR1.csv routerR2.csv routerR3.csv borderRouter.csv


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import argparse

parser = argparse.ArgumentParser (description='Plot a graph from a csv nfdump file')
parser.add_argument(dest='fileName', metavar='fileName', action='store', help='file to process', nargs='+')
args = parser.parse_args()

dflist = []
for file in args.fileName: 
    l = open(file).readline()
    if l == 'No matched flows\n':
        print "[-] Fichero vacio: " + file
    else:
        df = pd.read_csv (file, parse_dates={'date': [0]}, header=None, usecols=[0], index_col=[0])
        df[file[:-4]] = 1
        df = df.resample('2Min', how='sum').reset_index()
 #       print df.head()
        dflist.append(df)
        print '[+] Procesado fichero: ' + file

#print "Longitud dflist: " + str(len(dflist))

if len(dflist)>1:
    df_final = reduce(lambda left,right: pd.merge(left,right,on='date',how='outer'), dflist).fillna(0)
     
elif len(dflist) == 1:
    df_final = dflist[0]
else:
    print "No hay datos validos en los ficheros indicados"
    exit()
    
#print df_final.head()
df_final.plot(marker='o')
plt.show()
