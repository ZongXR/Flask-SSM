# -*- coding: utf-8 -*-
import inspect
from functools import wraps
from pydantic import ValidationError
from flask_ssm.utils.type_utils import validate_params, validate_value_with_type, to_json


class Validated:
    def __init__(self, func):
        wraps(func)(self)
        self.func = func

    def __call__(self, *args, **kwargs):
        kwargs.update(dict(zip(inspect.signature(self.func).parameters.keys(), args)))
        kwargs, errors = validate_params(self.func, kwargs)
        if errors:
            raise TypeError(f"参数类型校验出错: {str(errors)}")
        result = self.func(**kwargs)
        try:
            if "return" in self.func.__annotations__.keys():
                return validate_value_with_type(self.func.__annotations__["return"], result)
            else:
                return result
        except ValidationError as e:
            raise TypeError(f"返回值类型校验出错: {str(e.errors()[0])}")
