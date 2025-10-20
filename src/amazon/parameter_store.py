import json
import logging
import os

from src import exceptions

logger = logging.getLogger(__name__)
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
            logger.info(f'get_secret# r: {self.Response(r).Parameter.Value}')
            try:
                logger.info(f'get_secret# secret value: {self.Response(r).Parameter.Value}')
                __secrets = json.loads(self.Response(r).Parameter.Value)
            except json.decoder.JSONDecodeError as e:
                raise exceptions.ParameterStoreException('Failed to decode json secrets from Parameter Store') from e

        logger.info(f'get_secret# secrets: {self.__secrets}')
        return self.__secrets.get(key)
