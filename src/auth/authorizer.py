from src import logs

logger = logs.get_logger()

def lambda_handler(event, context):
    logger.info(f'event: {event}, context: {context}')
    return True
