from flask import Flask,send_file,render_template
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns

fig,ax=plt.subplots(figsize=(10,10))
ax=sns.set_style(style="darkgrid")

#------------------------------------------------ Vizualisations will go below 
x=[i for i in range(100)]
y=[i for i in range(100)]
#------------------------------------------------

app=Flask(__name__)

@app.route('/') #this is the root directory for local,  will need to be changed to the key or equivelant 
def home():
    return render_template('index.html')  

@app.route('/visualize') 
def visualize():
    sns.lineplot(x,y)
    canvas=FigureCanvas(fig)
    img=io.BytesIO()
    fig.savefig(img)
    img.see(0)
    return send_file(img,mimetypes='img/png')
#above section converts image to bytes and displays on the Canvas aka HTML 

if __name__ == "__main__":
    app.run()

    #visuals will need to be constructed in the flask app, then the paths are what go in the img tag of the html
