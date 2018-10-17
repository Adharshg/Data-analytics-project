import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

pop='population.csv'
df=pd.read_csv(pop)

#print(df.head())
"""
mean_pop=df["1961"].mean()
print(mean_pop)

df["Sint Maarten (Dutch part)"]=df["Sint Maarten (Dutch part)"].fillna(mean_pop)
df.info()
"""
