import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template, redirect, flash, send_file
from sklearn.preprocessing import MinMaxScaler
from werkzeug.utils import secure_filename
import pickle
import tensorflow as tf
from keras.models import Sequential,load_model,model_from_json
from keras.layers import Dense, Dropout,Activation,MaxPooling2D,Conv2D,Flatten
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.utils import load_img
from keras.preprocessing import image
import numpy as np
import h5py
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template, redirect, flash, send_file
from sklearn.preprocessing import MinMaxScaler
from werkzeug.utils import secure_filename
import pickle
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

app = Flask(__name__) #Initialize the flask App

model = load_model('theft.h5')
sc = pickle.load(open('StandardScaler.pk', 'rb'))
@app.route("/")
@app.route("/index")
def index():
	return render_template('index.html')

@app.route('/chart')
def chart():
	return render_template('chart.html')

#@app.route('/future')
#def future():
#	return render_template('future.html')    

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/preview', methods=["POST"])
def preview():
    global global_df
    dataset = request.files['datasetfile']
    df = pd.read_csv(dataset)
    df.set_index('Id', inplace=True)
    global_df = df
    return render_template("preview.html", df_view=df)





#@app.route('/home')
#def home():
 #   return render_template('home.html')

@app.route('/prediction', methods = ['GET', 'POST'])
def prediction():
    return render_template('prediction.html')


#@app.route('/upload')
#def upload_file():
#   return render_template('BatchPredict.html')



@app.route('/predict', methods=['POST'])
def predict():
    meter_id = request.form['meter_id']

    # Load dataset
    df = pd.read_csv("upload.csv")   # correct path haaki

    # Filter row using meter_id
    row = df[df['Id'] == int(meter_id)]

    if row.empty:
        return render_template('prediction.html',
                               prediction_text="Meter ID not found")

    # Select features (same order as training)
    features = row[['energy_median','energy_mean','energy_max',
                    'energy_count','energy_std','energy_sum','energy_min']]

    # Scale + predict
    scaled = sc.transform(features)
    prediction = model.predict(scaled)

    if prediction[0][0] > 0.5:
        result = "Unfaithful (Theft Detected)"
    else:
        result = "Faithful (Normal Usage)"

    return render_template('prediction.html',
                           prediction_text=result)





@app.route('/performance')
def performance():
	return render_template('performance.html')   
    
if __name__ == "__main__":
    app.run(debug=True)
