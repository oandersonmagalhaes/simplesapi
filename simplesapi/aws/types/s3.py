from simplesapi.types import AWSSession

class S3:
    def __init__(self, session: AWSSession, bucket_name: str):
        self.bucket_name = bucket_name
        self.session = session
        self.client_config = {"service_name":"s3", "endpoint_url":"http://localhost:4566"} if session.aws_local else {"service_name":"s3"}

    async def upload_file(self, file_path: str, object_key: str):
        async with self.session.client(**self.client_config) as client:
            response = await client.upload_file(
                file_path,
                self.bucket_name,
                object_key
            )
            return response

    async def download_file(self, object_key: str, file_path: str):
        async with self.session.client(**self.client_config) as client:
            response = await client.download_file(
                self.bucket_name,
                object_key,
                file_path
            )
            return response

    async def delete_object(self, object_key: str):
        async with self.session.client(**self.client_config) as client:
            response = await client.delete_object(
                Bucket=self.bucket_name,
                Key=object_key
            )
            return response

    async def list_objects(self):
        async with self.session.client(**self.client_config) as client:
            response = await client.list_objects(
                Bucket=self.bucket_name
            )
            return response

    async def get_object(self, object_key: str):
        async with self.session.client('s3') as client:
            response = await client.get_object(
                Bucket=self.bucket_name,
                Key=object_key
            )
            return response
