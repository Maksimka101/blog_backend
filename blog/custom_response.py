import json
from enum import Enum
from typing import Any, Dict, NoReturn


class Status(Enum):

    OK = 'OK'

    DATA_ERROR = 'Error: Error in data on server'

    REQUEST_ERROR = 'Error: Error in request'

    SERVER_ERROR = 'Error: Error on server'


class CustomResponse:

    response_body: Dict[str, Any]

    response_status: Status

    response_message: str

    def __init__(self, response_body=None,
                 response_status: Status = Status.OK,
                 response_message: str = ''):
        if response_body is None:
            response_body = dict()
        self.response_body = response_body
        self.response_status = response_status
        self.response_message = response_message

    def status_from_bool(self, status: bool) -> NoReturn:
        self.response_status = Status.OK if status else Status.REQUEST_ERROR

    def to_dict(self) -> Dict[str, Any]:
        response = dict()
        response['status'] = self.response_status.value
        if self.response_message != '':
            response['response_message'] = self.response_message
        if self.response_body != dict():
            response['body'] = self.response_body
        return response

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
