##
## Hand-e project, 2024
## hostasphere python profiler api
## File description:
## tokens_usage.py
##

from . import session_pb2

import time

_token_usage: list[session_pb2.UsageAtTime] = []
_total_tokens: int = 0

def record_usage(usage: int):
    global _total_tokens
    _total_tokens += usage
    _token_usage.append(session_pb2.UsageAtTime(
        time=time.time(),
        memory_usage=usage
    ))

def get_tokens_usage() -> list[session_pb2.UsageAtTime]:
    return _token_usage

def get_total_tokens() -> int:
    return _total_tokens

def get_usage_at_time(time: float) -> session_pb2.UsageAtTime:
    if len(_token_usage) == 0:
        return None
    closest_usage = _token_usage[0]
    for usage in _token_usage:
        if abs(usage.time - time) < abs(closest_usage.time - time):
            closest_usage = usage
    return closest_usage
