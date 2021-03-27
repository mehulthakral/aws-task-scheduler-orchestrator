import psycopg2
from flask import Flask, render_template, jsonify, request, abort, Response
from flask_cors import CORS
import requests
import random
import time
import string
import random
import create

from pytz import utc
import pytz
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
CORS(app, allow_headers='*', origins='*')

scheduler.start()


def scheduleInDb(TaskURL, RunTime, LambdaName, LambdaDescription):

    print("SCHEDULING IN DB: ", TaskURL, RunTime)

    idQuery = "INSERT INTO " + allTaskTable + " (url,run_time,lambda_name,lambda_description,status)" + " VALUES('{url}','{run_time}','{lambda_name}','{lambda_description}','Added')".format(url=TaskURL,
                                                                                                                                                                                              run_time=RunTime,
                                                                                                                                                                                              lambda_name=LambdaName,
                                                                                                                                                                                              lambda_description=LambdaDescription) + " RETURNING id;"
    cur.execute(idQuery)
    Taskid = cur.fetchone()[0]
    conn.commit()

    scheduleQuery = "INSERT INTO " + tableName + " (id,url,run_time,lambda_name,lambda_description,status)" + "VALUES('{id}','{url}','{run_time}','{lambda_name}','{lambda_description}','Scheduled')".format(id=Taskid,
                                                                                                                                                                                                              url=TaskURL,
                                                                                                                                                                                                              run_time=RunTime,
                                                                                                                                                                                                              lambda_name=LambdaName,
                                                                                                                                                                                                              lambda_description=LambdaDescription) + ";"
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


def lambdaCaller(TaskURL, Taskid, retries, timeBetweenRetries):
    print("Started Invocation")
    runningInDb(Taskid)
    # time.sleep(50)
    send = requests.get(TaskURL)
    try:
        res = eval(send.content)
    except Exception as e:
        print(e)
        res = send.content
    print(send.status_code, res)
    if(send.status_code != 200 or isinstance(res, dict) and 'errorMessage' in res):
        print("Task failed")
        failedInDb(Taskid)
        if retries is not None and retries > 0:
            print("RETRYING TASKID: ", Taskid, " RETRY LEFT: ", retries)
            now = datetime.now(utc)
            scheduler.add_job(
                lambdaCaller,
                trigger='date',
                jobstore='default',
                args=[TaskURL, str(Taskid), int(retries)-1,
                      timeBetweenRetries],
                id=str(Taskid),
                max_instances=1,
                run_date=now + timeBetweenRetries
            )

    else:
        print("Completed lambda: ", Taskid, TaskURL)
        completedInDb(Taskid)


def check(json, l):
    for att in l:
        if att not in json:
            return False, Response(att + " attribute is required", status=400, mimetype="application/json")
    return True, ""


# Additional details for date time
# For frontend : https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/datetime-local
# Apply min attribute for current time as a function can't be scheduled in past


# WARNING : While testing remember that the schedule function takes schedule time in miliseconds, so provide parameters accordingly
@app.route('/tasks', methods=["POST"])
def schedule():

    # Option 1 : Using delay in miliseconds
    # Option 2 : Using date and time

    json = request.json

    correct, res = check(json, ['schedulingOption', 'taskType'])

    if(correct == False):
        return res

    choosenOption = json['schedulingOption']
    taskType = json['taskType']
    TaskURL = None
    retries = None
    timeBetweenRetries = None

    if("retries" in json):
        correct, res = check(json, ['timeBetweenRetries'])

        if(correct == False):
            return res

        retries = json['retries']
        timeBetweenRetries = json['timeBetweenRetries']

    else:
        retries = 0
        timeBetweenRetries = 0

    try:
        retries = int(retries)
        timeBetweenRetries = int(timeBetweenRetries)
    except:
        retries = 0
        timeBetweenRetries = 0

    LambdaName = str(json['LambdaName']) if "LambdaName" in json else ''.join(random.choices(string.ascii_uppercase +
                                                                                             string.digits, k=7))
    LambdaDescription = str(
        json['LambdaDescription']) if "LambdaDescription" in json else ''

    if(taskType.lower() == "function"):
        correct, res = check(json, ['funcSrc', 'requirements', 'region',
                                    'access_key', 'secret_access_key', 'session_token', 'args'])

        if(correct == False):
            return res

        funcSrc = json["funcSrc"]
        requirements = json["requirements"]
        region = json["region"]
        access_key = json["access_key"]
        secret_access_key = json["secret_access_key"]
        session_token = json["session_token"]
        args = json["args"]

        success, res = create.deploy(
            funcSrc, requirements, LambdaName, region, access_key, secret_access_key, session_token)

        if(success == False):
            return Response(res, status=400, mimetype="application/json")

        print("Deployed successfully: " + res)
        if(len(args) > 0):
            for a in args:
                res += "/"+a
        TaskURL = res

    elif(taskType.lower() == "url"):
        correct, res = check(json, ['TaskURL'])

        if(correct == False):
            return res

        TaskURL = json["TaskURL"]

    else:
        return Response("Please provide correct taskType", status=400, mimetype="application/json")

    print("RETRIES: ", retries)
    print(timeBetweenRetries)

    if choosenOption == '1':
        correct, res = check(json, ['timeInMS'])

        if(correct == False):
            return res

        timeInMS = int(json['timeInMS'])
        now = datetime.now(utc)
        id = scheduleInDb(
            TaskURL, now + timedelta(milliseconds=timeInMS), LambdaName, LambdaDescription)

        print("GENERATED ID: ", id)

        scheduler.add_job(
            lambdaCaller,
            trigger='date',
            jobstore='default',
            args=[TaskURL, str(id), int(retries),
                  timedelta(milliseconds=timeBetweenRetries)],
            id=str(id),
            max_instances=1,
            run_date=now + timedelta(milliseconds=timeInMS)
        )

        return jsonify({"id": id})

    elif choosenOption == '2':
        correct, res = check(json, ['dateTimeValue'])

        if(correct == False):
            return res

        datetimeStr = json['dateTimeValue']
        print("Local time: ", datetimeStr)
        # Assuming the input will always from a Indian Timezone
        # Converting to utc
        local = pytz.timezone('Asia/Kolkata')
        # Expecting format from frontend: "13 Mar 2021 07:08:38"
        datetimeStr = datetime.strptime(datetimeStr, "%d %b %Y %H:%M:%S")
        local_time = local.localize(datetimeStr, is_dst=None)
        utc_time = local_time.astimezone(pytz.utc)

        print("UTC Time: ", utc_time)

        id = scheduleInDb(
            TaskURL, utc_time, LambdaName, LambdaDescription)

        scheduler.add_job(
            lambdaCaller,
            trigger='date',
            jobstore='default',
            args=[TaskURL, str(id), int(retries),
                  timedelta(milliseconds=timeBetweenRetries)],
            id=str(id),
            max_instances=1,
            run_date=utc_time
        )

        print("Task scheduled : url:{0} at datetime:{1}".format(
            TaskURL, json["dateTimeValue"]))

        return jsonify({"id": id})


@ app.route('/tasks/<Taskid>', methods=["DELETE"])
def cancel(Taskid):

    print("Cancel ID: ", Taskid)

    # Checking if cancelled successfully
    try:
        scheduler.get_job(Taskid, 'default')
    except:
        print("Job with id: ", Taskid, "Not found")
        return jsonify(False)

    # Checking if the Taskid is valid and can be cancelled
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
