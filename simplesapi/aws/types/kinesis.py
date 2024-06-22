from simplesapi.types import AWSSession
from typing import Dict, Any

class Kinesis:
    def __init__(self, session: AWSSession, stream_name: str):
        self.stream_name = stream_name
        self.session = session
        self.client_config = {"service_name":"kinesis", "endpoint_url":"http://localhost:4566"} if session.aws_local else {"service_name":"kinesis"}

    async def put_record(self, data: Dict[str, Any], partition_key: str):
        async with self.session.client(**self.client_config) as client:
            response = await client.put_record(
                StreamName=self.stream_name,
                Data=data,
                PartitionKey=partition_key
            )
            return response

    async def put_records(self, records: Dict[str, Any]):
        async with self.session.client(**self.client_config) as client:
            response = await client.put_records(
                StreamName=self.stream_name,
                Records=records
            )
            return response

    async def describe_stream(self):
        async with self.session.client(**self.client_config) as client:
            response = await client.describe_stream(
                StreamName=self.stream_name
            )
            return response