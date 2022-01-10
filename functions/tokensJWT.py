from datetime import datetime
from functions import db as db
from flask import Flask
from flask import jsonify
from flask import request
from flaskext.mysql import MySQL
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
def loginToken(username,password):
    UNAUTHORIZED = False
    if username and password:
        credentials = db.getUserByCredentials(username,password)
        if not credentials:
            UNAUTHORIZED = True 
    else:
        UNAUTHORIZED = True
        
    if not UNAUTHORIZED:
        access_token = create_access_token(identity=username)
        user_id = db.getUserData(username)[0]
        db.logDataIntoDB(datetime.now(),'GET_TOKEN',user_id[0][1],access_token)
        return jsonify(access_token=access_token),200
    
    return jsonify({"msg": "Bad username or password"}), 401