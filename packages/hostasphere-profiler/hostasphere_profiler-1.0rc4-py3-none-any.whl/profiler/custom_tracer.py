##
## Hand-e project, 2024
## hostasphere python profiler api
## File description:
## custom_tracer.py
##

from .tokens_usage import record_usage
from abc import ABC, abstractmethod
from typing import Callable


class CustomTracer(ABC):
    @abstractmethod
    def inspect_func(self, func: Callable) -> dict[str, str]:
        pass


class OpenHostaTracer(CustomTracer):
    def inspect_func(self, func: Callable) -> dict[str, str]:
        result = {}
        if hasattr(func, "_last_request"):
            result["_last_request"] = getattr(func, "_last_request")
        if hasattr(func, "_last_response"):
            _last_response = getattr(func, "_last_response")
            result["_last_response"] = _last_response
            record_usage(_last_response["usage"]["total_tokens"])
        return result


_tracer_registry = {
    "openhosta": OpenHostaTracer(),
}


def get_tracer(tracer_name: str) -> CustomTracer:
    return _tracer_registry[tracer_name]


def call_custom_tracers(func: Callable) -> dict[str, dict[str, str]]:
    result = {}
    for tracer in _tracer_registry.values():
        result[tracer.__class__.__name__] = tracer.inspect_func(func)
    return result
