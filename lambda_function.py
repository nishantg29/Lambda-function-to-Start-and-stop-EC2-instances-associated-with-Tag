import os
import boto3

# Get the Instance State by filter "running" | "Stop"
def getInstanceState(project,state):
    ec2 = boto3.resource('ec2')

    print("Trace1: Get into the list of instances")
    filters = [
            {
            'Name': 'tag:project',
            'Values': [project]
            },
            {
            'Name': 'instance-state-name', 
            'Values': [state]}
       ]
       
    # filter the state and save into list 
    RunningInstances = []
    for instance in ec2.instances.filter(Filters=filters):
        print("Trace2: Append List")
        RunningInstances.append(instance)
    return RunningInstances

def startInstance(project):
    print("Trace3: Start Stop Instances- using tag")
    toStartInstance = getInstanceState(project,'stopped')
    print("startinstaces")
    statechange =0
    for instance in toStartInstance:
        instance.start()
        statechange +=1
    return statechange

def stopInstace(project):
    print("Trace4: Stop Start Instances- using tag")
    toStopInstance = getInstanceState(project,'running')
    statechange =0
    for instance in toStopInstance:
        print("StopInstances")
        instance.stop()
        statechange +=1
    return statechange

def lambda_handler(event, context):
    print("Trace-Main: Enter to Lambda handler:")
    #set envirement variable project as a demo 
    #For Example create a instance and give a "TAGS" value "key"--> project and "value"--> demo
    # The instance which have a tag with demo will only start and stop
    project = os.getenv('project','demo')
    print(project)
    statechange = 0
    if(event.get('action') == 'start'):
        statechange = startInstance(project)
    elif(event.get('action') == 'stop'):
        statechange = stopInstace(project)
        
    return statechange
