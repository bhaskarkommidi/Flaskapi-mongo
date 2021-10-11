# Imports
from flask import Flask, Response, request
#from bson.objectid import ObjectId
from Settings.security import authenticate, identity
from flask_jwt import JWT, jwt_required, current_identity
from flask_restful import Resource, Api
from flasgger import Swagger
from flasgger.utils import swag_from
from flasgger import LazyString, LazyJSONEncoder
import  pymongo
import json
import os
import Settings.settings

 
app = Flask(__name__)
app.secret_key = 'secret'
jwt = JWT(app, authenticate, identity)



mongo_uri = os.getenv("MONGO_URI")
client = pymongo.MongoClient(mongo_uri) 
db = client.get_database('Digi_Flask')  
col = db.Products 


 ########### Swagger %%%%%%%%%%%%%%%%%%%%%%%
# app.config["SWAGGER"] = {"title": "Swagger-UI", "uiversion": 2}

# swagger_config = {
#     "headers": [],
#     "specs": [
#         {
#             "endpoint": "apispec_1",
#             "route": "/apispec_1.json",
#             "rule_filter": lambda rule: True,  # all in
#             "model_filter": lambda tag: True,  # all in
#         }
#     ],
#     "static_url_path": "/flasgger_static",
#     # "static_folder": "static",  # must be set by user
#     "swagger_ui": True,
#     "specs_route": "/swagger/",
# }

# template = dict(
#     swaggerUiPrefix=LazyString(lambda: request.environ.get("HTTP_X_SCRIPT_NAME", ""))
# )

# app.json_encoder = LazyJSONEncoder
# swagger = Swagger(app, config=swagger_config, template=template)


#########################
#GET
#########################
@app.route('/products', methods=["GET"])
def get():
    try:
        data = list(db.col.find())
        for product in data:
            product["_id"] = str(product["_id"])
        return Response(
            response = json.dumps(data,default=str), 
            status=500,
            mimetype="application/json"
            ) 
    except Exception as e:
        print(e)
        return Response(
            response = json.dumps(
                {"message":"can't get"},default=str), 
                status=404,
                mimetype="application/json"
                ) 


#########################
#POST
#########################
@app.route("/products", methods=["POST"])
@jwt_required()
def create():
    try:
        sku = {"sku":request.form["sku"]}
        name = {"name":request.form["name"]}
        description = {"description":request.form["description"]}
        category = {"category":request.form["category"]}
        price = {"price":request.form["price"]}
        metadata = {"metadata":request.form["metadata"]}
        dbResponse = db.col.insert_one(name)
        print(dbResponse.inserted_id)
        return Response(
            response = json.dumps(
                {"message":"Created", 
                "id":f"{dbResponse.inserted_id}"
                },default=str), 
                status=200,
                mimetype="application/json"
                )
    except Exception as e:
        print(e)

#########################
#PATCH
#########################
@app.route("/products/<string:name>", methods=["PATCH"])
@jwt_required()
def update(name):
    try:
        dbResponse = db.col.update_one(
            {"name":name},
            {"$set":{"sku":request.form["sku"],"name":request.form["name"],"description":request.form["description"],"category":request.form["category"],"price":request.form["price"],"metadata":request.form["metadata"]}}
        )
        # for l in dir(dbResponse):
        #     print(f"{l}")
        if dbResponse.modified_count == 1:  
            return Response(
                response = json.dumps({"message":"updated!!"},default=str), 
                status=200,
                mimetype="application/json"
                )
        return Response(
            response = json.dumps({"message":"Nothing to Update!!"},default=str), 
            status=200,
            mimetype="application/json"
            )
    except Exception as e:
        print(e)
        return Response(
            response = json.dumps({"message":"OOPS!! can't update"},default=str), 
                status=500,
                mimetype="application/json"
                )

#########################
#DELETE
#########################
@app.route("/products/<string:name>", methods=["DELETE"])
@jwt_required()
def delete(name):
    try:
        dbResponse = db.col.delete_one({"name":name})
        if dbResponse.deleted_count == 1:
            return Response(
                response = json.dumps({"message":"Deleted!!", "name":f"{name}"},default=str), 
                status=200,
                mimetype="application/json"
                )
            # for l in dir(dbResponse):
            #      print(f"{l}")
        return Response(
            response = json.dumps({"message":"Not Found!!", "name":f"{name}"},default=str), 
            status=404,
            mimetype="application/json"
            )
    except Exception as e:
        print(e)
        return Response(
            response = json.dumps({"message":"OOPS!! can't delete"},default=str), 
                status=500,
                mimetype="application/json"
                )
            




if __name__ == "__main__":
    app.run(port=3030, debug=True)