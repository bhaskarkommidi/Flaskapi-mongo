from flask import Flask, Response, request
import  pymongo
import json
from bson.objectid import ObjectId
app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(host="localhost", port=27017, serverSelectionTimeoutMS = 1000)
    db = mongo.Coding
    mongo.server_info()
except:
    print("Can't connect to DB")


@app.route('/languages', methods=["GET"])
def get():
    try:
        data = list(db.codinglang.find())
        for language in data:
            language["_id"] = str(language["_id"])
        return Response(
            response = json.dumps(data), 
            status=500,
            mimetype="application/json"
            ) 
    except Exception as e:
        print(e)
        return Response(
            response = json.dumps(
                {"message":"can't get"}), 
                status=500,
                mimetype="application/json"
                ) 


##################################################
@app.route("/languages", methods=["POST"])
def create():
    try:
        language = {"name":request.form["name"]}
        dbResponse = db.codinglang.insert_one(language)
        print(dbResponse.inserted_id)
        return Response(
            response = json.dumps(
                {"message":"hi", 
                "id":f"{dbResponse.inserted_id}"
                }), 
                status=200,
                mimetype="application/json"
                )
    except Exception as e:
        print(e)

##################################################
@app.route("/languages/<id>", methods=["PATCH"])
def update(id):
    return id

if __name__ == "__main__":
    app.run(port=3030, debug=True)