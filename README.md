# AWS scheduler

This repo contains a script useful to schedule power on and off of EC2 Instances. Moreover there is a Python Script that using boto3 library to create all lamba functions directly on AWS

## Usage
Edit create-lambda-function.py and insert all your schedules.

>vms = {

>'iot-dev-on' : {'project': 'iot', 'environment': 'dev', 'action': 'start', 'scheduler': 'cron(0 7 ? * 1-5 *)'},

>'iot-dev-off' : {'project': 'iot', 'environment': 'dev', 'action': 'stop', 'scheduler': 'cron(55 17 ? * * *)'},

>}

project and enviroment are tags present on your EC2 instance.
Once you have edit, launch from shell create-lambda-function.py Script

### Requirements
- python 2.7
- boto3 library
- aws command line configured with your credential
