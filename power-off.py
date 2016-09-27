import boto3
import logging
import json

#setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#define the connection
ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
    # Use the filter() method of the instances collection to retrieve
    # all running EC2 instances #"

    print json.dumps(event)

    filters = [{
            'Name': 'tag:Project',
            'Values': [ event["project"] ]
        },
        {
            'Name': 'tag:Deployment',
            'Values': [ event["environment"] ]
        }
    ]

    #filter the instances
    instances = ec2.instances.filter(Filters=filters)

    #locate all running instances
    RunningInstances = [instance.id for instance in instances]

    #make sure there are actually instances to shut down.
    if len(RunningInstances) > 0:
        #perform the shutdown
        response = ""
        if event["action"] == "start":
            response = ec2.instances.filter(InstanceIds=RunningInstances).start()
        if event["action"] == "stop":
            response = ec2.instances.filter(InstanceIds=RunningInstances).stop()
        print response
    else:
        print "Nothing to see here"
