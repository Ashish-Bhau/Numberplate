from flask import Flask, request, render_template, app
import numpy as np

from .model import Car_Name_Plate
app=Flask(__name__)
@app.route('/index')

#@app.route('/')
def index():
    return Car_Name_Plate()

if __name__=="__main__":
    app.run(debug=True)