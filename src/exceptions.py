class BaseArmException(Exception):
    pass

class DDBException(BaseArmException):
    """DynamoDB Exceptions"""

class ParameterStoreException(BaseArmException):
    """ParameterStore Exceptions"""
