import re

from typing import TYPE_CHECKING, Union


if TYPE_CHECKING:
    from snowflake.core.function import Function
    from snowflake.core.procedure import Procedure
    from snowflake.core.user_defined_function import UserDefinedFunction


def get_function_name_with_args(
    function: Union["Function", "Procedure", "UserDefinedFunction"]
) -> str:
    return f"{function.name}({','.join([str(argument.datatype) for argument in function.arguments])})"


FUNCTION_WITH_ARGS_PATTERN = re.compile(r"""^(\"([^\"]|\"\")+\"|[a-zA-Z_][a-zA-Z0-9_$]*)\(([A-Za-z,0-9_]*)\)$""")


def replace_function_name_in_name_with_args(
    name_with_args: str,
    new_name: str
) -> str:
    matcher = FUNCTION_WITH_ARGS_PATTERN.match(name_with_args)
    if not matcher:
        raise ValueError("Invalid function name with arguments")

    args = matcher.group(3)
    return f"{new_name}({args})"


def check_version_gte(version_to_check: str, reference_version: str) -> bool:
    cur_version = tuple(map(int, version_to_check.split(".")))
    req_version = tuple(map(int, reference_version.split(".")))

    return cur_version >= req_version


def check_version_lte(version_to_check: str, reference_version: str) -> bool:
    cur_version = tuple(map(int, version_to_check.split(".")))
    req_version = tuple(map(int, reference_version.split(".")))

    return cur_version <= req_version


def fix_hostname(
    hostname: str,
    account_locator: str,
) -> str:
    """Perform automatic hostname fixes.

    When a legacy format hostname is used to connect to Snowflake SSL certificates might not work as expected.
    For example if the legacy url format is used to connect to Snowflake (see
    https://docs.snowflake.com/en/user-guide/organizations-connect for more documentation) _ (underscores) should
    be replaced with - (dashes).
    """
    if hostname.startswith(account_locator) and "_" in account_locator:
        new_account_locator = account_locator.replace("_", "-")
        return new_account_locator + hostname[len(account_locator):]
    else:
        return hostname
