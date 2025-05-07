
import boto3
import os
import datetime

USERS_TABLE = os.environ['USERS_TABLE']
SCHEDULE_TABLE = os.environ['SCHEDULE_TABLE']

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table(USERS_TABLE)
schedule_table = dynamodb.Table(SCHEDULE_TABLE)

# SES Client
ses = boto3.client('ses', region_name='us-west-2')  # Adjust to your region

def send_email(name, email, week_start):
    ses.send_email(
        Source='ayalate@unomaha.edu',  # Replace with your verified SES email
        Destination={'ToAddresses': [email]},
        Message={
            'Subject': {'Data': 'You are now On-Call'},
            'Body': {'Text': {'Data': f"Hello {name},\n\nYou are scheduled as On-Call for the week starting {week_start}.\n\nThank you."}}
        }
    )

def handler(event, context):
    # Fetch users list
    response = users_table.scan()
    users = response.get('Items', [])
    if not users:
        print("No users found")
        return

    users_sorted = sorted(users, key=lambda x: x['id'])

    # Find last scheduled user
    current_week = datetime.date.today().strftime("%Y-%m-%d")
    prev_schedule = schedule_table.scan().get('Items', [])

    last_user_id = None
    if prev_schedule:
        prev_schedule_sorted = sorted(prev_schedule, key=lambda x: x['week_start'], reverse=True)
        last_user_id = prev_schedule_sorted[0]['oncall_user_id']

    # Determine next user
    next_user_index = 0
    if last_user_id:
        for idx, user in enumerate(users_sorted):
            if user['id'] == last_user_id:
                next_user_index = (idx + 1) % len(users_sorted)
                break

    next_user = users_sorted[next_user_index]

    # Store new schedule
    schedule_table.put_item(
        Item={
            'week_start': current_week,
            'oncall_user_id': next_user['id']
        }
    )

    print(f"On-Call user for {current_week} is {next_user['id']}")

    # Send email notification
    send_email(next_user['name'], next_user['email'], current_week)
