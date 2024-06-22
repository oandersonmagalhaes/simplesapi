from simplesapi.types import AWSSession

class SNS:
    def __init__(self, session: AWSSession, topic_arn: str):
        self.topic_arn = topic_arn
        self.session = session
        self.client_config = {"service_name":"sns", "endpoint_url":"http://localhost:4566"} if session.aws_local else {"service_name":"sns"}

    async def publish_message(self, message: str):
        async with self.session.client('sns') as client:
            response = await client.publish(
                TopicArn=self.topic_arn,
                Message=message
            )
            return response
