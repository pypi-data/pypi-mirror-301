##
## Hand-e project, 2024
## hostasphere python profiler api
## File description:
## core.py
##

import atexit
import threading
import time
import traceback

import grpc

from . import profiler_output_pb2_grpc as profiler_output_grpc, token_pb2
from .custom_tracer import call_custom_tracers
from .session import Session
from .token import token_exists
from .utils import *


class Profiler:
    def __init__(self, address: str, token: str, refresh_interval: float = 0.1,
                 session_tag: str = ''):
        self.refresh_interval = refresh_interval
        self._address = address
        self._token = token
        token_res: token_pb2.ExistsTokenResponse = token_exists(self._token, self._address)
        if token_res is None:
            raise Exception("Invalid address, target is not a hostaspere server")
        if not token_res.exists:
            raise Exception("Invalid token")
        self._token_id = token_res.id
        self._session = Session(self._address, self._token, self._token_id, self.refresh_interval, session_tag)
        atexit.register(self._session.end_session)

    def sendProfilerOutput(self, profiler_data: profiler_output.ProfilerOutput):
        try:
            with grpc.insecure_channel(self._address) as channel:
                stub = profiler_output_grpc.ProfilerStub(channel)
                profiler_data.token = self._token
                response = stub.SendProfilerOutput(profiler_data)
            if not response.ok:
                raise Exception(
                    f"Error sending profiler output: {response.message}")
        except grpc.RpcError:
            raise Exception(
                "Impossible to send profiler output check address, or check if hostaspere is running")

    def sendProfilerOutputAsync(self, profiler_data: profiler_output.ProfilerOutput):
        thread = threading.Thread(target=self.sendProfilerOutput, args=(profiler_data,))
        thread.start()

    def track(self):
        def decorator(func):
            def wrapper(*args, **kwargs):
                copied_args = deep_copy_args(args)
                self._session.record_usage()
                start_time = time.time()
                start_date = int(time.time() * 1000)
                stack = traceback.extract_stack()
                callers = []
                for f in stack[:-1]:
                    callers.append(profiler_output.FuncCaller(
                        caller_file=f[0],
                        caller_line=f[1],
                        caller=f[2]
                    ))
                result = func(*args, **kwargs)
                setattr(wrapper, "_last_response", func._last_response)
                setattr(wrapper, "_last_request", func._last_request)

                custom_tracer_data = call_custom_tracers(func)

                self._session.record_usage()
                end_time = time.time()
                end_date = int(time.time() * 1000)

                returned_value = profiler_output.ReturnedValue(
                    value=str(result),
                    type=type(result).__name__
                )

                source_code = get_source_code(func)

                custom_tracer_data_map = {}
                for key, value_dict in custom_tracer_data.items():
                    string_map = profiler_output.StringMap()
                    for sub_key, sub_value in value_dict.items():
                        string_map.data[sub_key] = str(sub_value)
                    custom_tracer_data_map[key] = string_map

                profiler_data = profiler_output.ProfilerOutputRequest(
                    profiler_output=profiler_output.ProfilerOutput(
                        function_name=get_function_name(func),
                        function_id=hash_function(source_code),
                        function_callers=callers,
                        token_id=self._token_id,
                        start_time=start_time,
                        start_date=start_date,
                        end_time=end_time,
                        end_date=end_date,
                        execution_time=(end_time - start_time) * 1000,  # in ms
                        memory_usage=get_memory_usage(),
                        cpu_usage=get_cpu_usage(),
                        func_params=get_func_params(copied_args, func),
                        returned_value=returned_value,
                        session_uuid=self._session.metrics.session_uuid,
                        source_code=source_code,
                        is_pure_function=is_function_pure(source_code),
                        custom_tracer_data=custom_tracer_data_map
                    )
                )
                self.sendProfilerOutputAsync(profiler_data)
                return result

            return wrapper

        return decorator

    def get_session(self):
        return self._session
