from flask import Flask, request, app,render_template
from flask import Response
import pickle
import numpy as np
import pandas as pd


application = Flask(__name__)
app=application

encoder=pickle.load(open("/config/workspace/Model/encoderfruad.pkl", "rb"))
model = pickle.load(open("/config/workspace/Model/modelrffruad.pkl", "rb"))

## Route for homepage

@app.route('/')
def index():
    return render_template('index.html')

## Route for Single data point prediction
@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
    result=""

    if request.method=='POST':

        step=int(request.form.get("step"))
        customer=int(request.form.get("customer"))
        age=int(request.form.get("age"))
        gender=int(request.form.get("gender"))
        merchant=int(request.form.get("merchant"))
        category=(request.form.get("category"))
        amount=float(request.form.get("amount"))

        category=encoder.transform([category])[0]
        new_data=[[step,customer,age,gender,merchant,category,amount]]

        predict=model.predict(new_data)
       
        if predict[0] ==1 :
            result = 'Fraud'
        else:
            result ='not Fraud'
            
        return render_template('single_prediction.html',result=result)

    else:
        return render_template('home.html')


if __name__=="__main__":
    app.run(host="0.0.0.0")