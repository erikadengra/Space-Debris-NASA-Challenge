# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 22:47:04 2024

@author: PepRubi
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import poisson
import chardet

# Cargar el archivo CSV
#file_path = 'alltime_data.csv'
file_path = 'today_data.csv'

data_2 = pd.read_csv(file_path)

data = data_2[(9000 < data_2['SEMIAXIS']) & (data_2['SEMIAXIS']< 80000)]
# Función de Poisson para el ajuste
def poisson_func(x, lamb):
    return poisson.pmf(np.floor(x), lamb)

# Función gaussiana para hacer el ajuste
def gaussian(x, mu, sigma):
    return (1/(sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma)**2)

# Función para crear el histograma y ajustar la curva de Poisson
def hist_and_fit_poisson(column_data, column_name, lambda_1):
    # Crear el histograma
    hist_values, bin_edges = np.histogram(column_data.dropna(), bins=30)  # Frecuencia en y
     
    # Graficar el histograma
    plt.figure(figsize=(8, 6))
    plt.hist(column_data.dropna(), bins=30, density = True, alpha=0.6, color='lightblue', label=f'Histograma de {column_name}', edgecolor='black')
    
    # Generar puntos para la curva ajustada
    x_fit = np.linspace(min(column_data), max(column_data), 100)
    y_fit = poisson_func(x_fit, lambda_1) # Escalar a la suma del histograma
    # Graficar la curva ajustada
    plt.plot(x_fit, y_fit, color='red', label='Ajuste Poisson')
    plt.xlabel(column_name)
    plt.ylabel('Cantidad de Datos')
    plt.title(f'Ajuste Poisson al Histograma de {column_name}')
    plt.legend()
    plt.show()

# Función para crear el histograma y ajustar la curva gaussiana
def hist_and_fit_gaussian(column_data, column_name, mu, sigma):
    # Crear el histograma
    hist_values, bin_edges = np.histogram(column_data.dropna(), bins=30)  # Frecuencia en y    
    
    # Ajustar la curva gaussiana    
    # Graficar el histograma
    plt.figure(figsize=(8, 6))
    plt.hist(column_data.dropna(), bins=40, density = True, alpha=0.6, color='lightblue', label=f'Histograma de {column_name}', edgecolor='black')
    
    # Generar puntos para la curva ajustada
    x_fit = np.linspace(min(column_data), max(column_data), 100)
    y_fit = gaussian(x_fit, mu, sigma)
    # Graficar la curva ajustada
    plt.plot(x_fit, y_fit, color='red', label='Ajuste Gaussiano')
    plt.xlabel(column_name)
    plt.ylabel('Cantidad de Datos')
    plt.title(f'Ajuste Gaussiano al Histograma de {column_name}')
    plt.legend()
    plt.show()
#hist_and_fit_gaussian(data['SEMIAXIS'], 'Semieje Mayor', 7100, 200)
hist_and_fit_gaussian(data['SEMIAXIS'], 'Semieje Mayor', 7100, 200)
hist_and_fit_gaussian(data['ECCENTRICITY'], 'Excentricidad', 0, 0.008)
hist_and_fit_gaussian(data['INCLINATION'], 'Inclinación', 100, 1)
hist_and_fit_gaussian(data['INCLINATION'], 'Inclinación', 70, 15)

def double_gaussian(prob_1, num_tot):
    gaussiana_b = []
    for i in range(num_tot):
        a = np.random.uniform(0,1)
        if a < prob_1*2.5:
            b = np.random.normal(100,1)
        else:
            b = np.random.normal(70,15)
        gaussiana_b.append(b)
    return gaussiana_b

gaussiana_B = double_gaussian(0.08, 30000)
plt.hist(gaussiana_B, bins = 40, density = True, alpha=0.6, color='lightblue', label='Histograma de', edgecolor='black')

num_sat = 56000
obj_name = []
a = []
for j in range(num_sat):
    obj_name.append(str(j))
    a.append(0)

prob1 = 0.1
semiaxis_1 = np.random.normal(7100,200, int(num_sat*(1-prob1)))
semiaxis_2 = np.random.normal(35000, 1000, int(num_sat*prob1))
eccentricity = np.random.normal(0, 0.008, num_sat)
inclination_1 = np.random.normal(70, 15, int(num_sat*(1-prob1)))
inclination_2 = np.random.normal(100,1,int(num_sat*prob1))
lan = np.random.uniform(0,360, num_sat)
inclination = np.concatenate((inclination_1, inclination_2))
semiaxis = np.concatenate((semiaxis_1, semiaxis_2))

df = pd.DataFrame({
    'Semiaxis': semiaxis*0.00313577924,
    'Eccentricity': eccentricity,
    'inclinacion': inclination,
    'LAN': lan,  # Longitud del nodo ascendente
    'Argument of Perigee': a
})

df.to_csv('Orbital_parameters.csv', columns = ['Semiaxis', 'Eccentricity', 'inclinacion','LAN','Argument of Perigee'])

# Aplicar el ajuste de Poisson a las dos primeras columnas (SEMIAXIS y ECCENTRICITY)
#hist_and_fit_poisson(data['SEMIAXIS'], 'Semieje Mayor')
#hist_and_fit_gaussian(data['ECCENTRICITY'], 'Excentricidad')

# Aplicar el ajuste gaussiano a la tercera columna (INCLINATION)
#hist_and_fit_gaussian(data['INCLINATION'], 'Inclinación')
