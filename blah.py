#https://notebooks.azure.com/Microsoft/projects/AzureCosmosDB/html/Cosmos%20DB%20and%20its%20Python%20SDK.ipynb#Playing-with-the-Python-SDK
from flask import Flask
from flask_cors import cross_origin, CORS
app = Flask(__name__)
cors = CORS(app, resources={r'/*':{"origins": 'http://localhost:4000'}})

@app.route('/')
# @cross_origin(headers=['Content-type','Accept'])
def hello_world():
   return 'Updated'

if __name__ == '__main__':
   app.run(host='0.0.0.0',debug=True)