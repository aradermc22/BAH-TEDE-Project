from flask import Flask,send_file,render_template
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns
import pyodbc 
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from sqlalchemy.engine import URL
import jinja2
import json
import plotly
import plotly.express as px


connection_string = ('Driver={ODBC Driver 17 for SQL Server};Server=tcp:unstructured-data-server.database.windows.net,1433;Database=unstructured-data;Uid=project-admin;Pwd={password22$};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
connection_url = URL.create('mssql+pyodbc', query={'odbc_connect': connection_string})
engine = create_engine(connection_url, fast_executemany=True)
#------------------------------------------------------------------------------------------------------------------------------------------
#steam_data = pd.read_sql('SELECT * FROM steam_source_data', engine)
#print(steam_data)

top_ten_devs = pd.read_sql('SELECT * FROM Top_Ten_Played_Developers', engine)
print(top_ten_devs)

counts = pd.read_sql('SELECT * FROM Developer_Released_Games_By_Year', engine)
print(counts)




#--------------------------------------------------------------------------- Visualization 4 --------------------------------------------------

ax=sns.set_style(style="darkgrid")

#------------------------------------------------ 
x=[i for i in range(100)]
y=[i for i in range(100)]
#------------------------------------------------

app=Flask(__name__, template_folder='BAH-TEDE-Project')

@app.route('/') 
def home():
    return render_template('index2.html')  

@app.route('/visualize') 
def visualize():
    fig = px.line(counts, x='release_year', y='Count', color='developer')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return send_file(graphJSON=graphJSON)

#--------------------------------------------------------------------------- Visualization 3 --------------------------------------------------

#fig,ax=plt.subplots(figsize=(10,10))
#ax=sns.set_style(style="darkgrid")

#------------------------------------------------ 
m=[i for i in range(75)]
n=[i for i in range(75)]
#------------------------------------------------
 

@app.route('/viz3') 
def viz3():
    sns.lineplot(m,n)
    canvas=FigureCanvas(fig)
    img=io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img,mimetype='img/png')
 
#--------------------------------------------------------------------------- Visualization 2 -s-------------------------------------------------


#------------------------------------------------ 
q=[i for i in range(50)]
w=[i for i in range(50)]
#------------------------------------------------
 

@app.route('/viz2') 
def viz2():
    sns.lineplot(q,w)
    canvas=FigureCanvas(fig)
    img=io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img,mimetype='img/png')
#--------------------------------------------------------------------------- # Visualization 1 --------------------------------------------------


#------------------------------------------------ 
#e=[i for i in range(-1000)]
#r=[i for i in range(-1000)]
#------------------------------------------------

ax=sns.set_style(style="darkgrid")

@app.route('/viz1') 
def viz1():
    #sns.lineplot(e,r)   
    canvas=FigureCanvas(fig)
    img=io.BytesIO()
    plt.savefig(img)
    img.seek(0)
    
    return send_file(img,mimetype='img/png')


#------------------------------------------------------------Run----------------------------------------------------
if __name__ == "__main__":
    app.debug = True
    app.run()

