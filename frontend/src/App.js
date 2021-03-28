import React from 'react';
import {Box,Button,Card,CardBody,Grommet,Nav,Sidebar,Select,TextInput, Spinner } from 'grommet';
import {Add,Amazon,CircleInformation,Clock,Domain,Edit,History,Link as URL,Revert,SchedulePlay,Tasks,TextAlignFull,Trash} from 'grommet-icons';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import Async from 'react-async';

const axios = require('axios');

const theme = {
  global: {
    font: {
      family: 'Roboto',
      size: '18px',
      height: '20px',
    },
  },
};


function Navbar() 
  {    
      return <Router>
      <div style={{position : 'fixed'}}>
      <Sidebar background="#FF9900"
      header={
        <Link to="/"><Button icon={<Amazon color='black'/>} hoverIndicator/></Link>
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
      </Nav>
    </Sidebar>
    </div>
    <Switch>
          <Route path="/" exact="true">
            <Home />
          </Route>
          <Route path="/addTask">
            <AddTask />
          </Route>
          <Route path="/allTasks">
            <AllTasks />
          </Route>
          <Route path="/about">
            <About />
          </Route>
        </Switch>

    </Router>
  }


function Home()
{
  return <Box direction="column" border="solid" margin="xlarge" align="center">
  <h1>CWoD AWS - Task Scheduler and Orchestrator</h1>
  <h2>AWS T4</h2>
  </Box>
}

async function ScheduleTask(LambdaName,
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
      }).then((response) => alert("Task scheduled with id: " + response.data.id)) 
    }
  else if(SchedulingType === 'Based on Date and Time in future, Ex:"28 Mar 2021 23:05:00"')
      await axios({
        method : 'post',
        url : 'http://localhost:5000/tasks',
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
      }).then((response) => alert("Task scheduled with id: " + response.data.id)) 

  console.log("Tried to schedule")
}

function AddTask()
{
  const [TaskURL, setTaskURL] = React.useState('');
  const [LambdaName, setLambdaName] = React.useState('');
  const [LambdaDescription, setLambdaDescription] = React.useState('');
  const [Retries, setRetries] = React.useState('');
  const [RetryGap, setRetryGap]  = React.useState('');
  const [SchedulingType, setSchedulingType] = React.useState('');
  const [DelayValue, setDelayValue] = React.useState('');

  return <Box direction="column" width="100%" margin='xlarge' align="center">
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
      icon = {<URL/>}
      placeholder="Enter URL of Lambda function"
      TaskURL={TaskURL}
      onChange={event => setTaskURL(event.target.value)}
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
        console.log("TYPE: ", option)
      }}
    />

    <TextInput
      icon = {<Clock/>}
      DelayValue={DelayValue}
      onChange={event => setDelayValue(event.target.value)}
    />

    <Button 
    primary 
    label="Schedule Task" 
    icon = {<SchedulePlay/>}
    color = "#146eb4"
    margin = "small"
    alignSelf = "center"
    onClick = {() => ScheduleTask(
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

const loadTasks = () =>
    fetch("http://localhost:5000/tasks/retrieve")
    .then(res => (res.ok ? res : Promise.reject(res)))
    .then(res => res.json())

function compare(a,b)
{
  if(a.Taskid > b.Taskid)
    return -1;
  return 1;
}

function AllTasks()
{
  return <>
    <Async promiseFn={loadTasks}>
      {({data, err, isLoading}) => {
        if(isLoading)
          return <Spinner size="large" color="#146eb4" margin="xlarge" align="center"/>
        if (err)
          return "Something went wrong"
        if(data)
          data.sort(compare)
          return <Box direction="column" margin="xlarge" gap="small">
          <h2>Details of all tasks:</h2>
          {
            data.map(task => (
              <Card padding="small" margin='{"left" : "medium"}' border="solid" elevation="large">
                <CardBody pad="medium"> TaskId : {task.Taskid}</CardBody>
                <CardBody pad="medium"> RunTime : {task.Runtime}</CardBody>
                <CardBody pad="medium"> Status : {task.Status}</CardBody>
                <CardBody pad="medium"> URL : {task.TaskURL}</CardBody>
                <Box direction="row">
                  <Button primary label="Modify" alignSelf="start" color="#146eb4" icon={<Edit />} margin = "small"/>
                  <Button primary label="Cancel" alignSelf="start" color="#146eb4" icon={<Trash />} margin = "small"/>
                </Box>
              </Card>
            ))
          }
          </Box>
      }}
  </Async>
  </>
}

function About()
{
  return <Box direction="column" margin="xlarge" padding="small" border="solid">
  <h4>Built by Mehul Thakral & Divyansh Dixit for Crio Winter of Doing Stage 3</h4>
  <h4>Special thanks for our mentors and the people at Crio for their guidance</h4>
  </Box>
}

function Corrector()
{
  return <div marginLeft="100%">

  </div>
}


function App() {
  return (
    <Grommet theme={theme}>
    <Box direction="row-responsive" height='{"min":"100vh"}' animation="zoomOut">
      <Navbar />
      <Corrector />
    </Box>
    </Grommet>
  );
}

export default App;
