from flask import Flask

app = Flask(__name__)

@app.route("/", methods=["POST"])
def create():
    return "hi"

if __name__ == "__main__":
    app.run(port=3030, debug=True)