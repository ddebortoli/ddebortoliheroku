# app.py
from flask import Flask, request, jsonify
from flask.helpers import send_from_directory
from flaskext.mysql import MySQL

#datetime
from datetime import datetime

#db.py
from functions import db as db

#TokensJWT
from functions import tokensJWT as tkn
import jwt as j
 


#Config
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = tkn.JWTManager(app)


def getUserFromToken(token):
    decoded = j.decode(token, options={"verify_signature": False})
    return decoded['sub']

#Get users info from db
@app.route('/ddebortoli/users/', methods=['GET'])
@tkn.jwt_required()
def users():
    "get data from users"
    #get variables
    auth =  (request.headers['Authorization']).split('Bearer ',1)[1]
    name = request.args.get("name", None)
    response = {}
    
    #Validations of name
    # name is string
    if str(name).isdigit():
        response["ERROR"],status = "name can't be numeric.",400
    # name value cant be null
    elif name == '':
        response["ERROR"],status = "name can't be null.",400
    elif not name:
        #fetch all
        data,status = db.getUserData()
        response["MESSAGE"] = data 
        
        #log Data to db
        user_id = db.getUserIdByName(getUserFromToken(auth))
        db.logDataIntoDB(datetime.now(),'GET_User_Info',user_id,auth)
    else:
        #fetch one
        data,status = db.getUserData(name)
        response["MESSAGE"] = data 
        #log data to db
        user_id = db.getUserIdByName(getUserFromToken(auth))
        db.logDataIntoDB(datetime.now(),'GET_User_Info',user_id,auth)
        
    # Return the response in json format
    return jsonify(response),status

#Generate JWTToken
@app.route('/ddebortoli/token/', methods=['GET'])
def token():
    "get JWT token"
    #get variables
    user = request.args.get("user", None)
    password = request.args.get("password", None)
    token = {}
    if not user or not password:
        token["ERROR"],status = "user and password are mandatory parameters",400
    else:
        token,status = tkn.loginToken(user,password)
    return token,status

#get user's log
@app.route('/ddebortoli/logs/', methods=['GET'])
@tkn.jwt_required()
def userLogs():
    "get user's log"
    data,status = db.getLogHistory()
    response = {}
    response['MESSAGE'] = data
    return jsonify(response),status

#Get repositories by id
@app.route('/ddebortoli/repositories/', methods=['GET'])
@tkn.jwt_required()
def repositories():
    "get repositories by id or catch all"
    id = request.args.get("repository_id", None)
    response = {}
    repositories,status = db.getRepositoryById(id)
    
    #log data to db
    auth =  (request.headers['Authorization']).split('Bearer ',1)[1]
    user_id = db.getUserIdByName(getUserFromToken(auth))
    db.logDataIntoDB(datetime.now(),'GET_Repositories',user_id,auth)
    
    response["MESSAGE"] = repositories;
    #return response
    return jsonify(response),status

#swagger with flask_swagger_ui
from flask_swagger_ui import get_swaggerui_blueprint
SWAGGER_URL = '/ddebortoli/docs'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "ddebortoliheroku"
    },
)
app.register_blueprint(swaggerui_blueprint)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
    