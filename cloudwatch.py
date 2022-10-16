import boto3
sns_topic_arn = 'Desired sns topic arn'
notification_email='example@example.com'
alarm= {
    "Your Instance id" : "Threshold on which the alarm will trigger(Must be an integer value)" ,
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
client_cw = boto3.client('cloudwatch')
for i,j in zip(keys,values):
 response = client_cw.put_metric_alarm(
          AlarmName='ec2-cpu-alarmsadasd',
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
