# Importing Tkinter for the output window
from tkinter import *

# Entire back-end code defined as a function to serve for the front-end Tkinter code
def func(country):

    # IMPORTING PACKAGES

    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    import sqlalchemy
    
    from bokeh.io import output_file, show
    from bokeh.layouts import column, row, widgetbox
    from bokeh.models import ColumnDataSource, Select, HoverTool
    from bokeh.plotting import figure
    from bokeh.models.annotations import Title

    from numpy.random import random

    from sklearn.linear_model import LinearRegression


    # IMPORTING & ASSIGNING

    pop_df=pd.read_csv('final_population.csv', index_col=0, encoding = 'latin1')
    gdp_df=pd.read_csv('final_gdp.csv', index_col=0, encoding= 'latin1')
    surf_df=pd.read_csv('final_surfacearea.csv', index_col=0, encoding= 'latin1')

    # Acquiring the names of countries as list
    country_names=surf_df.index.values.tolist()


    
    # CLEANING

    # Filling in empty values in the datasets
    years=[]
    for i in range(1961,2016):
        temp=[]
        year=str(i)
        gdp_mean = gdp_df[year].mean()
        surf_mean = surf_df[year].mean()
        pop_mean = pop_df[year].mean()
        
        gdp_df[year]=gdp_df[year].fillna(gdp_mean)
        surf_df[year]=surf_df[year].fillna(surf_mean)
        pop_df[year]=pop_df[year].fillna(pop_mean)
        temp.append(i)
        years.append(temp)
        

    # Transposing datasets
    gdp_df = gdp_df.transpose()
    pop_df = pop_df.transpose()
    surf_df = surf_df.transpose()




    # REGRESSION

    reg = LinearRegression()

    # Concerting normal array to numpy array and reshaping the years array
    years=np.array(years)

    # Creating the prediction space
    prediction_space = np.arange(1960,2016,1).reshape(-1,1)
    # Fitting the model to  data
    reg.fit(years, gdp_df[country])

    # Computing predictions over the prediction space: y_pred
    y_pred = reg.predict(prediction_space)
    reg_score = reg.score(years, gdp_df[country])
    reg_score = 'Regression score: ' + str(reg_score)


    # Converting datatypes of the variables
    years = years.ravel().tolist()
    prediction_space = prediction_space.ravel().tolist()
    y_pred = y_pred.tolist()
    gdpval = gdp_df[country].values.ravel().tolist()

  
    # Predicting GDP for any year
    pred_year = int(input('Enter the year you wish to see the GDP for: '))
    m,c = np.polyfit(years ,gdp_df[country], 1)
    y =str((m * pred_year) + c)
    y= 'Predicted GDP for ' + str(pred_year) + ': ' + y
    

    # Plotting regression line
    hover1 = HoverTool(tooltips = [('year', '$x')], formatters = {'year':'datetime'})
    plot1=figure(plot_width=400, plot_height=400, x_axis_label='years', y_axis_label='GDP', tools=[hover1, 'pan', 'wheel_zoom'])
    plot1.scatter(years, gdpval)
    plot1.line(prediction_space, y_pred, color='black', line_width=2)
    t1 = Title()
    t1.text = 'Plot for Regression line'
    plot1.title = t1


    # CALCULATION OF PEARSON CORRELATION COEFFICIENT AND DISPLAY OF SCATTER PLOT TO SHOW RELATION

    # Defining pearson coeff function
    def pcoeff(x, y):
        corr_mat = np.corrcoef(x, y)
        return corr_mat[0,1]


    # Calculating coefficient of correlation (Pearson)
    coeff = pcoeff(gdp_df[country],pop_df[country])
    coeff= 'Pearson coefficient: ' + str(coeff)
    

    # Plotting the relation between population and GDP
    plot2=figure(plot_width=400, plot_height=400, x_axis_label='GDP', y_axis_label='Population')
    plot2.circle(gdp_df[country],pop_df[country])
    t2 = Title()
    t2.text = 'Relation between Popualtion and GDP (by year)'
    plot2.title = t2


    # POPULATION DENSITY OF COUNTRIES OVER VARIOUS YEARS

    pops = np.array(pop_df[country])
    surf = np.array(surf_df[country])
    pd = pops/surf

    # Conversion of numpy array to list
    pd = pd.tolist()

    # Plotting population density
    plot3=figure(plot_width=400, plot_height=400, x_axis_label='years', y_axis_label='Population Dnesity')
    plot3.line(years, pd)
    plot3.circle(years, pd, fill_color='white', size=4)
    t3 = Title()
    t3.text = 'Population density over the years'
    plot3.title = t3


    # DISPLAYING OUTPUT USING TKINTER
    
    # Printing obtained values
    def printreg():
        label = Label(mainframe, text= reg_score, borderwidth = 2)
        label.grid(row = 8, column = 1)
        
    def printy():
        label = Label(mainframe, text= y, borderwidth = 2)
        label.grid(row = 6, column = 1)

    def printcoef():
        label = Label(mainframe, text= coeff, borderwidth = 2)
        label.grid(row = 10, column = 1)

    def printgraphs():
        layout=row(plot1, plot2, plot3)
        output_file('output.html')
        show(layout)

    root = Tk()
    root.title('OUTPUT OPTIONS')

    mainframe = Frame(root)
    mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
    mainframe.columnconfigure(0, weight = 1)
    mainframe.rowconfigure(0, weight = 1)
    mainframe.pack(pady = 100, padx = 100)

    # Creating three different buttons for three different modules of project
    button1 = Button(mainframe, text = 'Display Regression Score', command = printreg, borderwidth = 2)
    button1.grid(row = 1, column = 1, pady=(20, 10), padx=(40, 40))
    button2 = Button(mainframe, text = 'Display Pearson Coefficient', command = printcoef, borderwidth = 2)
    button2.grid(row = 2, column = 1, pady=(40, 10), padx=(40, 40))
    button3 = Button(mainframe, text = 'Display Predicted GDP', command = printy, borderwidth = 2)
    button3.grid(row = 0, column = 1, pady=(40, 10), padx=(40, 40))
    button4 = Button(mainframe, text = 'Display graphs', command = printgraphs, borderwidth = 2)
    button4.grid(row = 3, column = 1, pady=(40, 10), padx=(40, 40))
    button5 = Button(mainframe, text = 'EXIT', command =quit, borderwidth = 2)
    button5.grid(row = 4, column = 1, pady=(40, 10), padx=(40, 40))

    root.mainloop()



# Creating plain Bokeh layout (old)
"""
    # Create ColumnDataSource: source
    source = ColumnDataSource(data={
        'x' : years,
        'y' : (np.array(pop_df[country])/np.array(surf_df[country])).tolist()
    })

    # Create a new plot: plot

    plot3=figure(plot_width=400, plot_height=400)
    plot3.line(years, pd)
    plot3.circle(years, pd, fill_color='white', size=4)

    # Define a callback function: update_plot
    def update_plot(attr, old, new):
        print("in")
        for i in range(len(country_names)):
            print("yp")
            if new==country_names[i]: 
                pos=i
        else:
            print("Np")
            pos=-1
        
        # If the new Selection is 'female_literacy', update 'y' to female_literacy
        if pos>0:
            print("a")
            country=country_names[pos]
            source.data = {
                'x' : years,
                'y' : (np.array(pop_df[country])/np.array(surf_df[country])).tolist()
            }
        # Else, update 'y' to population
        else:
            print("b")
            source.data = {
                'x' : fertility,
                'y' : (np.array(pop_df["India"])/np.array(surf_df["India"])).tolist()
            }

    # Create a dropdown Select widget: select    
    select = Select(title="Select country", options=country_names, value='Aruba')

    # Attach the update_plot callback to the 'value' property of select
    select.on_change('value', update_plot)

    # Create layout and add to current document
    layout = row(plot1, plot2, column(widgetbox(select), plot3))
    curdoc().add_root(layout)
    """
