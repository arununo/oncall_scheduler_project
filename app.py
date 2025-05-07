
import aws_cdk as cdk
from oncall_scheduler_project.oncall_scheduler_project_stack import OnCallSchedulerStack

app = cdk.App()
OnCallSchedulerStack(app, "OnCallSchedulerStack")
app.synth()
