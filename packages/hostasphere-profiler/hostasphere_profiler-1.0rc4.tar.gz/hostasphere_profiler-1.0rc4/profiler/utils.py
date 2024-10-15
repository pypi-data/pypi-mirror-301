##
## Hand-e project, 2024
## hostasphere python profiler api
## File description:
## utils.py
##

import ast
import copy
import hashlib
import inspect
import os

import psutil

from . import profiler_output_pb2 as profiler_output


def get_function_name(func):
    return func.__name__


def get_func_params(args, func):
    result = []
    sig = inspect.signature(func)
    params = sig.parameters
    for i, arg in enumerate(args):
        arg_name = list(params.keys())[i] if i < len(params) else 'N/A'
        result.append(profiler_output.FuncParams(
            arg=str(arg),
            arg_name=arg_name,
            type=type(arg).__name__
        ))
    return result


def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss


def get_cpu_usage():
    process = psutil.Process(os.getpid())
    return process.cpu_percent()


def deep_copy_args(args):
    result = []
    for arg in args:
        try:
            result.append(copy.deepcopy(arg))
        except Exception:
            result.append(copy.copy(arg))
    return result


def get_source_code(func):
    try:
        source_code = inspect.getsource(func)
    except:
        source_code = "No source code available"
    return source_code


def hash_function(source_code):
    return hashlib.sha256(source_code.encode('utf-8')).hexdigest()


def is_function_pure(source_code):
    try:
        tree = ast.parse(source_code)

        class PurityVisitor(ast.NodeVisitor):
            def __init__(self):
                self.is_pure = True

            def visit_Assign(self, node):
                for target in node.targets:
                    if isinstance(target, ast.Name) and isinstance(target.ctx, ast.Store):
                        pass
                self.generic_visit(node)

            def visit_Call(self, node):
                if not (isinstance(node.func, ast.Name) and node.func.id == "emulate"):
                    self.is_pure = False
                self.generic_visit(node)

        visitor = PurityVisitor()
        visitor.visit(tree)

        return visitor.is_pure

    except SyntaxError:
        return False
