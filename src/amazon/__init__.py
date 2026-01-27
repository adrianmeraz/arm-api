import boto3

from src.amazon.parameter_store import ParameterStore

__session = boto3.Session()

dynamodb_client = __session.resource('dynamodb')
ssm_client = boto3.client('ssm')
param_store = ParameterStore(ssm_client=ssm_client)
comprehend_client = boto3.client('comprehend')
