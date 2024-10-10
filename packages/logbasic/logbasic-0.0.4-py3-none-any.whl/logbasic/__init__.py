import datetime as dt
import inspect
import json


import os
from typing import Any, Dict, Final

from .color_code import ColorCode
from .log_type_text import LogTypeText


DEBUGGING = False  # set either via this variable or via env var 'log_debugging'
LOG_DEBUGGING_ENV_VAR: Final = 'log_debugging'

####################
# COMMON FUNCTIONS #
####################


def debug(*args: list) -> None:
    debugging = bool(os.environ.get(LOG_DEBUGGING_ENV_VAR, '')) or DEBUGGING
    if debugging:
        format_and_print(ColorCode.grey, LogTypeText.debug, *args)


def warning(*args: list) -> None:
    format_and_print(ColorCode.yellow, LogTypeText.warning, *args)


def error(*args: list) -> None:
    format_and_print(ColorCode.bold_red, LogTypeText.error, *args)


def info(*args: list) -> None:
    format_and_print(ColorCode.reset, LogTypeText.info, *args)


def special(*args: list) -> None:
    format_and_print(ColorCode.purple_marked, LogTypeText.special, *args)


def success(*args: list) -> None:
    format_and_print(ColorCode.green, LogTypeText.success, *args)


#####################################
# FUNCTIONS TO GET FORMATTED STRING #
#####################################


def warning_string(*args: list) -> None:
    format(ColorCode.yellow, LogTypeText.warning, *args)


def error_string(*args: list) -> None:
    format(ColorCode.bold_red, LogTypeText.error, *args)


def info_string(*args: list) -> None:
    format(ColorCode.reset, LogTypeText.info, *args)


def debug_string(*args: list) -> None:
    debugging = bool(os.environ.get(LOG_DEBUGGING_ENV_VAR, 'false')) or DEBUGGING
    if debugging:
        format(ColorCode.grey, LogTypeText.debug, *args)


def special_string(*args: list) -> None:
    format(ColorCode.purple_marked, LogTypeText.special, *args)


def success_string(*args: list) -> None:
    format(ColorCode.green, LogTypeText.success, *args)


# Helper Functions


def format_and_print(color: ColorCode, log_type_text: LogTypeText, *args: list):
    print(format(color, log_type_text, *args))


def format(color: ColorCode, log_type_text: LogTypeText, *args: list):
    args_string = convert_args_to_str(*args)
    # time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # only want milliseconds so remove 3 last nums form nanoseconds
    time = format_datetime(dt.datetime.now())

    og_function_stack = inspect.stack()[3]
    function = og_function_stack[3]
    function = f'\\{function}()' if function != '<module>' else ''
    file = og_function_stack[1].rsplit('\\', 1)[-1]

    time_part = ColorCode.grey.add_to(time)
    log_type_part = color.add_to(f'[{log_type_text.value}]')
    added_space = ' ' * (log_type_text.n_max_chars - log_type_text.n_chars)
    file_function_part = ColorCode.grey.add_to(f'{file}{function}:')

    formatted_string = f'{time_part} {log_type_part} {added_space}{file_function_part}{color.add_to(args_string)}'

    return formatted_string


def convert_args_to_str(*args: list) -> str:
    result: str = ''
    for i in range(0, len(args)):
        arg = args[i]

        str_arg: str = format_on_type(arg)

        if i == 0:
            result = result + str_arg
        else:
            result = result + ' ' + str_arg
    return result


def format_on_type(arg: Any) -> str:
    if isinstance(arg, dict):
        result = format_dict(arg)
    elif isinstance(arg, dt.datetime):
        result = format_datetime(arg)
    elif isinstance(arg, dt.timedelta):
        result = format_timedelta(arg)
    else:
        result = str(arg)

    return result


def format_dict(dict: Dict) -> str:
    return json.dumps(dict, sort_keys=True, indent=4)


def format_timedelta(timedelta: dt.timedelta) -> str:
    if timedelta < dt.timedelta(0):
        return '-' + format_timedelta(-timedelta)
    else:
        # Change this to format positive timedeltas the way you want
        # return str(dt.timedelta(days=timedelta.days, seconds=timedelta.seconds))
        return str(timedelta)


def format_datetime(datetime: dt.datetime) -> str:
    # if datetime.tzinfo is None or datetime.tzinfo != dt.timezone.utc:
    # raise ValueError('datetime is not UTC!')
    if datetime.tzinfo is None:
        tz = ''
    else:
        utcoffset: dt.timedelta = datetime.tzinfo.utcoffset(datetime)  # type:ignore
        print(utcoffset)
        prefix = '+' if utcoffset.total_seconds() > 0 else '-'
        tz = f'{prefix}{format_timedelta(utcoffset)}'  # type:ignore

    timetuple = datetime.timetuple()
    day_of_the_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][timetuple[6]]
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][timetuple[1] - 1]

    return f'{day_of_the_week}, {str(timetuple[2]).zfill(2)} {month} {timetuple[0]}, {timetuple[3]}:{timetuple[4]}:{timetuple[5]}.{round(datetime.microsecond/10000)}{tz}'
