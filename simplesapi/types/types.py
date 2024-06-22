from abc import ABC
import aioboto3


class Database(ABC):
    def __init__(self): ...


class AWSSession(aioboto3.Session):
    def __init__(self, aws_local: bool, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aws_local = aws_local
