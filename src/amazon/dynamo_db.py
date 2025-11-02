import typing

from botocore.exceptions import ClientError

from src import exceptions, logs

logger = logs.get_logger()


class DynamoDBClient:
    def __init__(self, dynamodb_client: typing.Any, table_name: str):
        # boto3 resource objects provide a Table() factory; use typing.Any for
        # the client to avoid static-analysis resolving boto3 internals here.
        self._table = dynamodb_client.Table(table_name)
        self._key_schema = {schema['KeyType']: schema['AttributeName'] for schema in self._table.key_schema}

    @property
    def hash_key_attribute_name(self):
        return self._key_schema['HASH']

    @property
    def range_key_attribute_name(self):
        return self._key_schema['RANGE']

    def get_all_table_items(self, limit: int = None, **kwargs):
        """Scan the table and return all items, using pagination.

        This method will page through DynamoDB scan results until there are no
        more pages or until ``limit`` items have been collected (if provided).

        Args:
            limit: Optional maximum number of items to return. If None, all
                items from the table will be returned.
            **kwargs: Additional keyword arguments passed through to ``scan``.

        Returns:
            A list of item dicts.
        """
        items = []
        scan_kwargs: dict[str, typing.Any] = dict(**kwargs)

        while True:
            # if a global limit is provided, pass remaining as the per-scan Limit
            if limit is not None:
                remaining = limit - len(items)
                if remaining <= 0:
                    break
                # DynamoDB expects an integer Limit; ensure correct type.
                scan_kwargs['Limit'] = int(remaining)

            response = self._table.scan(**scan_kwargs)
            page_items = response.get('Items', [])
            items.extend(page_items)

            # If we've reached the requested limit, stop
            if limit is not None and len(items) >= limit:
                return items[:limit]

            # Continue to next page if present
            if 'LastEvaluatedKey' in response:
                scan_kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']
                # continue loop to fetch next page
                continue

            break

        return items

    def create_item(self, item: dict, **kwargs: dict):
        try:
            logger.info(f'Creating item: {item}')
            self._table.put_item(Item=item, **kwargs)
            return item
        except ClientError as e:
            raise exceptions.DDBException() from e

    def delete_item(self, hash_key: str, sort_key: str):
        return self._table.delete_item(
            Key={
                self.hash_key_attribute_name: hash_key,
                self.range_key_attribute_name: sort_key
            }
        )

    def delete_all_items(self):
        response = self._table.scan()
        data = response['Items']

        # Continue scanning if there are more items (pagination)
        while 'LastEvaluatedKey' in response:
            response = self._table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])

        # Batch delete items
        try:
            with self._table.batch_writer() as batch:
                for item in data:
                    batch.delete_item(Key={
                        self.hash_key_attribute_name: item[self.hash_key_attribute_name],
                        self.range_key_attribute_name: item[self.range_key_attribute_name]
                    })
        except ClientError as e:
            raise exceptions.DDBException() from e

    def get_item(self, hash_key: str, sort_key: str, **kwargs: dict):
        response = self._table.get_item(
            Key={
                self.hash_key_attribute_name: hash_key,
                self.range_key_attribute_name: sort_key
            },
            **kwargs
        )
        return response.get('Item', None)

    def batch_write_items(self, items: typing.List[dict], **kwargs: dict):
        try:
            with self._table.batch_writer() as batch:
                logger.info(f'Writing {len(items)} batch items')
                for item in items:
                    try:
                        batch.put_item(Item=item, **kwargs)
                    except ClientError as e:
                        raise exceptions.DDBException() from e
        except ClientError as e:
            raise exceptions.DDBException() from e
