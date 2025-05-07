
import boto3
import os
import datetime

USERS_TABLE = os.environ['USERS_TABLE']
SCHEDULE_TABLE = os.environ['SCHEDULE_TABLE']

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table(USERS_TABLE)
schedule_table = dynamodb.Table(SCHEDULE_TABLE)

def handler(event, context):
    response = users_table.scan()
    users = response.get('Items', [])
    if not users:
        print("No users found")
        return

    users_sorted = sorted(users, key=lambda x: x['id'])

    current_week = datetime.date.today().strftime("%Y-%m-%d")
    prev_schedule = schedule_table.scan().get('Items', [])

    last_user_id = None
    if prev_schedule:
        prev_schedule_sorted = sorted(prev_schedule, key=lambda x: x['week_start'], reverse=True)
        last_user_id = prev_schedule_sorted[0]['oncall_user_id']

    next_user_index = 0
    if last_user_id:
        for idx, user in enumerate(users_sorted):
            if user['id'] == last_user_id:
                next_user_index = (idx + 1) % len(users_sorted)
                break

    next_user = users_sorted[next_user_index]

    schedule_table.put_item(
        Item={
            'week_start': current_week,
            'oncall_user_id': next_user['id']
        }
    )

    print(f"On-Call user for {current_week} is {next_user['id']}")
