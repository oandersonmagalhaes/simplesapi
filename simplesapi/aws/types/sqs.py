from simplesapi.types import AWSSession

class SQS:
    def __init__(self, session: AWSSession, queue_name: str):
        self.queue_name = queue_name
        self.session = session

    async def send_message(self, message_body: str):
        async with self.session.client('sqs') as client:
            response = await client.send_message(
                QueueUrl=self.queue_name,
                MessageBody=message_body
            )
            return response

    async def receive_message(self):
        async with self.session.client('sqs') as client:
            response = await client.receive_message(
                QueueUrl=self.queue_name
            )
            return response

    async def delete_message(self, receipt_handle: str):
        async with self.session.client('sqs') as client:
            response = await client.delete_message(
                QueueUrl=self.queue_name,
                ReceiptHandle=receipt_handle
            )
            return response

    async def list_queues(self):
        async with self.session.client('sqs') as client:
            response = await client.list_queues()
            return response
