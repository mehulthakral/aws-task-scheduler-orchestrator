import React, { useState } from 'react';
import {Box,Button,Card,Clock as Timer,CardBody,DropButton,Grommet,Nav,RoutedAnchor,Sidebar,Select,Text,TextInput,Spinner,Tip } from 'grommet';
import {Add,Action,Archive,CircleInformation,Clock,Compliance,Domain,Edit,History,Home as HomeIcon,Install,Key,Lock,Link as URL,MapLocation,Notes,Revert,Run,SchedulePlay,Search,Task,Tasks,TextAlignFull,Trash,Logout,UserAdmin,Waypoint} from 'grommet-icons';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Modal from 'react-modal';


import * as Yup from "yup";
import { ErrorMessage, Field, FieldArray, Form, Formik } from "formik";


import {
  BrowserRouter as Router,
  Switch,
  Redirect,
  Route,
  Link,
} from "react-router-dom";
import Async from 'react-async';


const axios = require('axios');

let backend_url = "http://localhost:5000";

Modal.setAppElement('#root');
const customStyles = {
  content : {
    top                   : '50%',
    left                  : '50%',
    right                 : 'auto',
    bottom                : 'auto',
    marginRight           : '-50%',
    transform             : 'translate(-50%, -50%)'
  }
};

const theme = {
  global: {
    font: {
      family: 'Roboto',
      size: '18px',
      height: '20px',
    }
  },
};

function LogoutUser()
{
  if(sessionStorage.getItem('username') === null)
    {
        toast.error("Sign In first")
        return;
    }

  sessionStorage.clear();
  toast.success("User Logged Out")
  console.log("User logout")
}

function Navbar() 
  {    
      return <Router>
      <div style={{position : 'fixed'}}>
      <Sidebar background="#FF9900"
      header={
        <Link to="/home"><Button icon={<HomeIcon color='plain'/>} hoverIndicator/></Link>
      }
      footer={
        <Link to="/about"><Button icon={<CircleInformation color='plain'/>} hoverIndicator/></Link>
      }
      elevation="xlarge"
      height="100vh"
      round = "false"
      gap="small"
      position = "fixed"

    >
      <Nav gap="small">
        <Link to="/addTask"><Button icon={<Add color='plain'/>} hoverIndicator/></Link>
        <Link to="/allTasks"><Button icon={<Tasks color='plain' /> } hoverIndicator/></Link>
        <Link to="/orchestrator"><Button icon={<Action color='plain' /> } hoverIndicator/></Link>
        <Link to="/retrieveOrchestratorTasks"><Button icon={<Task color='plain' /> } hoverIndicator/></Link>
        <a href="documentation.html" target="_blank"><Button icon={<Notes color='plain'/>} hoverIndicator/></a>
        <Button icon={<Logout color='plain' onClick={() => LogoutUser()}/> } hoverIndicator/>
      </Nav>
    </Sidebar>
    </div>
    <Switch>
          <Route path="/home">
            <Home /> 
          </Route>
          <Route path="/addTask">
            <AddTask />
          </Route>
          <Route path="/allTasks">
            <RetrieveTasks />
          </Route>
          <Route path="/orchestrator">
            <Orchestrator />  
          </Route>
           <Route path="/retrieveOrchestratorTasks">
            <OrchestratorTasks />  
          </Route>
          <Route path="/about">
            <About />  
          </Route>
        </Switch>

    </Router>
  }

async function DoSignIn(username, password)
{
   console.log("Logging In")
   await axios({
        method : 'head',
        url : backend_url + '/login',
        headers: {
          username: username,
          password: password
        }
      })
      .catch((err) => console.log(err))
      .then((response) => {
        
        console.log("RESPONSE:",response)

        if(response === undefined)
        {
          console.log("Not able to Login")
          toast.error("Incorrect credentials", {
              position: toast.POSITION.TOP_RIGHT
            });
          return
        }
        if(response.status === 200)
          {
            console.log(response)
            console.log("Login Successful");
            sessionStorage.setItem('username',username)
            sessionStorage.setItem('password',password)
              toast.success("Login Successful", {
              position: toast.POSITION.TOP_RIGHT
              });
            return <Redirect to="/home" />
          }
        else
          console.log("Not able to Login")
          toast.warn("Incorrect credentials", {
              position: toast.POSITION.TOP_RIGHT
            });
      })
}

async function DoSignUp(username, password)
{
   console.log("Signning Up")
   await axios({
        method : 'post',
        url : backend_url + '/login',
        data: {
          "username": username,
          "password": password
        }
      }).then((response) => {
        
        if(response === undefined)
        {
          console.log("Not able to Signup")
          toast.error("Not able to Signup")
          return
        }

        if(response.status === 200)
          {
            console.log(response)
            console.log("Signup Successful, please login");
            toast.success("Signup Successful")
            return <Redirect to="/home" />
          }
        
      }) 
}

function Home()
{
  
 const [username, setUsername] = React.useState('');
 const [password, setPassword] = React.useState('');

 if(sessionStorage.getItem('username') !== null)
 {
   return <Box margin="xlarge">User: {sessionStorage.getItem('username')} is already logged in.</Box>
 }

  return (
    <Box 
    alignSelf="center" 
    alignContent="center"
    justify = "center"
    align="center"
    direction="column"
    width="50vw"
    height="100vh"
    elevation="large"
    margin={{"left" : "large"}}
    pad={{"left" : "large"}}
    gap="small"
    border="all"
    >
  <Box direction="column" align="center" >
  <h1>Sign In/Sign up</h1>
  <h2>AWS T4</h2>
  </Box>
      <Box width="30vw" gap="small" >
      <TextInput
        placeholder="Enter username"
        value={username}
        onChange={event => setUsername(event.target.value)}
        alignSelf="center" 
        alignContent="center"
        justify = "center"
        align="center"
        width="50vw"
        background="white"
      />
      <TextInput
        placeholder="Enter password"
        value={password}
        onChange={event => setPassword(event.target.value)}
        type="password"
        width="50vw"
        pad="large"
        justify="center"
        background="white"
      />
      </Box>
      <Box direction="row" gap="small" margin="medium">
      <Button primary label="SignIn" alignSelf="center" color="#232f3e" onClick={() => DoSignIn(username,password)}/>
      <Button primary label="SignUp" alignSelf="center" color="#232f3e" onClick={() => DoSignUp(username,password)}/>
      </Box>
    </Box>
  );
  
}

function AddTask()
{

  const [LambdaName, setLambdaName] = React.useState('');
  const [LambdaDescription, setLambdaDescription] = React.useState('');
  const [Retries, setRetries] = React.useState('');
  const [RetryGap, setRetryGap]  = React.useState('');
  const [SchedulingType, setSchedulingType] = React.useState('Based on Time Delay in miliseconds');
  const [DelayValue, setDelayValue] = React.useState('');
  const [TaskType, setTaskType] = React.useState('Based on URL');

  const margin = {
   "left" : "xlarge"
    }
  let username = sessionStorage.getItem('username')
  if(username === null)
  {
      return <Box margin="xlarge">Please login before accessing this section</Box>
  }

  return <Box direction="column" margin={margin} alignSelf="center" width="50%" gap="small">
        <Box direction="row" alignSelf="center" justify="center">
          <h1>Task Scheduler</h1> 
          <Box pad="medium">
            <Timer type="digital" />
          </Box>
        </Box>
    <TextInput
      icon = {<Domain/>}
      placeholder="Enter Name of Lambda function"
      LambdaName={LambdaName}
      onChange={event => setLambdaName(event.target.value)}
    />
    <TextInput
      icon = {<TextAlignFull/>}
      placeholder="Enter Description about Lambda function"
      LambdaDescription={LambdaDescription}
      onChange={event => setLambdaDescription(event.target.value)}
    />

     <TextInput
      icon = {<Revert/>}
      placeholder="Enter no. of retries if Lambda fails"
      Retries={Retries}
      onChange={event => setRetries(event.target.value)}
    />
    

     <TextInput
      icon = {<History/>}
      placeholder="Duration between retries in milliseconds"
      RetryGap={RetryGap}
      onChange={event => setRetryGap(event.target.value)}
    />

    
    <Select
      defaultValue = 'Based on Time Delay in miliseconds'
      options={['Based on Time Delay in miliseconds', 'Based on Date and Time in future, Ex:"28 Mar 2021 23:05:00"']}
      SchedulingType={SchedulingType}
      alignSelf = "stretch"
      onChange={({ option }) => 
      {
        setSchedulingType(option)
        console.log("SCHEDULING TYPE: ", option)
      }}
    />

    <TextInput
      icon = {<Clock/>}
      DelayValue={DelayValue}
      onChange={event => setDelayValue(event.target.value)}
    />

    <Select
      defaultValue = 'Based on URL'
      options={['Based on URL', 'Based on Function']}
      TaskType={TaskType}
      alignSelf = "stretch"
      onChange={({ option }) => 
      {
        setTaskType(option)
        console.log("TASK TYPE: ", option)
      }}
    />

    <UrlOptions 
    LambdaName = {LambdaName} 
    LambdaDescription = {LambdaDescription}
    TaskType = {TaskType}
    Retries = {Retries}
    RetryGap = {RetryGap}
    SchedulingType = {SchedulingType}
    DelayValue = {DelayValue}
    />

    
    <FunctionOptions 
    LambdaName={LambdaName}
    LambdaDescription = {LambdaDescription}
    TaskType={TaskType}
    Retries={Retries}
    RetryGap={RetryGap}
    SchedulingType = {SchedulingType}
    DelayValue = {DelayValue}
    />

    
  </Box>
}

function UrlOptions({LambdaName,
      LambdaDescription,
      TaskType,
      Retries,
      RetryGap,
      SchedulingType,
      DelayValue})
{
  const [TaskURL, setTaskURL] = React.useState('');

    if(TaskType === "Based on URL")
    {
      return <Box>
      <TextInput
      icon = {<URL/>}
      placeholder="Enter URL of Lambda function"
      TaskURL={TaskURL}
      onChange={event => setTaskURL(event.target.value)}
      />
      <Button 
        primary 
        label="Schedule Task" 
        icon = {<SchedulePlay/>}
        color = "#146eb4"
        margin = "small"
        alignSelf = "center"
        onClick = {() => ScheduleUrlTask(
          LambdaName,
          LambdaDescription,
          TaskURL,
          Retries,
          RetryGap,
          SchedulingType,
          DelayValue
          )}
      />
      </Box>
    }

    return null
}

async function ScheduleUrlTask(LambdaName,
      LambdaDescription,
      TaskURL,
      Retries,
      RetryGap,
      SchedulingType,
      DelayValue)
{ 
  console.log(LambdaName,
      LambdaDescription,
      TaskURL,
      Retries,
      RetryGap, "TYPE: ",
      SchedulingType, "DELAY: ",
      DelayValue)

      
  if(SchedulingType === 'Based on Time Delay in miliseconds')
  {
      await axios({
        method : 'post',
        url : 'http://localhost:5000/tasks',
        headers: {
        username: sessionStorage.getItem('username'),
        password: sessionStorage.getItem('password')
        },
        data : {
        "LambdaName" : LambdaName,
        "LambdaDescription" : LambdaDescription,
        "TaskURL" : TaskURL,
        "retries" : Retries,
        "timeBetweenRetries" : RetryGap,
        "schedulingOption" : "1",
        "timeInMS" : DelayValue,
        "taskType" : "url"
        }
      }).then((response) => toast.info("Task scheduled with id: " + response.data.id, {
              position: toast.POSITION.TOP_RIGHT
              })) 
    }
  else if(SchedulingType === 'Based on Date and Time in future, Ex:"28 Mar 2021 23:05:00"')
      await axios({
        method : 'post',
        url : 'http://localhost:5000/tasks',
        headers: {
        username: sessionStorage.getItem('username'),
        password: sessionStorage.getItem('password')
        },
        data : {
        "LambdaName" : LambdaName,
        "LambdaDescription" : LambdaDescription,
        "TaskURL" : TaskURL,
        "retries" : Retries,
        "timeBetweenRetries" : RetryGap,
        "schedulingOption" : "2",
        "dateTimeValue" : DelayValue,
        "taskType" : "url"
        }
      }).then((response) => toast.info("Task scheduled with id: " + response.data.id, {
              position: toast.POSITION.TOP_RIGHT
              })) 

  console.log("Tried to schedule")
}


function FunctionOptions({LambdaName,LambdaDescription,TaskType,Retries,RetryGap,SchedulingType,DelayValue})
{
  
  const [FunctionSourceString, setFunctionSourceString] = React.useState('');
  const [Arguments, setArguments] = React.useState('');
  const [Requirements, setRequirements] = React.useState('');
  const [Region, setRegion] = React.useState('');
  const [AccesskeyValue, setAccesskeyValue] = React.useState('');
  const [SecretAccesskey, setSecretAccesskey] = React.useState('');
  const [SessionToken, setSessionToken] = React.useState('');

  if(TaskType === "Based on Function")
    {
        return <Box gap="small">
          
          <TextInput
            icon = {<Run/>}
            placeholder="Enter function source string"
            FunctionSourceString={FunctionSourceString}
            onChange={event => setFunctionSourceString(event.target.value)}
          />

          <TextInput
            icon = {<Waypoint/>}
            placeholder="Enter comma separated arguments"
            Arguments={Arguments}
            onChange={event => setArguments(event.target.value)}
          />

          <TextInput
            icon = {<Compliance/>}
            placeholder="Enter requirements string"
            Requirements={Requirements}
            onChange={event => setRequirements(event.target.value)}
          />

          <TextInput
            icon = {<MapLocation/>}
            placeholder="Enter region"
            Region={Region}
            onChange={event => setRegion(event.target.value)}
          />

          <TextInput
            icon = {<Key/>}
            placeholder="Enter Access Key"
            AccesskeyValue={AccesskeyValue}
            onChange={event => setAccesskeyValue(event.target.value)}
          />

          <TextInput
            icon = {<UserAdmin/>}
            placeholder="Enter Secret Access Key"
            SecretAccesskey={SecretAccesskey}
            onChange={event => setSecretAccesskey(event.target.value)}
          />

          <TextInput
            icon = {<Lock/>}
            placeholder="Enter Session Token"
            SessionToken={SessionToken}
            onChange={event => setSessionToken(event.target.value)}
          />

          <Button 
            primary 
            label="Deploy Function" 
            icon = {<Install/>}
            color = "#146eb4"
            margin = "small"
            alignSelf = "center"
            onClick = {() => 
              ScheduleFunctionTask(
                LambdaName,
                LambdaDescription,
                FunctionSourceString,
                Arguments,
                Requirements,
                Region,
                AccesskeyValue,
                SecretAccesskey,
                SessionToken,
                Retries,
                RetryGap,
                SchedulingType,
                DelayValue)}
          />

        </Box>
    }

    return null
    
}

async function ScheduleFunctionTask(
      LambdaName,
      LambdaDescription,
      FunctionSourceString,
      Arguments,
      Requirements,
      Region,
      AccesskeyValue,
      SecretAccesskey,
      SessionToken,
      Retries,
      RetryGap,
      SchedulingType,
      DelayValue)
{ 
  console.log(LambdaName,
      LambdaDescription,
      FunctionSourceString,
      Retries,
      RetryGap, "TYPE: ",
      SchedulingType, "DELAY: ",
      DelayValue)

      if(Arguments !== undefined)
      {
        Arguments = Arguments.split(',')
        Arguments.map(Argument => Argument.trim())
      }

  if(SchedulingType === 'Based on Time Delay in miliseconds')
  {
      await axios({
        method : 'post',
        url : 'http://localhost:5000/tasks',
        headers: {
        username: sessionStorage.getItem('username'),
        password: sessionStorage.getItem('password')
        },
        data : {
        "LambdaName" : LambdaName,
        "LambdaDescription" : LambdaDescription,
        "funcSrc" : FunctionSourceString,
        "args" : Arguments,
        "requirements" : Requirements,
        "region" : Region,
        "access_key" : AccesskeyValue,
        "secret_access_key" : SecretAccesskey,
        "session_token" : SessionToken,
        "retries" : Retries,
        "timeBetweenRetries" : RetryGap,
        "schedulingOption" : "1",
        "dateTimeValue" : DelayValue,
        "taskType" : "function"
        }
      }).then((response) => toast.info("Task scheduled with id: " + response.data.id, {
              position: toast.POSITION.TOP_RIGHT
              })) 
    }
  else if(SchedulingType === 'Based on Date and Time in future, Ex:"28 Mar 2021 23:05:00"')
      await axios({
        method : 'post',
        url : 'http://localhost:5000/tasks',
        headers: {
        username: sessionStorage.getItem('username'),
        password: sessionStorage.getItem('password')
        },
        data : {
        "LambdaName" : LambdaName,
        "LambdaDescription" : LambdaDescription,
        "funcSrc" : FunctionSourceString,
        "args" : Arguments,
        "requirements" : Requirements,
        "region" : Region,
        "access_key" : AccesskeyValue,
        "secret_access_key" : SecretAccesskey,
        "session_token" : SessionToken,
        "retries" : Retries,
        "timeBetweenRetries" : RetryGap,
        "schedulingOption" : "2",
        "timeInMS" : DelayValue,
        "taskType" : "function"
        }
      }).then((response) => toast.info("Task scheduled with id: " + response.data.id, {
              position: toast.POSITION.TOP_RIGHT
              })) 

  console.log("Tried to schedule")
}



const loadTasks = () =>
  fetch("http://localhost:5000/tasks/retrieve", {
  method: 'GET',
  headers: {
    'username': sessionStorage.getItem('username'),
    'password': sessionStorage.getItem('password')
    },
  })
    .then(res => (res.ok ? res : Promise.reject(res)))
    .then(res => res.json())

function compare(a,b)
{
  if(a.Taskid > b.Taskid)
    return -1;
  return 1;
}

async function modifyTask(taskid, timedelay)
{
  await axios({
        method : 'PATCH',
        url : backend_url + '/tasks',
        headers: {
          username: sessionStorage.getItem('username'),
          password: sessionStorage.getItem('password')
        },
        data : {
        "Taskid" : taskid,
        "timeInMS" : timedelay,
        }
      }).then((res) =>toast.info(res.data))
}

async function cancelTask(Taskid)
{
  console.log("Trying to cancel")
  await axios({
        method : 'DELETE',
        url : backend_url + '/tasks/' + Taskid,
        headers: {
          username: sessionStorage.getItem('username'),
          password: sessionStorage.getItem('password')
        }
      }).then((res) => toast.info(res.data))
}


async function retriveTasksWithStatus(Taskid, set)
{
   await axios({
        method : 'GET',
        url : backend_url + '/tasks/retrieve/' + Taskid,
        headers: {
          username: sessionStorage.getItem('username'),
          password: sessionStorage.getItem('password')
        }
      }).then((res) => console.log(res))
}

const retriveSingleTaskDetails = async ({TaskID}) => {
      console.log("FETCHING:", backend_url + '/tasks/' + TaskID)
      let res = await fetch(backend_url + '/tasks/' + TaskID,{
        method : 'GET',
        headers: {
          username: sessionStorage.getItem('username'),
          password: sessionStorage.getItem('password')
        }
      })
      console.log("RESPONSE", res)

      if(res.status !== 200)
      return {"status" : res.status}

      return res.json()
      
    }

function TaskDetails({TaskID,ButtonClicked})
{
    let colours = {
    "Completed" : "#7cd992",
    "Cancelled" : "#a8a8a8",
    "Failed" : "#eb6060",
    "Running" : "#f7e463",
    "Scheduled" : "#87dfe9"
  }

  console.log("Entered Task Details: ", TaskID)
  console.log("Button Clicked: ",ButtonClicked)

  let [timeDelay, setTimeDelay] = React.useState('');

  if(TaskID === undefined || !ButtonClicked)
        return null;

  console.log("Rendering")  

    return <Box direction="column">
    <Async promiseFn={retriveSingleTaskDetails} TaskID={TaskID}>
      {({data, err, isLoading}) => {
        console.log("Trying to fetch")
        if(isLoading)
          return <Spinner size="large" color="#146eb4" margin="xlarge" align="start"/>
        if (err)
        {
          console.log(err)
          return <h1>Unable to fetch this taskid</h1>
        }
        if(data)
        {
            console.log("FETCHED TASK: ", data)
           if(data.status && data.status !== 200)
            return <h3>TaskID is not accessible</h3>
           return <Box direction="column" margin="small" gap="small">
          {
              <Card key={data.taskid} pad="small" background={colours[data.Status]}>
                <CardBody > TaskId : {data.Taskid}</CardBody>
                <CardBody > {data.LambdaName}</CardBody>
                <CardBody > {data.LambdaDescription}</CardBody>
                <CardBody > RunTime : {data.Runtime}</CardBody>
                <CardBody > Retries : {data.Retries ? data.Retries : 0}</CardBody>
                <CardBody > Time Between Retries : {data.TimeBetweenRetries ? data.TimeBetweenRetries : 0}</CardBody>
                <CardBody > Status : {data.Status}</CardBody>
                <CardBody > URL : {data.TaskURL}</CardBody>
                <CardBody > Time taken to execute : {data.TimeToExecute} ms</CardBody>
                <CardBody > Schedule Type : {data.ScheduleType}</CardBody>
                <Box direction="row">
                  <DropButton primary label="Modify" alignSelf="start" color="#232f3e" icon={<Edit />} margin = "small"
                  dropContent={
                  <Box pad="large" background="light-2">
                    <TextInput
                      placeholder="Time delay in ms"
                      timeDelay={timeDelay}
                      onChange={event => setTimeDelay(event.target.value)}
                    />
                  <Button primary label="OK" onClick={() => modifyTask(data.Taskid, timeDelay)} alignSelf="center" margin="small" color="#232f3e"/>
                  </Box>
                  }/>
                  <Button primary label="Cancel" alignSelf="start" color="#232f3e" icon={<Trash />} margin = "small" onClick={() => cancelTask(data.Taskid)}/>
                </Box>
              </Card>
              
          }
          </Box>
        
        
         }}}
    </Async>
    </Box>
}

function RetrieveTaskWithID ({RetrieveType})
{

  const [ButtonClicked, setButtonClicked] = React.useState(false);
  const [TaskID, setTaskID] = React.useState('');

  if(RetrieveType !== 'TaskID')
  {
    return null;
  }

  return <Box direction="column" >
    <Box align="start" justify="center">
      <h3>Enter TaskID: </h3>
    </Box>
      <Box direction="row" align="center" justify="start">
        <TextInput
          TaskID={TaskID}
          onChange={event => setTaskID(event.target.value)}
        />
      
      
        <Button 
          primary 
          label="Get Details" 
          icon = {<SchedulePlay/>}
          color = "#232f3e"
          margin = "small"
          alignSelf = "center"
          onClick = {() => setButtonClicked(true)}
        />
      </Box>

      <Box direction="column">
        <TaskDetails TaskID={TaskID} ButtonClicked={ButtonClicked}/>
      </Box>
  </Box>
}

function RenderAllTasks({TaskStatus})
{
    let colours = {
    "Completed" : "#7cd992",
    "Cancelled" : "#a8a8a8",
    "Failed" : "#eb6060",
    "Running" : "#f7e463",
    "Scheduled" : "#87dfe9"
  }

  console.log("TASKSTATUS: ", TaskStatus)

  let [timeDelay, setTimeDelay] = React.useState('');

  let username = sessionStorage.getItem('username')
  if(username === null)
  {
      return <Box margin="xlarge">Please login before accessing this section</Box>
  }

  return <Box direction="column">
    <Async promiseFn={loadTasks}>
      {({data, err, isLoading}) => {
        if(isLoading)
          return <Spinner size="large" color="#146eb4" margin="xlarge" align="start"/>
        if (err)
          return "Something went wrong"
        if(data)
        {
          if(TaskStatus !== "All")
            data = data.filter((task) => task.Status === TaskStatus)
          }
          
          console.log("DATA: ", data)
          data.sort(compare)

          return <Box direction="column" margin="small" gap="small">
          {
            data.map(task => (
              <Card border="solid" key={task.taskid} pad="small" background={colours[task.Status]}>
                <CardBody > TaskId : {task.Taskid}</CardBody>
                <CardBody > {task.LambdaName}</CardBody>
                <CardBody > {task.LambdaDescription}</CardBody>
                <CardBody > RunTime : {task.Runtime}</CardBody>
                <CardBody > Retries : {task.Retries ? task.Retries : 0}</CardBody>
                <CardBody > Time Between Retries : {task.TimeBetweenRetries ? task.TimeBetweenRetries : 0}</CardBody>
                <CardBody > Status : {task.Status}</CardBody>
                <CardBody > URL : {task.TaskURL}</CardBody>
                <CardBody > Time taken to execute : {task.TimeToExecute} ms</CardBody>
                <CardBody > Schedule Type : {task.ScheduleType}</CardBody>
                <Box direction="row">
                  <DropButton primary label="Modify" alignSelf="start" color="#232f3e" icon={<Edit />} margin = "small"
                  dropContent={
                  <Box pad="large" background="light-2">
                    <TextInput
                      placeholder="Time delay in ms"
                      timeDelay={timeDelay}
                      onChange={event => setTimeDelay(event.target.value)}
                    />
                  <Button primary label="OK" onClick={() => modifyTask(task.Taskid, timeDelay)} alignSelf="center" margin="small" color="#232f3e"/>
                  </Box>
                  }/>
                  <Button primary label="Cancel" alignSelf="start" color="#232f3e" icon={<Trash />} margin = "small" onClick={() => cancelTask(task.Taskid)}/>
                </Box>
              </Card>
              ))
          }
          </Box>
      }
    }</Async>
  </Box>

}

function RetrieveTasksWithStatus({RetrieveType="All"})
{
    const [TaskStatus, setTaskStatus] = React.useState('Status');

    if(RetrieveType !== "Status")
    {
      return null;
    }
    

    return <Box width="50vw">
        <Box direction="row" gap = "small" align="center" justify="start">
          <h3>Showing</h3>
        <Box>
        <Select
          defaultValue = 'All'
          options={["All", "Completed", "Cancelled", "Failed", "Running", "Scheduled"]}
          TaskStatus={TaskStatus}
          onChange={({ option }) => setTaskStatus(option)}
        />
        </Box>
        <h3>Tasks</h3>
    </Box>
    <Box direction="column">
        <RenderAllTasks TaskStatus={TaskStatus}/>
    </Box>
    </Box>
}

function RetrieveTasks()
{
  const margin = {
   "left" : "xlarge"
    }

    const [RetrieveType, setRetrieveType] = React.useState('Status');

  return <Box margin={margin}>
    <Box align="start" justify="start">
      <h2>Retrieve Task Details</h2>
    </Box>
    <Box direction="row" gap="small" align="center" justify="start">
      <h3>Get task details based on</h3>
        <Box width="small">
        <Select
          defaultValue = 'Status'
          options={['TaskID', 'Status',]}
          RetrieveType={RetrieveType}
          onChange={({ option }) => setRetrieveType(option)}
        />
        </Box>
    </Box>
    <RetrieveTaskWithID RetrieveType={RetrieveType}/>
    <RetrieveTasksWithStatus RetrieveType={RetrieveType}/>
  </Box>
}


function About()
{
  return <Box direction="column" margin="xlarge" padding="large" border="solid" height="30vh" width="50vw" align="center" justify="center">
  <text size="Large">Built by Mehul Thakral & Divyansh Dixit for Crio Winter of Doing Stage 3</text>
  <text size="Large">Special thanks to our mentors and the people at Crio for their guidance</text>
  </Box>
}



async function orchestratorCall(JSONdata)
{
  console.log("Orchestrator Call")
  console.log("JSON: ",JSONdata)
  await axios({
        method : 'POST',
        url : backend_url + '/taskset',
        headers: {
         username: sessionStorage.getItem('username'),
         password: sessionStorage.getItem('password')
        },
        data : {
          "initialDelay" : JSONdata["initialDelay"],
          "tasks" : JSONdata["tasks"]
        }
      }) 
      .then((res) => {
        toast.info("Added with ID: " + res.data["id"], {
        position : toast.POSITION.TOP_RIGHT
        })
        console.log("RESPONSE: ",res)
      })
    .catch((res) => 
      {
        console.log("CATCHED: ",res)
        toast.error("Can't orchestrate less than 2 tasks" , {
        position : toast.POSITION.TOP_RIGHT
      })
      return res
      })

}


const Orchestrator = () => (
  <Box margin={{"left" : "xlarge"}}>
    <h3>Task Orchestrator</h3>
    <hr />
    <Formik
      initialValues={{
        tasks: [],
        initialDelay: 0
      }}
      validationSchema={Yup.object({
        initialDelay: Yup.number("Must be number")
          .integer("Must be a integer")
         .required("Initial Delay is required"),
        tasks: Yup.array().of(
          Yup.object().shape({
            taskURL: Yup.string()
              .url("Must be a url")
              .required("TaskURL required"),
            conditionCheckTaskURL: Yup.string()
              .url("Must be a url")
              .required("Condition Check TaskURL required"),
            fallbackTaskURL: Yup.string()
              .url("Must be a url")
              .required("Condition Check TaskURL required"),
            timeDelayForConditionCheck: Yup.number("Must be number")
              .positive("Must be positive")
              .integer("Must be a integer")
              .required("Time Delay is required"),
            conditionCheckRetries: Yup.number("Must be number")
              .positive("Must be positive")
              .integer("Must be a integer")
              .required("No. of retries is required"),
            timeDelayBetweenRetries: Yup.number("Must be number")
              .positive("Must be positive")
              .integer("Must be a integer")
              .required("Time delay is required")
          })
        )
      })}
      onSubmit={(values) => orchestratorCall(values)}
      render={({ values }) => (
        <Form>
          <h5>Enter Initial Delay (in ms) </h5>
          <Field placeholder="Inital Delay" name={`initialDelay`} />
          <ErrorMessage name={`initialDelay`} />
          <h4>Tasks for Orchestration</h4>
          <FieldArray
            name="tasks"
            render={(arrayHelpers) => {
              const tasks = values.tasks;
              return (
                <Box gap="small" width="50vw">
                  {tasks && tasks.length > 0
                    ? tasks.map((task, index) => (
                        <Box key={index} gap="xsmall" border="all" elevation="small" pad="small">

                          <h5>Enter TaskURL</h5>
                          <Field
                            placeholder="TaskURL"
                            name={`tasks.${index}.taskURL`}
                          />
                          <ErrorMessage name={`tasks.${index}.taskURL`} />
                          
                          <h5>Enter Condition Check Task URL</h5>
                          <Field
                            placeholder="Condition Check Task URL"
                            name={`tasks.${index}.conditionCheckTaskURL`}
                          />
                          <ErrorMessage
                            name={`tasks.${index}.conditionCheckTaskURL`}
                          />
                         
                          <h5>Enter Fallback Task URL</h5>
                          <Field
                            placeholder="Fallback Task URL"
                            name={`tasks.${index}.fallbackTaskURL`}
                          />
                          <ErrorMessage
                            name={`tasks.${index}.fallbackTaskURL`}
                          />
                          
                          <h5>Enter Time delay for condition check (in ms)</h5>
                          <Field
                            placeholder="Time delay for condition check (in ms)"
                            name={`tasks.${index}.timeDelayForConditionCheck`}
                          />
                          <ErrorMessage
                            name={`tasks.${index}.timeDelayForConditionCheck`}
                          />

                          
                          <h5>Enter no. of retries for condition check</h5>
                          <Field
                            placeholder="No. of retries for condition check"
                            name={`tasks.${index}.conditionCheckRetries`}
                          />
                          <ErrorMessage
                            name={`tasks.${index}.conditionCheckRetries`}
                          />

                          
                          <h5>Enter time delay between retries of condition check (in ms)</h5>
                          <Field
                            placeholder="Time delay between retries of condition check (in ms)"
                            name={`tasks.${index}.timeDelayBetweenRetries`}
                          />
                          <ErrorMessage
                            name={`tasks.${index}.timeDelayBetweenRetries`}
                          />

  

                          <Button
                            type="button"
                            onClick={() => arrayHelpers.remove(index)} // remove a task from the list
                            justify="center"
                            alignSelf="start" 
                            color="#232f3e" 
                            icon={<Trash />}
                          />
                          
      
                        </Box>
                      ))
                    : null}
                  <Button
                    type="button"
                    onClick={() => arrayHelpers.push({})} // insert an empty string at a position
                    label="ADD"
                    justify="center"
                    alignSelf="start" 
                    color="#232f3e" 
                  />
                  
                  <div>
                    <Button 
                    label="Schedule"
                    type="submit"
                    justify="center"
                    alignSelf="start" 
                    color="#232f3e"
                    />
                  </div>
                </Box>
              );
            }}
          />
          <hr />
        </Form>
      )}
    />
  </Box>
);

async function modifyOrchestratorCall(JSONdata,Taskid)
{
  console.log("Modify Call")
  console.log("JSON: ",JSONdata)
  console.log("Taskid: ", Taskid)
  await axios({
        method : 'PATCH',
        url : backend_url + '/taskset',
        headers: {
         username: sessionStorage.getItem('username'),
         password: sessionStorage.getItem('password')
        },
        data : {
          "id" : Taskid,
          "initialDelay" : JSONdata["initialDelay"],
          "tasks" : JSONdata["tasks"]
        }
      })
      .catch((res) => toast.error("Can't modify this orchestration" , {
        position : toast.POSITION.TOP_RIGHT
      }))
      .then((res) => {
        toast.info("TaskID: " + Taskid + " Modified", {
        position : toast.POSITION.TOP_RIGHT
      })
      })
}

const ModifyOrchestrationForm = ({Taskid}) => (
  <Box margin={{"left" : "xlarge"}}>
    <hr />
    <Formik
      initialValues={{
        tasks: [],
        initialDelay: 0
      }}
      validationSchema={Yup.object({
        initialDelay: Yup.number("Must be number")
          .integer("Must be a integer")
         .required("Initial Delay is required"),
        tasks: Yup.array().of(
          Yup.object().shape({
            taskURL: Yup.string()
              .url("Must be a url")
              .required("TaskURL required"),
            conditionCheckTaskURL: Yup.string()
              .url("Must be a url")
              .required("Condition Check TaskURL required"),
            fallbackTaskURL: Yup.string()
              .url("Must be a url")
              .required("Condition Check TaskURL required"),
            timeDelayForConditionCheck: Yup.number("Must be number")
              .positive("Must be positive")
              .integer("Must be a integer")
              .required("Time Delay is required"),
            conditionCheckRetries: Yup.number("Must be number")
              .positive("Must be positive")
              .integer("Must be a integer")
              .required("No. of retries is required"),
            timeDelayBetweenRetries: Yup.number("Must be number")
              .positive("Must be positive")
              .integer("Must be a integer")
              .required("Time delay is required")
          })
        )
      })}
      onSubmit={(values) => modifyOrchestratorCall(values,Taskid)}
      render={({ values }) => (
        <Form>
          <h5>Enter Initial Delay (in ms) </h5>
          <Field placeholder="Inital Delay" name={`initialDelay`} />
          <ErrorMessage name={`initialDelay`} />
          <h4>Tasks for Orchestration</h4>
          <FieldArray
            name="tasks"
            render={(arrayHelpers) => {
              const tasks = values.tasks;
              return (
                <Box gap="small" width="50vw">
                  {tasks && tasks.length > 0
                    ? tasks.map((task, index) => (
                        <Box key={index} gap="xsmall" border="all" elevation="small" pad="small">

                          <h5>Enter TaskURL</h5>
                          <Field
                            placeholder="TaskURL"
                            name={`tasks.${index}.taskURL`}
                          />
                          <ErrorMessage name={`tasks.${index}.taskURL`} />
                          
                          <h5>Enter Condition Check Task URL</h5>
                          <Field
                            placeholder="Condition Check Task URL"
                            name={`tasks.${index}.conditionCheckTaskURL`}
                          />
                          <ErrorMessage
                            name={`tasks.${index}.conditionCheckTaskURL`}
                          />
                         
                          <h5>Enter Fallback Task URL</h5>
                          <Field
                            placeholder="Fallback Task URL"
                            name={`tasks.${index}.fallbackTaskURL`}
                          />
                          <ErrorMessage
                            name={`tasks.${index}.fallbackTaskURL`}
                          />
                          
                          <h5>Enter Time delay for condition check (in ms)</h5>
                          <Field
                            placeholder="Time delay for condition check (in ms)"
                            name={`tasks.${index}.timeDelayForConditionCheck`}
                          />
                          <ErrorMessage
                            name={`tasks.${index}.timeDelayForConditionCheck`}
                          />

                          
                          <h5>Enter no. of retries for condition check</h5>
                          <Field
                            placeholder="No. of retries for condition check"
                            name={`tasks.${index}.conditionCheckRetries`}
                          />
                          <ErrorMessage
                            name={`tasks.${index}.conditionCheckRetries`}
                          />

                          
                          <h5>Enter time delay between retries of condition check (in ms)</h5>
                          <Field
                            placeholder="Time delay between retries of condition check (in ms)"
                            name={`tasks.${index}.timeDelayBetweenRetries`}
                          />
                          <ErrorMessage
                            name={`tasks.${index}.timeDelayBetweenRetries`}
                          />

  

                          <Button
                            type="button"
                            onClick={() => arrayHelpers.remove(index)} // remove a task from the list
                            justify="center"
                            alignSelf="start" 
                            color="#232f3e" 
                            icon={<Trash />}
                          />
                          
      
                        </Box>
                      ))
                    : null}
                  <Button
                    type="button"
                    onClick={() => arrayHelpers.push({})} // insert an empty string at a position
                    label="ADD TASK"
                    justify="center"
                    alignSelf="start" 
                    color="#232f3e" 
                  />
                  
                  <div>
                    <Button 
                    label="MODIFY ORCHESTRATION"
                    type="submit"
                    justify="center"
                    alignSelf="start" 
                    color="#232f3e"
                    />
                  </div>
                </Box>
              );
            }}
          />
          <hr />
        </Form>
      )}
    />
  </Box>
);



function ModifyOrchestration({Taskid})
{
  // let subtitle;
  const [modalIsOpen,setIsOpen] = React.useState(false);
  function openModal() {
    setIsOpen(true);
  }
 
  function afterOpenModal() {
    // references are now sync'd and can be accessed.
    // subtitle.style.color = '#f00';
  }
 
  function closeModal(){
    setIsOpen(false);
  }

  const modalStyle = {
    "max-height" : "100vh",
    "overflow-y" : "auto"
  };
 
    return (
      <Box pad="small">
        <Button
        primary
        onClick={openModal}
        alignSelf="center" 
        color="#232f3e" 
        icon={<Edit />} 
        margin = "small"
        label = "Modify"
        />
        <Modal
          
          isOpen={modalIsOpen}
          onAfterOpen={afterOpenModal}
          onRequestClose={closeModal}
          style={customStyles}
          contentLabel="Example Modal"
        >
          <div style={modalStyle}>
          <h1>Modifying Orchestration for Taskid: {Taskid}</h1>
          <Button 
          primary
          onClick={closeModal} 
          label="Close"
          alignSelf="end" 
          color="#232f3e" 
          icon={<Trash />} 
          />
          <ModifyOrchestrationForm Taskid={Taskid}/>
          </div>
        </Modal>
      </Box>
    );
}

function CancelOrchestration(Taskid)
{
  console.log("CANCELLING: ",Taskid)
  fetch(backend_url + "/taskset/" + Taskid, {
  method: 'DELETE',
  headers: {
    username: sessionStorage.getItem('username'),
    password: sessionStorage.getItem('password')
    },
  }).catch(res => toast.error("Failed to cancel task"))
    .then(res => toast.info("TaskID " + Taskid + " Cancelled"))
}

const FetchOrchestratorTasks = () =>
  fetch("http://localhost:5000/taskset/retrieve", {
  method: 'GET',
  headers: {
    username: sessionStorage.getItem('username'),
    password: sessionStorage.getItem('password')
    },
  })
    .then(res => (res.ok ? res : Promise.reject(res)))
    .then(res => res.json())

function compareOrchestration(a,b)
{
  if(a.id > b.id)
    return -1;
  return 1;
}

function RenderOrchestratorTasks({TaskStatus})
{
  let colours = {
    "Completed" : "#7cd992",
    "Cancelled" : "#a8a8a8",
    "Failed" : "#eb6060",
    "Running" : "#f7e463",
    "Scheduled" : "#87dfe9"
  }

  return <Async promiseFn={FetchOrchestratorTasks}>
      {({data, err, isLoading}) => {
        if(isLoading)
          return <Spinner size="large" color="#146eb4" margin={{"left" : "medium"}} align="center"/>
        if (err)
          return "Something went wrong"
        if(data)
        {
          if(TaskStatus !== "All")
          data = data.filter((task) => task.status  === TaskStatus)
        }
          data.sort(compareOrchestration)
          console.log("DATA: ",data)
          console.log("STATUS: ",TaskStatus)
          return <Box direction="column" gap="small">
          {
            data.map(task => (
              <Card pad="small" border="solid" key={task.id} background={colours[task.status]} width="50vw">
                <CardBody > TaskId : {task.id}</CardBody>
                <CardBody > Initial Delay : {task.initialDelay}</CardBody>
                <CardBody > Status : {task.status}</CardBody>
                <CardBody > URL : {task.TaskURL}</CardBody>
                <CardBody > Time taken to execute : {task.TimeToExecute} ms</CardBody>
                <CardBody > Schedule Type : {task.ScheduleType}</CardBody>
                <Box>
                  {task.tasks.map((taskDetail, index) => {
                    return <Box margin="small" key={index}>
                    <h4>Task {index+1}:</h4>
                    <CardBody > Condition Check Retries : {taskDetail.conditionCheckRetries}</CardBody>
                    <CardBody > Condition Check TaskURL : {taskDetail.conditionCheckTaskURL}</CardBody>
                    <CardBody > Fallback TaskURL : {taskDetail.fallbackTaskURL}</CardBody>
                    <CardBody > TaskURL : {taskDetail.taskURL} </CardBody>
                    <CardBody > Time Delay Between Retries : {taskDetail.timeDelayBetweenRetries} ms</CardBody>
                    <CardBody > Time Delay For Condition Check : {taskDetail.timeDelayForConditionCheck} ms </CardBody>
                    </Box>
                  })}
                </Box>

                <Box direction="row">
                  <ModifyOrchestration Taskid={task.id}/>
                  <Button primary label="Cancel" alignSelf="center" color="#232f3e" icon={<Trash />} margin = "small" onClick={() => CancelOrchestration(task.id)}/>
                </Box>

              </Card>
              ))
          }
          </Box>
      }
    }</Async>
}


function RetrieveOrchestrationsWithStatus({RetrieveType})
{
    const [TaskStatus, setTaskStatus] = React.useState('All');

    return <Box width="100vw" >
        <Box direction="row" gap = "small" align="center" justify="start">
          <h3>Showing</h3>
        <Box>
        <Select
          defaultValue = 'All'
          options={["All", "Completed", "Cancelled", "Failed", "Running", "Scheduled"]}
          TaskStatus={TaskStatus}
          onChange={({ option }) => setTaskStatus(option)}
        />
        </Box>
        <h3>Orchestrations</h3>
    </Box>
    <Box direction="column">
        <RenderOrchestratorTasks TaskStatus={TaskStatus}/>
    </Box>
    </Box>
}



function OrchestratorTasks()
{
  let [timeDelay, setTimeDelay] = React.useState('');
  let [taskId, setTaskId] = React.useState('');
  let [taskStatus, setTaskStatus] = React.useState('');
  let [RetrieveType, setRetrieveType] = React.useState('');

  let username = sessionStorage.getItem('username')
  if(username === null)
  {
      return <Box margin="xlarge">Please login before accessing this section</Box>
  }

  return <Box direction="column" margin={{"left" : "xlarge"}} align="start" justify="start">
    <h1>Retrieve Details of Orchestrated Tasks</h1>
    <RetrieveOrchestrationsWithStatus/>

    
  </Box>
}



function App() {

  return (
      <Grommet theme={theme}>
      <Box direction="row-responsive" height='{"min":"100vh"}'>
        <Navbar />
        <ToastContainer />
      </Box>
      </Grommet>
    );
}



export default App;
