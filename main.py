from flask import Flask,render_template,jsonify,request,abort,Response
from flask_cors import CORS
import requests
import random

app = Flask(__name__)
CORS(app)

@app.route('/tasks',methods=["POST"])
def schedule():
    
    json = request.get_json()
    id = random.randrange(1,5e4+1)
    print("Task scheduled with id:{0}, url:{1} and delay:{2}".format(id,json["url"],json["delay"]))
    return jsonify({"id":id})


@app.route('/tasks/<id>',methods=["DELETE"])
def cancel(id):
    
    print("Cancelled task with id:{0}".format(id))

    # Check if cancelled successfully
    if(True):
        return jsonify(True)
    return jsonify(False)


@app.route('/tasks/<id>',methods=["GET"])
def checkStatus(id):
    
    # Check if task with that id exists
    if(True):
        status = ["Scheduled", "Running", "Completed", "Failed", "Cancelled"]
        return jsonify(random.choice(status))
    
    return Response("No task found",status=404,mimetype="application/json")


@app.route('/tasks',methods=["PATCH"])
def modify():
    
    json = request.get_json()

    # Check if task with json["id"] exists
    if(True):
        print("Modifying task with id:{0}, url:{1} and delay:{2}".format(json["id"],json["url"],json["delay"]))

        # Check if successfully modified
        if(True):
            return jsonify(True)
        else:
            return jsonify(False)
    
    return Response("No task found",status=404,mimetype="application/json")


@app.route('/tasks/retrieve',methods=["GET"])
def retrieveAll():
    
    tasks = []

    # Iterate and append all task objects with id, url, delay and status to tasks list

    return jsonify(tasks)


@app.route('/tasks/retrieve/<status>',methods=["GET"])
def retrieveWithStatus(status):
    
    tasks = []

    # Iterate and append all task objects with id, url, delay which have status=status to tasks list

    return jsonify(tasks)

if __name__ == '__main__':
    app.debug=True
    app.run()