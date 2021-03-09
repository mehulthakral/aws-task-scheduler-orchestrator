from flask import Flask, render_template, jsonify, request, abort, Response
from flask_cors import CORS
import requests
import random

from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from datetime import timedelta  # required for current time
from datetime import datetime

import logging
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

scheduler = BackgroundScheduler()

jobstores = {
    'default': SQLAlchemyJobStore(url='postgresql://postgres:postgres@123@localhost:5432/jobs', tablename='scheduler_jobs')
}

executors = {
    'default': ThreadPoolExecutor(20)
}

job_defaults = {
    'coalesce': False,
    'max_instances': 1
}

scheduler = BackgroundScheduler(
    jobstores=jobstores,
    executors=executors,
    job_defaults=job_defaults,
    timezone=utc
)

app = Flask(__name__)
CORS(app)

scheduler.start()

# Callback Function


def lambdaCaller(TaskURL):
    print("Running lambda: ", TaskURL)


@app.route('/tasks', methods=["POST"])
def schedule():

    json = request.json

    TaskURL = json['TaskURL']
    timeInMS = json['timeInMS']

    print(TaskURL, timeInMS)

    # Get unique ID from postgres [TODO]
    id = random.randrange(1, 5e4+1)

    now = datetime.utcnow()
    scheduler.add_job(
        lambdaCaller,
        trigger='date',
        jobstore='default',
        args=[TaskURL],
        id=str(id),
        max_instances=1,
        run_date=now + timedelta(milliseconds=timeInMS)
    )

    print("Task scheduled with id:{0}, url:{1} and delay:{2}".format(
        id, json["TaskURL"], json["timeInMS"]))

    return jsonify({"id": id})


@app.route('/tasks/<Taskid>', methods=["DELETE"])
def cancel(Taskid):

    print("Cancel ID: ", Taskid)

    # Checking if cancelled successfully [DONE]
    try:
        scheduler.get_job(Taskid, 'default')
    except:
        return jsonify(False)

    # Checking if the Taskid is valid and can be cancelled [DONE]
    try:
        scheduler.remove_job(Taskid)
        print("Cancelled task with id:{0}".format(Taskid))
    except:
        print("TaskID ", Taskid, " doesn't exist")
        return jsonify(False)


# Implement Check Status [TODO]

@app.route('/tasks/<Taskid>', methods=["GET"])
def checkStatus(Taskid):

    # # Check if task with that id exists
    # if(get_job(Taskid, jobstores) is not None):
    status = ["Scheduled", "Running", "Completed", "Failed", "Cancelled"]
    #     return jsonify(random.choice(status))

    # return Response("No task found", status=404, mimetype="application/json")


# Allow to change schedule acc. to Crio Doc
@app.route('/tasks', methods=["PATCH"])
def modify():

    print("ENTERED MODIFY")

    json = request.json
    Taskid = str(json['Taskid'])
    timeInMS = int(json['timeInMS'])
    print(Taskid, timeInMS)
    # Check if task with json["id"] exists
    try:
        print("Finding Taskid", Taskid)
        scheduler.get_job(Taskid, 'default')
        print("Modifying task with id:{0}, delay:{1}".format(
            json["Taskid"], json["timeInMS"]))
    except:
        # Taskid doesn't exist
        print("Taskid doesn't exist")
        return jsonify(False)

    # Trying to reshedule the job
    try:
        now = datetime.utcnow()
        scheduler.reschedule_job(
            job_id=Taskid,
            jobstore='default',
            trigger='date',
            run_date=now + timedelta(milliseconds=timeInMS)
        )

        print("Taskid ", Taskid, " rescheduled")
        return jsonify(True)
    except Exception as err:
        # Was not able to reschedule
        print("Not able to  reschedule")
        print("Error: ", err)
        return jsonify(False)


# Currently retriving all running tasks
@app.route('/tasks/retrieve', methods=["GET"])
def retrieveAll():

    jobList = scheduler.get_jobs()
    tasks = []

    # Iterate and append all task objects with id, url, delay and status to tasks list

    if jobList is not None:
        for job in jobList:
            tasks.append({"Taskid": job.id, "TaskName": job.name})

    return jsonify(tasks)


@app.route('/tasks/retrieve/<status>', methods=["GET"])
def retrieveWithStatus(status):

    tasks = []

    # # Iterate and append all task objects with id, url, delay which have status=status to tasks list

    return jsonify(tasks)


if __name__ == '__main__':
    app.debug = True
    app.run()
