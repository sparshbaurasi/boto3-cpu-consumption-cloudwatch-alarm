import boto3
sns_topic_arn = 'arn:aws:sns:ap-south-1:612490972332:cpu-utilization-sns'
notification_email='sparsh.baurasi@virtuecloud.io'
alarm= {
    "i-0e778794334bf41db" : 20 ,
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
          AlarmName='ec2-cpu-alarm',
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
          Unit='second',
          EvaluationPeriods=1,
          DatapointsToAlarm=1,
          Threshold=j,
          ComparisonOperator='GreaterThanUpperThreshold',
          Tags=[
              {
                  'Key': 'Name',
                  'Value': 'Ec2-util'
              },
          ]
      )
