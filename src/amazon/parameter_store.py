import json
import os

from src import exceptions, logs

logger = logs.get_logger()
SM_PARAM_STORE_KEY = 'AWS_SECRET_NAME'


class ParameterStore:
    __secrets = dict()

    def __init__(self, ps_client):
        self.ps_client = ps_client

    class Response:
        def __init__(self, data):
            self.Parameter = self.Parameter(data['Parameter'])

        class Parameter:
            def __init__(self, data):
                self.ARN = data['ARN']
                self.LastModifiedDate = data['LastModifiedDate']
                self.Name = data['Name']
                self.Type = data['Type']
                self.Value = data['Value']
                self.Version = data['Version']

    @property
    def sm_param_store_key(self) -> str:
        try:
            return os.environ[SM_PARAM_STORE_KEY]
        except KeyError:
            raise exceptions.ParameterStoreException(f'Missing environment variable "{SM_PARAM_STORE_KEY}"')

    def get_secret(self, key: str) -> str:
        if value := os.environ.get(key):
            return value

        if not self.__secrets:
            r = self.ps_client.get_parameter(Name=self.sm_param_store_key, WithDecryption=True)
            value = self.Response(r).Parameter.Value
            try:
                self.__secrets = json.loads(value)
            except json.decoder.JSONDecodeError as e:
                raise exceptions.ParameterStoreException('Failed to decode json secrets from Parameter Store') from e

        return self.__secrets.get(key)
