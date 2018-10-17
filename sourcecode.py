# Importing packages
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from bokeh.io import curdoc, output_file, show
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from numpy.random import random
from sklearn.linear_model import LinearRegression


# IMPORTING

pop_df=pd.read_csv('popboiiii.csv', index_col=0, encoding = 'latin1')
gdp_df=pd.read_csv('gdpboiii.csv', index_col=0, encoding= 'latin1')
surf_df=pd.read_csv('surfboi.csv', index_col=0, encoding= 'latin1')

"""
print(df.head())
mean_pop=df["1961"].mean()
print(mean_pop)
df["Sint Maarten (Dutch part)"]=df["Sint Maarten (Dutch part)"].fillna(mean_pop)
df.info()"""


# CLEANING

# Filling in empty values in the datasets
years=[]
for i in range(1960,2017):
    year=str(i)
    gdp_mean = gdp_df[year].mean()
    pop_mean = pop_df[year].mean()
    surf_mean = surf_df[year].mean()
    gdp_df[year]=gdp_df[year].fillna(gdp_mean)
    pop_df[year]=pop_df[year].fillna(pop_mean)
    surf_df[year]=surf_df[year].fillna(surf_mean)
    years.append(i)


# Transposing datasets
gdp_df = gdp_df.transpose()
pop_df = pop_df.transpose()
surf_df = surf_df.transpose()



# REGRESSION

reg = LinearRegression()

# Adding year 2020 for the purpose of predicting
years.append(2020)
# Concerting normal array to numpy array and reshaping the years array
years=np.array(years).reshape(1, -1)

# Creating the prediction space
prediction_space = np.linspace(1960,2020).reshape(-1,1)
# Fitting the model to the data
reg.fit(years, gdp_df["Senegal"])
# Computing predictions over the prediction space: y_pred
y_pred = reg.predict(prediction_space)

# Printing regression score
print(reg.score(years, gdp_df["Senegal"]))

"""
# Plotting regression line
plot1=figure(plot_width=400, plot_height=400)
plot1.line(prediction_space, y_pred, color='black', line_width=3)
# CALCULATION OF PEARSON CORRELATION COEFFICIENT AND DISPLAY OF SCATTER PLOT TO SHOW RELATION
#defining pearson coeff function
def pcoeff(x, y):
    corr_mat = np.corrcoef(x, y)
    return corr_mat[0,1]
# Calculating coefficient of correlation (Pearson)
coeff = pcoeff(gdp_df.loc[["Senegal"]],pop_df.loc[["Senegal"]])
print(coeff)
plot2=figure(plot_width=400, plot_height=400)
plot2.circle(gdp_df.loc[["Senegal"]],pop_df.loc[["Senegal"]])
# POPULATION DENSITY OF COUNTRIES OVER VARIOUS YEARS
pops = np.array(pop_df.loc[["Senegal"]])
geeps = np.array(gdp_df.loc[["Senegal"]])
pd = pops/geeps
plot3=figure(plot_width=400, plot_height=400)
plot3.line(pop_df.loc[["Senegal"]], gdp_df.loc[["Senegal"]])
layout=row(plot1, plot2, plot3)
"""
