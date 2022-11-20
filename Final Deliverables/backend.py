import requests
import numpy as np
from flask import Flask,render_template,request
import pickle
import collections
collections.Callable = collections.abc.Callable
# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "WtGCq52jbLpAf6KgOTSLokoZeKmNP_wAgP-7i6HxzyuF"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app= Flask(__name__)
#model=pickle.load(open('wqi.pkl','rb'))
@app.route('/')
def home() :
  return render_template("index.html")
@app.route('/login',methods = ['POST'])
def login() :
  temp=request.form["temp"]
  do = request.form["do"]
  ph = request.form["ph"]
  co = request.form["co"]
  bod = request.form["bod"]
  na = request.form["na"]
  tc = request.form["tc"]
  year = request.form["year"]
 
  total = [[float(temp),float(do),float(ph),float(co),float(bod),float(na),float(tc),int(year)]]
  payload_scoring = {"input_data": [{"field": [["temp","do","ph","co","bod","na","tc","year"]], "values": total}]}
  response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/b61b8352-d24c-4ede-b0f4-9dcd50fffa28/predictions?version=2022-11-19', json=payload_scoring,headers={'Authorization': 'Bearer ' + mltoken})
  print("Scoring response")
  y_pred=response_scoring.json()
  print(y_pred)
  wqi_class=y_pred['predictions'][0]['values'][0][0]
  if wqi_class==0:
    return render_template("index.html",showcase="The predicted water quality is Poor")
  elif wqi_class==2:
    return render_template("index.html",showcase="The predicted water quality is Medium")
  elif wqi_class==3:
    return render_template("index.html",showcase="The predicted water quality is Good")
  elif wqi_class==4:
    return render_template("index.html",showcase="The predicted water quality is Excellent")

if __name__ == '__main__':
     app.run(debug = True,port=5000)