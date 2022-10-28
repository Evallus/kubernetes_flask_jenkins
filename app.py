import os
import socket

from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId


app = Flask(__name__)
host = os.environ['DB_URL']
port = 27017
username = os.environ['MONGO_INITDB_ROOT_USERNAME']
password = os.environ['MONGO_INITDB_ROOT_PASSWORD']
db_name = 'dev'

client = MongoClient(host=host,
                     port=27017,
                     username=username,
                     password=password,
                     authSource='admin')
db = client[db_name]


@app.route("/")
def index():
    hostname = socket.gethostname()
    return jsonify(
        message="Welcome to Tasks app! I am running inside {} pod!".format(hostname)
    )


@app.route("/tasks")
def get_all_tasks():
    tasks = db.task.find()
    data = []
    for task in tasks:
        item = {
            "id": str(task["_id"]),
            "task": task["task"]
        }
        data.append(item)
    return jsonify(
        data=data
    )


@app.route("/task", methods=["POST"])
def create_task():
    data = request.get_json(force=True)
    db.task.insert_one({"task": data["task"]})
    return jsonify(
        message="Task saved successfully!"
    )


@app.route("/task/<id>", methods=["PUT"])
def update_task(id):
    data = request.get_json(force=True)["task"]
    response = db.task.update_one({"_id": ObjectId(id)}, {"$set": {"task": data}})
    if response.matched_count:
        message = "Task updated successfully!"
    else:
        message = "No Task found!"
    return jsonify(
        message=message
    )


@app.route("/task/<id>", methods=["DELETE"])
def delete_task(id):
    response = db.task.delete_one({"_id": ObjectId(id)})
    if response.deleted_count:
        message = "Task deleted successfully!"
    else:
        message = "No Task found!"
    return jsonify(
        message=message
    )


@app.route("/hello")
def welcome():
    return "<p>Hello world!</p>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)