import psycopg2
from flask import Flask, render_template, jsonify, request, abort, Response
from flask_cors import CORS
import requests
import random
import time

from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from datetime import timedelta  # required for current time
from datetime import datetime

import logging
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

conn = psycopg2.connect(
    dbname="jobs",
    user="postgres",
    password="postgres@123",
    host="localhost",
    port="5432"
)
# tableName defines the name of the table that will be updated in DB
allTaskTable = "all_jobs"
tableName = "apscheduler_jobs"
cur = conn.cursor()
# scheduler = BackgroundScheduler()

jobstores = {
    # 'default': SQLAlchemyJobStore(url='postgresql://postgres:postgres@123@localhost:5432/jobs', tablename='scheduler_jobs')
    'default': MemoryJobStore()
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


def scheduleInDb(TaskURL, RunTime):

    print("SCHEDULING IN DB: ", TaskURL, RunTime)

    idQuery = "INSERT INTO " + allTaskTable + " (url,run_time,status)" + " VALUES('{url}','{run_time}','Added')".format(url=TaskURL,
                                                                                                                        run_time=RunTime) + " RETURNING id;"
    cur.execute(idQuery)
    Taskid = cur.fetchone()[0]
    conn.commit()

    scheduleQuery = "INSERT INTO " + tableName + " (id,url,run_time,status)" + "VALUES('{id}','{url}','{run_time}','Scheduled')".format(id=Taskid,
                                                                                                                                        url=TaskURL, run_time=RunTime) + ";"
    cur.execute(scheduleQuery)
    conn.commit()
    print("Task scheduled with id : ", Taskid)
    return Taskid


def cancelInDb(Taskid):
    cancelQuery = "UPDATE " + tableName + \
        " SET status = 'Cancelled' WHERE id = " + Taskid
    cur.execute(cancelQuery)
    conn.commit()


def runningInDb(Taskid):
    runningQuery = "UPDATE " + tableName + \
        " SET status = 'Running' WHERE id = " + Taskid
    cur.execute(runningQuery)
    conn.commit()


def completedInDb(Taskid):
    completedQuery = "UPDATE " + tableName + \
        " SET status = 'Completed' WHERE id = " + Taskid
    cur.execute(completedQuery)
    conn.commit()


def failedInDb(Taskid):
    failedQuery = "UPDATE " + tableName + \
        " SET status = 'Failed' WHERE id = " + Taskid
    cur.execute(failedQuery)
    conn.commit()


# Callback Function


def lambdaCaller(TaskURL, Taskid):
    print("Started Invocation")
    runningInDb(Taskid)
    # time.sleep(50)
    send = requests.get(TaskURL)
    res = eval(send.content)
    print(send.status_code, res)
    if(send.status_code != 200 or 'errorMessage' in res):
        print("Task failed")
        failedInDb(Taskid)
    else:
        print("Completed lambda: ", Taskid, TaskURL)
        completedInDb(Taskid)


# WARNING : While testing remember that the schedule function takes schedule time in miliseconds, so provide parameters accordingly
@app.route('/tasks', methods=["POST"])
def schedule():

    json = request.json

    TaskURL = json['TaskURL']
    timeInMS = json['timeInMS']

    print(TaskURL, timeInMS)

    # Get unique ID from postgres [TODO]
    now = datetime.utcnow()
    id = scheduleInDb(TaskURL, now + timedelta(milliseconds=timeInMS))

    scheduler.add_job(
        lambdaCaller,
        trigger='date',
        jobstore='default',
        args=[TaskURL, str(id)],
        id=str(id),
        max_instances=1,
        run_date=now + timedelta(milliseconds=timeInMS)
    )

    print("Task scheduled with id:{0}, url:{1} and delay:{2}".format(
        id, json["TaskURL"], json["timeInMS"]))

    return jsonify({"id": id})


@ app.route('/tasks/<Taskid>', methods=["DELETE"])
def cancel(Taskid):

    print("Cancel ID: ", Taskid)

    # Checking if cancelled successfully [DONE]
    try:
        scheduler.get_job(Taskid, 'default')
    except:
        print("Job with id: ", Taskid, "Not found")
        return jsonify(False)

    # Checking if the Taskid is valid and can be cancelled [DONE]
    try:
        scheduler.remove_job(Taskid)
        cancelInDb(Taskid)
        print("Cancelled task with id:{0}".format(Taskid))
        return jsonify(True)
    except Exception as err:
        print("ERROR: ", err)
        print("TaskID ", Taskid, " doesn't exist")
        return jsonify(False)


# Implement Check Status [TODO]

@ app.route('/tasks/<Taskid>', methods=["GET"])
def checkStatus(Taskid):

    retrieveQuery = "SELECT status FROM " + tableName + \
        " WHERE id='{givenId}';".format(givenId=Taskid)
    cur.execute(retrieveQuery)
    fetchedvalues = cur.fetchone()
    # # Iterate and append all task objects with id, url, delay which have status=status to tasks list

    return jsonify(fetchedvalues[0])


# Allow to change schedule acc. to Crio Doc
@ app.route('/tasks', methods=["PATCH"])
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
@ app.route('/tasks/retrieve', methods=["GET"])
def retrieveAll():

    retrieveQuery = "SELECT id,url,run_time,status FROM " + tableName
    cur.execute(retrieveQuery)
    fetchedTasks = cur.fetchall()
    # # Iterate and append all task objects with id, url, delay which have status=status to tasks list

    tasks = []

    for task in fetchedTasks:
        tasks.append({
            "Taskid": task[0],
            "TaskURL": task[1],
            "Runtime": task[2],
            "Status": task[3]
        })

    return jsonify(tasks)


@ app.route('/tasks/retrieve/<status>', methods=["GET"])
def retrieveWithStatus(status):

    retrieveQuery = "SELECT id,url,run_time FROM " + tableName + \
        " WHERE status='{fetchStatus}';".format(fetchStatus=status)
    cur.execute(retrieveQuery)
    fetchedTasks = cur.fetchall()
    # # Iterate and append all task objects with id, url, delay which have status=status to tasks list

    tasks = []

    for task in fetchedTasks:
        tasks.append({
            "Taskid": task[0],
            "TaskURL": task[1],
            "Runtime": task[2]
        })

    return jsonify(tasks)


if __name__ == '__main__':
    app.debug = True
    app.run()
