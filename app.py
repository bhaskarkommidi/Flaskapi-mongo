from flask import Flask, Response, request
import  pymongo
import json
app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(host="localhost", port=27017, serverSelectionTimeoutMS = 1000)
    db = mongo.Coding
    mongo.server_info()
except:
    print("Can't connect to DB")

@app.route("/", methods=["POST"])
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

if __name__ == "__main__":
    app.run(port=3030, debug=True)