from typing import TypedDict, Callable, Any, Dict
from functools import wraps

class Headers(TypedDict):
    accept: str
    accept_encoding: str
    user_agent: str
    x_forwarded_for: str
    x_forwarded_proto: str
    x_request_id: str

class Http(TypedDict):
    headers: Headers
    method: str
    path: str

class Event(TypedDict):
    http: Http

class Context(TypedDict):
    activation_id: str
    api_host: str
    api_key: str
    deadline: int
    function_name: str
    function_version: str
    namespace: str
    request_id: str
