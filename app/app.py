from flask import Flask, request
from db_loader import load_data, query, home_query

app = Flask(__name__)

@app.route("/")
def hello():
    result = home_query()
    return {"results": result}

@app.route("/load")
def load():
    load_data()
    return "Data Successfully Loaded"

@app.route("/query")
def query_data():
    filters = dict(request.args)
    if filters:
        data = query(filters)
    else:
        data = query()
    return {"a": data}

if __name__ == "__main__":
	app.run(debug=True,host="0.0.0.0")