# Imports
from flask import Flask, Response, request
import  pymongo
import json
import os
from bson.objectid import ObjectId
import settings

app = Flask(__name__)

mongo_uri = os.getenv("MONGO_URI")
client = pymongo.MongoClient(mongo_uri) 
db = client.get_database('Digi_Flask')  
col = db.Languages 


#########################
#GET
#########################
@app.route('/languages', methods=["GET"])
def get():
    try:
        data = list(db.col.find())
        for language in data:
            language["_id"] = str(language["_id"])
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
@app.route("/languages", methods=["POST"])
def create():
    try:
        language = {"name":request.form["name"]}
        dbResponse = db.col.insert_one(language)
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
@app.route("/languages/<string:name>", methods=["PATCH"])
def update(name):
    try:
        dbResponse = db.col.update_one(
            {"name":name},
            {"$set":{"name":request.form["name"]}}
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
@app.route("/languages/<string:name>", methods=["DELETE"])
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