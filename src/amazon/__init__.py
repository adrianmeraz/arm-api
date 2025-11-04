import boto3

from src.amazon.parameter_store import ParameterStore

__session = boto3.Session()

dynamodb_client = __session.resource('dynamodb')
ps_client = boto3.client('ssm')
param_store = ParameterStore(ps_client=ps_client)
