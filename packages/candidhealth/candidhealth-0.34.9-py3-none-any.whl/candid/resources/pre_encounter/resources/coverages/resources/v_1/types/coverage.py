# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ........core.datetime_utils import serialize_datetime
from ........core.pydantic_utilities import deep_union_pydantic_dicts
from .....common.types.coverage_id import CoverageId
from .....common.types.organization_id import OrganizationId
from .....common.types.user_id import UserId
from .mutable_coverage import MutableCoverage


class Coverage(MutableCoverage):
    """
    A coverage object with immutable server-owned properties.
    """

    id: CoverageId
    organization_id: OrganizationId = pydantic.Field()
    """
    The organization that owns this coverage.
    """

    deactivated: bool = pydantic.Field()
    """
    True if the coverage is deactivated. Deactivated coverages are not returned in search results but are returned in all other endpoints including scan.
    """

    version: int = pydantic.Field()
    """
    The version of the coverage. Any update to any property of a coverage object will create a new version.
    """

    updated_at: dt.datetime
    updating_user_id: UserId = pydantic.Field()
    """
    The user ID of the user who last updated the coverage.
    """

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults_exclude_unset: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        kwargs_with_defaults_exclude_none: typing.Any = {"by_alias": True, "exclude_none": True, **kwargs}

        return deep_union_pydantic_dicts(
            super().dict(**kwargs_with_defaults_exclude_unset), super().dict(**kwargs_with_defaults_exclude_none)
        )

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True
        extra = pydantic.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}
