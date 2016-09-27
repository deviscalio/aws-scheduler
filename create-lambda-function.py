#!/usr/bin/python
import boto3
import zipfile
import json

aws=boto3.Session(region_name=('eu-west-1'))
lam=aws.client('lambda')
cwe=aws.client('events')

zf = zipfile.ZipFile('power-vm-package.zip', mode='w')
try:
    zf.write('power-off.py')
finally:
    zf.close()

vms = {
'iot-dev-on' : {'project': 'iot', 'environment': 'dev', 'action': 'start', 'scheduler': 'cron(0 7 ? * 1-5 *)'},
'iot-dev-off' : {'project': 'iot', 'environment': 'dev', 'action': 'stop', 'scheduler': 'cron(55 17 ? * * *)'},
}
#cron(55 17 ? * * *)
#rate(1 minute)

for vm in vms:

    # Clean previous items
    try:
        lam.delete_function(
            FunctionName=vm
            )
        cwe.remove_targets(
            Rule=vm,
            Ids=[ vm ]
        )
        cwe.delete_rule(
            Name=vm
        )
    except:
        pass

    # Create Rule
    rule = cwe.put_rule(
        Name=vm,
        ScheduleExpression=vms[vm]["scheduler"]
        )

    lf = lam.create_function(FunctionName=vm,
                             Runtime='python2.7',
                             Role='arn:aws:iam::345762685377:role/lambda_start_stop_ec2',
                             Handler='power-off.lambda_handler',
                             Code={
                                'ZipFile': open('power-vm-package.zip', 'rb').read(),
                             },
                             Timeout=15,
                             MemorySize=128)

    lam.add_permission(FunctionName=vm,
                       StatementId=vm,
                       Action='lambda:InvokeFunction',
                       Principal='events.amazonaws.com',
                       SourceArn=rule["RuleArn"])

    lf_input = {
            'project': vms[vm]["project"],
            'environment': vms[vm]["environment"],
            'action': vms[vm]["action"]
        }

    cwe.put_targets(Rule=vm,
                    Targets=[{'Id': vm,
                                'Arn': lf['FunctionArn'],
                                'Input': json.dumps(lf_input)}])
