# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class CoverageStatus(str, enum.Enum):
    """
    enum to represent the statuses defined at https://build.fhir.org/valueset-fm-status.html
    """

    ACTIVE = "ACTIVE"
    CANCELLED = "CANCELLED"
    DRAFT = "DRAFT"
    ENTERED_IN_ERROR = "ENTERED_IN_ERROR"

    def visit(
        self,
        active: typing.Callable[[], T_Result],
        cancelled: typing.Callable[[], T_Result],
        draft: typing.Callable[[], T_Result],
        entered_in_error: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is CoverageStatus.ACTIVE:
            return active()
        if self is CoverageStatus.CANCELLED:
            return cancelled()
        if self is CoverageStatus.DRAFT:
            return draft()
        if self is CoverageStatus.ENTERED_IN_ERROR:
            return entered_in_error()
