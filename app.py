from flask import Flask, render_template, url_for, request
import numpy as np 
import pandas as pd 
from helpers import *

import warnings 
warnings.filterwarnings('ignore')

app = Flask(__name__)

predicted = pd.read_csv('predicted.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/after', methods=['GET','POST'])
def after():
    given = []
    val1 = {'name' : request.form['name_1'], 'year' : int(request.form['year_1'])}
    val2 = {'name' : request.form['name_2'], 'year' : int(request.form['year_2'])}
    val3 = {'name' : request.form['name_3'], 'year' : int(request.form['year_3'])}
    
    given.append(val1)
    given.append(val2)
    given.append(val3)
    
    recs = recommend_songs(given, predicted)
    return render_template('after.html', recs=recs)