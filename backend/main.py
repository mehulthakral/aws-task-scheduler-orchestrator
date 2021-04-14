import psycopg2
from flask import Flask, render_template, jsonify, request, abort, Response
from flask_cors import CORS
import requests
import random
import time
import string
import random
import create
import hashlib

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

backend_url = "http://127.0.0.1:5000"

conn = psycopg2.connect(
    dbname="jobs",
    user="postgres",
    password="postgres@123",
    host="localhost",
    port="5432"
)
# tableName defines the name of the table that will be updated in the postgres DB
tableName = "apscheduler_jobs"
functionTableName = "function_data"

# Tables for storing orchestrator taskset and tasks respectively
taskSetTable = "task_set"
orchestratorTasksTable = "orchestrator_tasks"

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

# Using a non blocking scheduler to ensure tasks can run parallely
scheduler = BackgroundScheduler(
    jobstores=jobstores,
    executors=executors,
    job_defaults=job_defaults,
    timezone=utc
)

app = Flask(__name__)
CORS(app, allow_headers='*', origins='*')

scheduler.start()


"""

------------------- Scheduler DB Functions---------------

"""

# Function for adding task in DB


def scheduleInDb(TaskURL, RunTime, LambdaName, LambdaDescription, Username, SchedulingType, Retries, TimeBetweenRetries):

    print("SCHEDULING IN DB: ", TaskURL, RunTime)

    id = None
    while(True):
        id = random.randint(1, 1e17)
        retrieveQuery = "SELECT * FROM " + tableName + \
        " WHERE id = '{0}'".format(id)
        cur.execute(retrieveQuery)
        fetchedTasks = cur.fetchall()
        if(len(fetchedTasks)==0):
            break

    idQuery = "INSERT INTO " + tableName + " (id,url,run_time,lambda_name,lambda_description,status,execution_time,username,scheduling_type,retries,time_between_retries)" + " VALUES('{id}','{url}','{run_time}','{lambda_name}','{lambda_description}','Scheduled',0,'{username}','{scheduling_type}','{retries}','{time_between_retries}')".format(id=id, url=TaskURL, run_time=RunTime, lambda_name=LambdaName, lambda_description=LambdaDescription, username=Username, scheduling_type=SchedulingType, retries=Retries, time_between_retries=TimeBetweenRetries)
    cur.execute(idQuery)
    Taskid = id
    conn.commit()

    print("Task scheduled with id : ", Taskid)
    return Taskid


def updateInDb(Taskid, TaskURL, RunTime, status):
    statusQuery = "UPDATE " + tableName + \
        " SET status = '{3}', url='{1}', run_time='{2}' WHERE id = {0}".format(
            Taskid, TaskURL, RunTime, status)
    cur.execute(statusQuery)
    conn.commit()


"""
    Following function updates the status of a task with given Taskid in database

"""


def setStatusInDB(Taskid, status):
    statusQuery = "UPDATE " + tableName + \
        " SET status = '{statusValue}' WHERE id = {idValue}".format(
            statusValue=status, idValue=Taskid)
    cur.execute(statusQuery)
    conn.commit()


"""
    Following function updates the time taken to excute a task of given Taskid in database

"""


def updateExecutionTimeInDB(Taskid, ExecutionTime):
    updateQuery = "UPDATE " + tableName + \
        " SET execution_time = '{timeValue}' WHERE id = {idValue}".format(
            timeValue=ExecutionTime, idValue=Taskid)
    cur.execute(updateQuery)
    conn.commit()


def addFunctionDataInDB(Taskid, code, requirements):
    insertQuery = "INSERT INTO " + functionTableName + \
        " (id, code, requirements)" + " VALUES({idValue},'{codeValue}','{requirementsValue}')".format(
            idValue=Taskid, codeValue=code, requirementsValue=requirements)
    cur.execute(insertQuery)
    conn.commit()


"""

------------------- Auth Functions---------------

"""


# Function to check if request has required fields
def check(json, l):
    for att in l:
        if att not in json:
            return False, Response(att + " attribute is required", status=400, mimetype="application/json")
    return True, ""


# Function to check if request header has correct username and password
def check_auth(headers):
    correct, res = check(headers, ['username', 'password'])

    if(correct == False):
        return correct, res

    username = headers["username"]
    password = headers["password"]
    pwd = hashlib.sha256(password.encode()).hexdigest()

    inp = {"table": "credentials", "columns": [
        "username", "password"], "where": "username='"+username+"' AND password='"+pwd+"'"}
    send = requests.post(backend_url+'/api/v1/db/read', json=inp)
    res = eval(send.content)

    if(len(res) > 0):
        return True, Response("Logged In", status=200, mimetype="application/json")
    else:
        return False, Response("Wrong username/password", status=401, mimetype="application/json")


# Function to login through UI
@app.route('/login', methods=["HEAD"])
def login():
    auth, res = check_auth(request.headers)
    return res


# Function to register a user
@app.route('/login', methods=["POST"])
def register():
    json = request.json

    correct, res = check(json, ['username', 'password'])

    if(correct == False):
        return res

    username = json["username"]
    password = json["password"]
    pwd = hashlib.sha256(password.encode()).hexdigest()

    if(len(username) == 0 or len(password) == 0):
        return Response("Empty username/password", status=400, mimetype="application/json")

    inp = {"table": "credentials", "columns": [
        "username", "password"], "where": "username='"+username+"'"}
    send = requests.post(backend_url+'/api/v1/db/read', json=inp)
    res = eval(send.content)

    if(len(res) > 0):
        return Response("Username already exists", status=400, mimetype="application/json")

    inp = {"table": "credentials", "columns": [
        "username", "password"], "data": [username, pwd], "type": "insert"}
    send = requests.post(backend_url+'/api/v1/db/write', json=inp)
    send.json()

    return Response("Registered successfully!", status=200, mimetype="application/json")


# WARNING : While testing remember that the schedule function takes schedule time in miliseconds, so provide parameters accordingly


"""

------------------- Scheduler Functions---------------

"""

# Callback Function - for scheduler tasks


def lambdaCaller(TaskURL, Taskid, retries, timeBetweenRetries):
    print("Started Invocation")
    setStatusInDB(Taskid, "Running")
    # time.sleep(50)

    startTime = datetime.now()

    f = 0
    try:
        send = requests.get(TaskURL)
    except Exception as e:
        f = 1
        print(e)

    if(f == 0):
        try:
            res = eval(send.content)
        except Exception as e:
            print(e)
            res = send.content
        print(send.status_code, res)

    if(f == 1 or send.status_code != 200 or isinstance(res, dict) and 'errorMessage' in res):
        print("Task failed")

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
            setStatusInDB(Taskid, "Failed")

    else:
        endTime = datetime.now()
        timeDiffInMS = (endTime - startTime)
        executionTime = timeDiffInMS.total_seconds() * 1000
        updateExecutionTimeInDB(Taskid, executionTime)

        print("Completed lambda: ", Taskid, TaskURL)
        setStatusInDB(Taskid, "Completed")


def functionDeploy(id, choosenOption, timeInMS, datetimeStr, retries, timeBetweenRetries, funcSrc, requirements, LambdaName, region, access_key, secret_access_key, session_token, args):
    success, res = create.deploy(
        funcSrc, requirements, LambdaName, region, access_key, secret_access_key, session_token)

    if(success == False):
        setStatusInDB(id, "DeploymentFailed")
        return Response(res, status=400, mimetype="application/json")

    print("Deployed successfully: " + res)
    if(len(args) > 0):
        for a in args:
            res += "/"+a
    TaskURL = res

    print("RETRIES: ", retries)
    print(timeBetweenRetries)

    if choosenOption == '1':

        now = datetime.now(utc)
        updateInDb(id, TaskURL, now +
                   timedelta(milliseconds=timeInMS), "Scheduled")

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

    elif choosenOption == '2':

        print("Local time: ", datetimeStr)

        # Assuming the input will always from a Indian Timezone
        # Converting to utc
        local = pytz.timezone('Asia/Kolkata')
        # Expecting format from frontend: "13 Mar 2021 07:08:38"
        datetimeStr = datetime.strptime(datetimeStr, "%d %b %Y %H:%M:%S")
        local_time = local.localize(datetimeStr, is_dst=None)
        utc_time = local_time.astimezone(pytz.utc)

        print("UTC Time: ", utc_time)

        updateInDb(id, TaskURL, utc_time, "Scheduled")

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


# Function to schedule tasks
@app.route('/tasks', methods=["POST"])
def schedule():

    auth, res = check_auth(request.headers)
    if(auth == False):
        return res

    username = request.headers["username"]

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
    timeInMS = None
    datetimeStr = None

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

    LambdaName = str(json['LambdaName']) if "LambdaName" in json and len(json["LambdaName"]) > 0 else ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=7))
    LambdaDescription = str(
        json['LambdaDescription']) if "LambdaDescription" in json else ''

    if choosenOption == '1':
        correct, res = check(json, ['timeInMS'])

        if(correct == False):
            return res

        timeInMS = int(json['timeInMS'])

    elif choosenOption == '2':
        correct, res = check(json, ['dateTimeValue'])

        if(correct == False):
            return res

        datetimeStr = json['dateTimeValue']

    else:
        return Response("Please provide correct schedulingOption", status=400, mimetype="application/json")

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

        now = datetime.now(utc)

        id = scheduleInDb(
            "", now, LambdaName, LambdaDescription, username, taskType, retries, timeBetweenRetries)
        setStatusInDB(id, "Deploying")
        addFunctionDataInDB(id, funcSrc, requirements)

        now = datetime.now(utc)

        scheduler.add_job(
            functionDeploy,
            trigger='date',
            jobstore='default',
            args=[str(id), choosenOption, timeInMS, datetimeStr, retries, timeBetweenRetries, funcSrc,
                  requirements, LambdaName, region, access_key, secret_access_key, session_token, args],
            id=str(id),
            max_instances=1,
            run_date=now + timedelta(milliseconds=1000)
        )

        return jsonify({"id": id})

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

        now = datetime.now(utc)
        id = scheduleInDb(
            TaskURL, now + timedelta(milliseconds=timeInMS), LambdaName, LambdaDescription, username, taskType, retries, timeBetweenRetries)

        # if(taskType.lower() == "function"):
        #     addFunctionDataInDB(id, funcSrc, requirements)

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
            TaskURL, utc_time, LambdaName, LambdaDescription, username, taskType, retries, timeBetweenRetries)

        # if(taskType.lower() == "function"):
        #     addFunctionDataInDB(id, funcSrc, requirements)

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


# Function to cancel scheduler tasks
@ app.route('/tasks/<Taskid>', methods=["DELETE"])
def cancel(Taskid):

    auth, res = check_auth(request.headers)
    if(auth == False):
        return res

    username = request.headers["username"]

    print("Cancel ID: ", Taskid)

    # Checking if the Taskid is valid and scheduled by the user and can be cancelled

    try:
        scheduler.get_job(Taskid, 'default')
        taskQuery = "SELECT * FROM " + tableName + \
            " WHERE id = {idValue} AND username = '{usernameValue}'".format(
                idValue=Taskid, usernameValue=username)
        cur.execute(taskQuery)
        fetchedTask = cur.fetchall()
        if(len(fetchedTask) == 0):
            raise Exception("Invalid Id to cancel")
    except:
        print("Job with id: ", Taskid, "Invalid Id to cancel")
        return Response("Not allowed to access TaskSetID "+str(Taskid), status=403, mimetype="application/json")

    # Checking if cancelled successfully
    try:
        scheduler.remove_job(Taskid)
        setStatusInDB(Taskid, "Cancelled")
        print("Cancelled task with id:{0}".format(Taskid))
        return Response("Cancelled TaskID: "+str(Taskid), status=200, mimetype="application/json")
    except Exception as err:
        print("ERROR: ", err)
        print("TaskID ", Taskid, " doesn't exist")
        return Response("Internal Error"+str(Taskid), status=500, mimetype="application/json")


# Function to check status of scheduler task
@ app.route('/tasks/<Taskid>', methods=["GET"])
def checkStatus(Taskid):

    print("TASKID:", Taskid)

    if(Taskid == -1):
        return Response("Taskid is required", status=400, mimetype="application/json")

    auth, res = check_auth(request.headers)
    if(auth == False):
        return res

    username = request.headers["username"]

    retrieveQuery = "SELECT * FROM " + tableName + \
        " WHERE id = {idValue} AND username = '{usernameValue}'".format(
            idValue=Taskid, usernameValue=username)
    cur.execute(retrieveQuery)
    try:
        task = list(cur.fetchall()[0])
    except:
        print("Failed to fetch task")
        return Response("Not allowed to access TaskSetID "+str(Taskid), status=403, mimetype="application/json")

    print("FETCHED TASK: ", task)
    # print(type(task))
    # # Iterate and append all task objects with id, url, delay which have status=status to tasks list
    if(task is not None):
        data = {
            "Taskid": task[5],
            "TaskURL": task[0],
            "Runtime": task[1],
            "Status": task[2],
            "TimeToExecute": round(task[6]),
            "ScheduleType": task[8],
            "LambdaName": task[3],
            "LambdaDescription": task[4],
            "Retries": task[9],
            "TimeBetweenRetries": task[10]
        }
        if(task[8] == "function"):
            retrieveQuery = "SELECT * FROM " + functionTableName + \
                " WHERE id = '{id}'".format(id=task[5])
            cur.execute(retrieveQuery)
            fetchedTasks = cur.fetchall()
            data["funcSrc"] = fetchedTasks[0][1]
            data["requirements"] = fetchedTasks[0][2]
        return jsonify(data)

    return Response("Not allowed to access TaskID "+str(Taskid), status=403, mimetype="application/json")


# Function to modify scheduler task
@ app.route('/tasks', methods=["PATCH"])
def modify():

    auth, res = check_auth(request.headers)
    if(auth == False):
        return res

    username = request.headers["username"]

    print("ENTERED MODIFY")

    json = request.json

    correct, res = check(json, ['Taskid', 'timeInMS'])

    if(correct == False):
        return Response("Taskid and timeInMS are required", status=400, mimetype="application/json")

    Taskid = str(json['Taskid'])
    timeInMS = int(json['timeInMS'])
    print(Taskid, timeInMS)
    # Check if task with json["id"] exists
    try:
        print("Finding Taskid", Taskid)
        scheduler.get_job(Taskid, 'default')
        print("Modifying task with id:{0}, delay:{1}".format(
            json["Taskid"], json["timeInMS"]))
        taskQuery = "SELECT * FROM " + tableName + \
            " WHERE id = {idValue} AND username = '{usernameValue}'".format(
                idValue=Taskid, usernameValue=username)
        cur.execute(taskQuery)
        fetchedTask = cur.fetchall()
        if(len(fetchedTask) == 0):
            raise Exception("Invalid Id to modify")
    except:
        # Taskid doesn't exist
        print("Invalid Taskid")
        return Response("Not allowed to access TaskID "+str(Taskid), status=403, mimetype="application/json")

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
        return Response("Rescheduled Taskid: "+str(Taskid), status=200, mimetype="application/json")
    except Exception as err:
        # Was not able to reschedule
        print("Not able to  reschedule")
        print("Error: ", err)
        setStatusInDB(Taskid, "Failed")
        return Response("Internal Error "+str(Taskid), status=500, mimetype="application/json")


# Function to retrieve all scheduler task
@ app.route('/tasks/retrieve', methods=["GET"])
def retrieveAll():

    auth, res = check_auth(request.headers)
    if(auth == False):
        return res

    username = request.headers["username"]

    retrieveQuery = "SELECT * FROM " + tableName + \
        " WHERE username = '{usernameValue}'".format(usernameValue=username)
    cur.execute(retrieveQuery)
    fetchedTasks = cur.fetchall()
    print("FETCHED\n")
    # # Iterate and append all task objects with id, url, delay which have status=status to tasks list

    tasks = []

    for task in fetchedTasks:
        data = {
            "Taskid": task[5],
            "TaskURL": task[0],
            "Runtime": task[1],
            "Status": task[2],
            "TimeToExecute": round(task[6]),
            "ScheduleType": task[8],
            "LambdaName": task[3],
            "LambdaDescription": task[4],
            "Retries": task[9],
            "TimeBetweenRetries": task[10]
        }
        if(task[8] == "function"):
            retrieveQuery = "SELECT * FROM " + functionTableName + \
                " WHERE id = '{id}'".format(id=task[5])
            cur.execute(retrieveQuery)
            fetchedTasks = cur.fetchall()
            data["funcSrc"] = fetchedTasks[0][1]
            data["requirements"] = fetchedTasks[0][2]
        tasks.append(data)

    return jsonify(tasks)


# Function to retireve scheduler tasks acc to status
@ app.route('/tasks/retrieve/<status>', methods=["GET"])
def retrieveWithStatus(status):

    auth, res = check_auth(request.headers)
    if(auth == False):
        return res

    if(status not in ["Completed", "Cancelled", "Failed", "Running", "Scheduled", "Deploying", "DeploymentFailed"]):
        return Response("Invalid Status: "+status, status=404, mimetype="application/json")

    username = request.headers["username"]

    retrieveQuery = "SELECT * FROM " + tableName + \
        " WHERE status='{fetchStatus}' AND username='{usernameValue}';".format(
            fetchStatus=status, usernameValue=username)
    cur.execute(retrieveQuery)
    fetchedTasks = cur.fetchall()
    # # Iterate and append all task objects with id, url, delay which have status=status to tasks list

    tasks = []

    for task in fetchedTasks:
        data = {
            "Taskid": task[5],
            "TaskURL": task[0],
            "Runtime": task[1],
            "TimeToExecute": round(task[6]),
            "ScheduleType": task[8],
            "LambdaName": task[3],
            "LambdaDescription": task[4],
            "Retries": task[9],
            "TimeBetweenRetries": task[10]
        }
        if(task[8] == "function"):
            retrieveQuery = "SELECT * FROM " + functionTableName + \
                " WHERE id = '{id}'".format(id=task[5])
            cur.execute(retrieveQuery)
            fetchedTasks = cur.fetchall()
            data["funcSrc"] = fetchedTasks[0][1]
            data["requirements"] = fetchedTasks[0][2]
        tasks.append(data)

    return jsonify(tasks)


"""

------------------- Orchestrator Functions---------------

"""

# Orchestrator Callback Function


def orchestratorCaller(taskset_id, num, total, type, url, conditionCheckUrl="", conditionCheckDelay=0, conditionCheckRetries=0, delayBetweenRetries=0, fallbackUrl=""):

    if type == "task":

        if(num == 1):
            inp = {"table": taskSetTable, "columns": ["status"], "data": [
                "Running"], "where": "id="+str(taskset_id), "type": "update"}
            send = requests.post(backend_url+'/api/v1/db/write', json=inp)
            send.json()

            inp = {"table": orchestratorTasksTable, "columns": ["url", "condition_check_url", "condition_check_delay",
                                                                "condition_check_retries", "delay_between_retries", "fallback_url"], "where": "id="+str(taskset_id)+" AND num="+"1"}
            send = requests.post(backend_url+'/api/v1/db/read', json=inp)
            res = eval(send.content)

            if(len(res) > 0):
                url = res[0][0]
                conditionCheckUrl = res[0][1]
                conditionCheckDelay = res[0][2]
                conditionCheckRetries = res[0][3]
                delayBetweenRetries = res[0][4]
                fallbackUrl = res[0][5]
            else:
                print("ERROR: No entry for first task in db")
                return

        send = requests.get(url)
        try:
            res = eval(send.content)
        except Exception as e:
            print(e)
            res = send.content
        print(send.status_code, res)
        if(send.status_code != 200 or isinstance(res, dict) and 'errorMessage' in res):
            print("Taskset {0} num {1} failed".format(taskset_id, num))

        now = datetime.now(utc)
        scheduler.add_job(
            orchestratorCaller,
            trigger='date',
            jobstore='default',
            args=[taskset_id, num, total, "condition", "", conditionCheckUrl,
                  conditionCheckDelay, conditionCheckRetries,
                  delayBetweenRetries, fallbackUrl],
            id=str(taskset_id)+";"+str(num)+";"+str(conditionCheckRetries),
            max_instances=1,
            run_date=now + timedelta(milliseconds=conditionCheckDelay)
        )

    elif type == "condition":

        send = requests.get(conditionCheckUrl)
        try:
            res = eval(send.content)
        except Exception as e:
            print(e)
            res = send.content
        print(send.status_code, res)
        if(send.status_code != 200 or isinstance(res, dict) and 'errorMessage' in res):
            print("Condition Check failed {0} num {1} failed".format(
                taskset_id, num))

            if conditionCheckRetries is not None and conditionCheckRetries > 0:
                print("RETRYING", taskset_id, num,
                      " RETRY LEFT: ", conditionCheckRetries)
                now = datetime.now(utc)
                scheduler.add_job(
                    orchestratorCaller,
                    trigger='date',
                    jobstore='default',
                    args=[taskset_id, num, total, "condition", url, conditionCheckUrl,
                          conditionCheckDelay, conditionCheckRetries-1,
                          delayBetweenRetries, fallbackUrl],
                    id=str(taskset_id)+";"+str(num) +
                    ";"+str(conditionCheckRetries),
                    max_instances=1,
                    run_date=now + timedelta(milliseconds=delayBetweenRetries)
                )

            else:
                print("Retries ended", taskset_id, num,
                      " RETRY LEFT: ", conditionCheckRetries)
                # call fallback
                orchestratorCaller(taskset_id, num, total, "fallback", url, conditionCheckUrl,
                                   conditionCheckDelay, conditionCheckRetries,                   delayBetweenRetries, fallbackUrl)

        else:
            if(num == total):
                inp = {"table": taskSetTable, "columns": ["status"], "data": [
                    "Completed"], "where": "id="+str(taskset_id), "type": "update"}
                send = requests.post(backend_url+'/api/v1/db/write', json=inp)
                send.json()
            else:
                # call next
                inp = {"table": orchestratorTasksTable, "columns": ["url", "condition_check_url", "condition_check_delay",
                                                                    "condition_check_retries", "delay_between_retries", "fallback_url"], "where": "id="+str(taskset_id)+" AND num="+str(num+1)}
                send = requests.post(backend_url+'/api/v1/db/read', json=inp)
                res = eval(send.content)

                if(len(res) > 0):
                    url = res[0][0]
                    conditionCheckUrl = res[0][1]
                    conditionCheckDelay = res[0][2]
                    conditionCheckRetries = res[0][3]
                    delayBetweenRetries = res[0][4]
                    fallbackUrl = res[0][5]
                else:
                    print("ERROR: No entry for {} task in db".format(num+1))
                    return

                orchestratorCaller(taskset_id, num+1, total, "task", url, conditionCheckUrl,
                                   conditionCheckDelay, conditionCheckRetries,                   delayBetweenRetries, fallbackUrl)

    else:  # for fallback
        print("Fallback called {0} num {1}".format(taskset_id, num))
        send = requests.get(fallbackUrl)
        try:
            res = eval(send.content)
        except Exception as e:
            print(e)
            res = send.content
        print(send.status_code, res)
        if(send.status_code != 200 or isinstance(res, dict) and 'errorMessage' in res):
            print("Fallback failed {0} num {1} failed".format(taskset_id, num))

        inp = {"table": taskSetTable, "columns": ["status"], "data": [
            "Failed"], "where": "id="+str(taskset_id), "type": "update"}
        send = requests.post(backend_url+'/api/v1/db/write', json=inp)
        send.json()


# Function to orchestrate taskset
@app.route('/taskset', methods=["POST"])
def orchestrate():

    print("REQUEST: ", request.json)

    auth, res = check_auth(request.headers)
    if(auth == False):
        return res

    username = request.headers["username"]

    json = request.json

    correct, res = check(json, ['initialDelay', 'tasks'])

    if(correct == False):
        return res

    initialDelay = int(json["initialDelay"])
    tasks = json["tasks"]

    if(len(tasks) < 2):
        return Response("Please provide atleast 2 tasks", status=400, mimetype="application/json")

    idQuery = "INSERT INTO " + taskSetTable + \
        " (status,username, initial_delay)" + \
        " VALUES('Scheduled','{0}',{1})".format(
            username, initialDelay) + " RETURNING id;"
    cur.execute(idQuery)
    id = cur.fetchone()[0]
    conn.commit()

    print("ID ASSIGNED: ", id)

    num = 0
    for task in tasks:
        num += 1
        correct, res = check(task, ["taskURL", "conditionCheckTaskURL",
                                    "timeDelayForConditionCheck", "conditionCheckRetries",
                                    "timeDelayBetweenRetries", "fallbackTaskURL"])

        if(correct == False):
            return res

        inp = {"table": orchestratorTasksTable, "columns": ["id", "num", "url", "condition_check_url", "condition_check_delay", "condition_check_retries", "delay_between_retries", "fallback_url"], "data": [str(id), str(num), task["taskURL"], task["conditionCheckTaskURL"],
                                                                                                                                                                                                              str(task["timeDelayForConditionCheck"]), str(
                                                                                                                                                                                                                  task["conditionCheckRetries"]),
                                                                                                                                                                                                              str(task["timeDelayBetweenRetries"]), task["fallbackTaskURL"]], "type": "insert"}
        send = requests.post(backend_url+'/api/v1/db/write', json=inp)
        send.json()

    now = datetime.now(utc)

    task = tasks[0]

    scheduler.add_job(
        orchestratorCaller,
        trigger='date',
        jobstore='default',
        args=[id, 1, num, "task", task["taskURL"], task["conditionCheckTaskURL"],
              task["timeDelayForConditionCheck"], task["conditionCheckRetries"],
                task["timeDelayBetweenRetries"], task["fallbackTaskURL"]],
        id=str(id)+";"+"1",
        max_instances=1,
        run_date=now + timedelta(milliseconds=initialDelay)
    )

    print("ORCHESTRATION ADDED")

    return jsonify({"id": id})


# Function to check authenticate user to access particular taskset
def check_task_auth(id, username):
    inp = {"table": "task_set", "columns": [
        "id", "username", "status"], "where": "id="+str(id)+" AND username='"+username+"'"}
    send = requests.post(backend_url+'/api/v1/db/read', json=inp)
    res = eval(send.content)

    if(len(res) > 0 and res[0][2] == "Scheduled"):
        return True, Response("Allowed", status=200, mimetype="application/json")
    elif(len(res) == 0):
        return False, Response("Not allowed to access TaskSetID "+str(id), status=403, mimetype="application/json")
    else:
        return False, Response("Orchestration has already started for TaskSetID "+str(id), status=400, mimetype="application/json")


# Function to modify taskset
@ app.route('/taskset', methods=["PATCH"])
def modify_taskset():

    auth, res = check_auth(request.headers)
    if(auth == False):
        return res

    username = request.headers["username"]

    print("ENTERED MODIFY")

    json = request.json

    correct, res = check(json, ['id', 'initialDelay', 'tasks'])

    if(correct == False):
        return res

    id = json['id']
    initialDelay = json['initialDelay']
    tasks = json['tasks']

    auth, res = check_task_auth(id, username)
    if(auth == False):
        return res

    if(len(tasks) < 2):
        return Response("Please provide atleast 2 tasks", status=400, mimetype="application/json")

    Taskid = str(id)+";"+"1"

    # Check if task with json["id"] exists
    try:
        print("Finding id", Taskid)
        scheduler.get_job(Taskid, 'default')
        print("Modifying task with id:{0}".format(
            Taskid))
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
            run_date=now + timedelta(milliseconds=int(initialDelay))
        )

    except Exception as err:
        # Was not able to reschedule
        print("Not able to  reschedule")
        print("Error: ", err)
        return jsonify(False)

    inp = {"table": orchestratorTasksTable, "columns": [],
           "data": [], "where": "id="+str(id), "type": "delete"}
    send = requests.post(backend_url+'/api/v1/db/write', json=inp)
    send.json()

    num = 0
    for task in tasks:
        num += 1
        correct, res = check(task, ["taskURL", "conditionCheckTaskURL",
                                    "timeDelayForConditionCheck", "conditionCheckRetries",
                                    "timeDelayBetweenRetries", "fallbackTaskURL"])

        if(correct == False):
            return res

        inp = {"table": orchestratorTasksTable, "columns": ["id", "num", "url", "condition_check_url", "condition_check_delay", "condition_check_retries", "delay_between_retries", "fallback_url"], "data": [str(id), str(num), task["taskURL"], task["conditionCheckTaskURL"],
                                                                                                                                                                                                              str(task["timeDelayForConditionCheck"]), str(
                                                                                                                                                                                                                  task["conditionCheckRetries"]),
                                                                                                                                                                                                              str(task["timeDelayBetweenRetries"]), task["fallbackTaskURL"]], "type": "insert"}
        send = requests.post(backend_url+'/api/v1/db/write', json=inp)
        send.json()

    inp = {"table": taskSetTable, "columns": ["initial_delay"], "data": [
        str(initialDelay)], "where": "id="+str(id), "type": "update"}
    send = requests.post(backend_url+'/api/v1/db/write', json=inp)
    send.json()

    print("Taskid ", Taskid, " rescheduled")
    return jsonify(True)

# Function to cancel taskset


@ app.route('/taskset/<id>', methods=["DELETE"])
def cancel_taskset(id):

    auth, res = check_auth(request.headers)
    if(auth == False):
        return res

    username = request.headers["username"]

    id = int(id)

    auth, res = check_task_auth(id, username)
    if(auth == False):
        return res

    Taskid = str(id)+";"+"1"

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
    except Exception as err:
        print("ERROR: ", err)
        print("TaskID ", Taskid, " doesn't exist")
        return jsonify(False)

    inp = {"table": taskSetTable, "columns": ["status"], "data": [
        "Cancelled"], "where": "id="+str(id), "type": "update"}
    send = requests.post(backend_url+'/api/v1/db/write', json=inp)
    send.json()
    print("Cancelled task with id:{0}".format(id))
    return jsonify(True)


# Function to retrieve all taskset
@ app.route('/taskset/retrieve', methods=["GET"])
def retrieveAll_taskset():

    auth, res = check_auth(request.headers)
    if(auth == False):
        return res

    username = request.headers["username"]

    inp = {"table": taskSetTable, "columns": [
        "id", "status", "initial_delay"], "where": "username='"+username+"'"}
    send = requests.post(backend_url+'/api/v1/db/read', json=inp)
    res = eval(send.content)

    final = []
    for task_set in res:
        ans = {}
        ans["id"] = task_set[0]
        ans["status"] = task_set[1]
        ans["initialDelay"] = task_set[2]

        inp = {"table": orchestratorTasksTable, "columns": ["url", "condition_check_url", "condition_check_delay",
                                                            "condition_check_retries", "delay_between_retries", "fallback_url"], "where": "id="+str(ans["id"])}
        send = requests.post(backend_url+'/api/v1/db/read', json=inp)
        fetchedTasks = eval(send.content)

        tasks = []

        for task in fetchedTasks:
            tasks.append({
                "taskURL": task[0],
                "conditionCheckTaskURL": task[1],
                "timeDelayForConditionCheck": task[2],
                "conditionCheckRetries": task[3],
                "timeDelayBetweenRetries": task[4],
                "fallbackTaskURL": task[5]
            })

        ans["tasks"] = tasks
        final.append(ans)

    return jsonify(final)


# Function to retireve taskset acc to status
@ app.route('/taskset/retrieve/<status>', methods=["GET"])
def retrieveWithStatus_taskset(status):

    auth, res = check_auth(request.headers)
    if(auth == False):
        return res

    username = request.headers["username"]

    inp = {"table": taskSetTable, "columns": [
        "id", "initial_delay"], "where": "username='"+username+"' AND status='"+status+"'"}
    send = requests.post(backend_url+'/api/v1/db/read', json=inp)
    res = eval(send.content)

    final = []
    for task_set in res:
        ans = {}
        ans["id"] = task_set[0]
        ans["initialDelay"] = task_set[1]

        inp = {"table": orchestratorTasksTable, "columns": ["url", "condition_check_url", "condition_check_delay",
                                                            "condition_check_retries", "delay_between_retries", "fallback_url"], "where": "id="+str(ans["id"])}
        send = requests.post(backend_url+'/api/v1/db/read', json=inp)
        fetchedTasks = eval(send.content)

        tasks = []

        for task in fetchedTasks:
            tasks.append({
                "taskURL": task[0],
                "conditionCheckTaskURL": task[1],
                "timeDelayForConditionCheck": task[2],
                "conditionCheckRetries": task[3],
                "timeDelayBetweenRetries": task[4],
                "fallbackTaskURL": task[5]
            })

        ans["tasks"] = tasks
        final.append(ans)

    return jsonify(final)


"""

------------------- Orchestrator DB Functions---------------

"""

# Endpoint to make changes to db - insert, update, delete


@app.route('/api/v1/db/write', methods=["POST"])
def write_db():

    json = request.get_json()
    # db = pymysql.connect(host="db_xmeme", user="root", password="123", db="xmeme", port=3306)
    # cur = db.cursor()

    if(json["type"] == "insert"):

        columns = json["columns"][0]
        data = "'"+json["data"][0]+"'"

        for iter in range(1, len(json["columns"])):
            columns = columns + "," + json["columns"][iter]
            data = data + ",'" + json["data"][iter]+"'"

        sql = "INSERT INTO "+json["table"]+"("+columns+") VALUES ("+data+")"

    elif(json["type"] == "delete"):

        if json["where"] != "":
            sql = "DELETE FROM "+json["table"]+" WHERE "+json["where"]
        else:
            sql = "DELETE FROM "+json["table"]

    elif(json["type"] == "update"):

        string = json["columns"][0] + "='" + json["data"][0] + "'"

        for iter in range(1, len(json["columns"])):
            string = string + ", " + \
                json["columns"][iter] + "='" + json["data"][iter] + "'"

        sql = "UPDATE "+json["table"]+" SET " + \
            string + " WHERE " + json["where"]

    cur.execute(sql)
    conn.commit()
    # cur.close()

    return Response("1", status=200, mimetype="application/text")

# Endpoint to read data from the db


@app.route('/api/v1/db/read', methods=["POST"])
def read_db():

    json = request.get_json()
    # db = pymysql.connect(host="db_xmeme", user="root", password="123", db="xmeme", port=3306)
    # cur = db.cursor()

    columns = json["columns"][0]
    for iter in range(1, len(json["columns"])):
        columns = columns + "," + json["columns"][iter]

    if json["where"] != "":
        sql = "SELECT "+columns+" FROM "+json["table"]+" WHERE "+json["where"]
    else:
        sql = "SELECT "+columns+" FROM "+json["table"]

    if "orderBy" in json:
        sql = sql + " ORDER BY " + json["orderBy"]

    cur.execute(sql)
    results = cur.fetchall()
    results = list(map(list, results))
    # cur.close()

    return Response(str(results), status=200, mimetype="application/text")


if __name__ == '__main__':
    app.debug = False
    app.run()
