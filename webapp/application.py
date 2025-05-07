from flask import Flask, request, jsonify, render_template
import boto3
import os

app = Flask(__name__)

region = os.environ.get("AWS_REGION", "us-west-2")
dynamodb = boto3.resource('dynamodb', region_name=region)

USERS_TABLE = os.environ.get("USERS_TABLE", "OnCallUsers")
SCHEDULE_TABLE = os.environ.get("SCHEDULE_TABLE", "OnCallSchedule")
users_table = dynamodb.Table(USERS_TABLE)
schedule_table = dynamodb.Table(SCHEDULE_TABLE)

@app.route("/")
def index():
    schedule = schedule_table.scan().get('Items', [])
    current = sorted(schedule, key=lambda x: x['week_start'], reverse=True)
    current_oncall = current[0] if current else None
    return render_template("index.html", oncall=current_oncall)

@app.route("/users", methods=["GET", "POST", "DELETE"])
def users():
    if request.method == "GET":
        return jsonify(users_table.scan().get('Items', []))

    elif request.method == "POST":
        data = request.json
        users_table.put_item(Item={"id": data["id"], "name": data["name"], "email": data["email"]})
        return jsonify({"message": "User added"})

    elif request.method == "DELETE":
        data = request.json
        users_table.delete_item(Key={"id": data["id"]})
        return jsonify({"message": "User deleted"})

# Elastic Beanstalk looks for 'application'
application = app

if __name__ == "__main__":
    app.run(debug=True)
