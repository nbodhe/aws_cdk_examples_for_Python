from aws_cdk import (
        aws_dynamodb as _dynamodb,
        aws_s3 as _s3,
        aws_lambda as _lambda,
        aws_sns as sns,
        aws_stepfunctions as sfn,
        aws_stepfunctions_tasks as tasks,
        core
        )

class MyProjectStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        #lf1= Function(self, id="my_stack_lambda", runtime=Runtime.PYTHON_3_7, handler='handlers/my_lambda_handler', code='', function_name='my_example_lambda')
        my_table=_dynamodb.Table(self, id='dynamoTable', table_name='testcdktabe', partition_key=_dynamodb.Attribute(name='lastname', type=_dynamodb.AttributeType.STRING))
        my_s3_bucket=_s3.Bucket(self, id='s3bucket', bucket_name='mynpbsample3bucket')

        my_lambda_function=_lambda.Function(self, id='lambdafunction', runtime=_lambda.Runtime.PYTHON_3_7, handler='hello.handler', code=_lambda.Code.asset('lambdacode'))


        process_purchase_function=_lambda.Function(self, id='process_purchase', runtime=_lambda.Runtime.PYTHON_3_7, handler='process_purchase.handler', code=_lambda.Code.asset('lambdacode'))


        process_refund_function=_lambda.Function(self, id='process_refund', runtime=_lambda.Runtime.PYTHON_3_7, handler='process_refund.handler', code=_lambda.Code.asset('lambdacode'))

        #start_state = sfn.Pass(self, "start_state")

        definition = sfn.Task(self, 'Get Process Type', task = tasks.InvokeFunction(process_purchase_function))

        sfn.StateMachine(
            self, "MyStateMachine",
            definition=definition,
            timeout=core.Duration.seconds(30),
        )

        my_topic = sns.Topic(self, "MyTopic", display_name="Customer Subscription")
