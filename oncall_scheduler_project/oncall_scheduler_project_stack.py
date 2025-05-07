
from aws_cdk import (
    App,
    Stack,
    RemovalPolicy,
    aws_lambda as _lambda,
    aws_events as events,
    aws_events_targets as targets,
    aws_dynamodb as dynamodb,
    aws_iam as iam
)
from constructs import Construct

class OnCallSchedulerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        users_table = dynamodb.Table(
            self, "OnCallUsers",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )

        schedule_table = dynamodb.Table(
            self, "OnCallSchedule",
            partition_key=dynamodb.Attribute(name="week_start", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )

        rotation_lambda = _lambda.Function(
            self, "OnCallRotationLambda",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="rotation.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "USERS_TABLE": users_table.table_name,
                "SCHEDULE_TABLE": schedule_table.table_name
            }
        )

        rotation_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=["ses:SendEmail", "ses:SendRawEmail"],
                resources=["*"]  # or your verified domain/email ARN
            )
        )

        users_table.grant_read_write_data(rotation_lambda)
        schedule_table.grant_read_write_data(rotation_lambda)

        rule = events.Rule(
            self, "WeeklyRotationRule",
            schedule=events.Schedule.cron(minute="0", hour="0", week_day="MON", month="*", year="*")
        )

        rule.add_target(targets.LambdaFunction(rotation_lambda))

app = App()
OnCallSchedulerStack(app, "OnCallSchedulerStack")
app.synth()
