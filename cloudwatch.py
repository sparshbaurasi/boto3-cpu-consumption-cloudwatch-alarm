import boto3
client_cw = boto3.client('cloudwatch')
sns_topic_arn = 'Desired sns topic arn' # Here you put sns topic arn on which the alarm will will send a notification to when it gets triggered
notification_email='example@example.com' # Here paste the email on which the sns topic will send notification to
alarm_name='alarm name that the user wants' 
alarm= {
    "i-Random string" : 1 , # Here you put the instance id for which you want to create the alarm and for its value you put at which threshold the alarm will trigger eg: 1,2,...100 
}
keys = list(alarm.keys())
values = list(alarm.values())
client_sns=boto3.client('sns')
response2 = client_sns.subscribe(
    TopicArn=sns_topic_arn,
    Protocol='email',
    Endpoint=notification_email,
    ReturnSubscriptionArn=True
)
for i,j in zip(keys,values):
 response = client_cw.put_metric_alarm(
          AlarmName=alarm_name,
          ActionsEnabled=True,
          AlarmActions=[
               sns_topic_arn,
          ],
          MetricName='CPUUtilization',
          Namespace='AWS/EC2',
          Statistic='Average',
          Dimensions=[
              {
                  'Name': 'InstanceId',
                  'Value': i
              },
          ],
          Period=60,
          EvaluationPeriods=1,
          DatapointsToAlarm=1,
          Threshold=j,
          ComparisonOperator='GreaterThanThreshold',
          Tags=[
              {
                  'Key': 'Name',
                  'Value': 'Ec2-util'
              },
          ]
      )
