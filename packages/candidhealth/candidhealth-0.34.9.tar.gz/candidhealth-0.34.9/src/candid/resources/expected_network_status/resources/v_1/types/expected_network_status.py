# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class ExpectedNetworkStatus(str, enum.Enum):
    IN_NETWORK = "in_network"
    OUT_OF_NETWORK = "out_of_network"
    UNKNOWN = "unknown"

    def visit(
        self,
        in_network: typing.Callable[[], T_Result],
        out_of_network: typing.Callable[[], T_Result],
        unknown: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is ExpectedNetworkStatus.IN_NETWORK:
            return in_network()
        if self is ExpectedNetworkStatus.OUT_OF_NETWORK:
            return out_of_network()
        if self is ExpectedNetworkStatus.UNKNOWN:
            return unknown()
