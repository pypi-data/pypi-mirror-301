# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ......core.datetime_utils import serialize_datetime
from ......core.pydantic_utilities import deep_union_pydantic_dicts


class RateEntry(pydantic.BaseModel):
    """
    A rate value in cents for a specific time range. Rate entries can be deactivated, which is set by using the deelte_rate endpoint. Deactivated rate entries are not considered when matching against service lines.

    Examples
    --------
    import datetime

    from candid.resources.fee_schedules.v_3 import RateEntry

    RateEntry(
        start_date=datetime.date.fromisoformat(
            "2024-04-11",
        ),
        rate_cents=33000,
        is_deactivated=False,
    )
    """

    start_date: dt.date
    end_date: typing.Optional[dt.date] = None
    rate_cents: int
    is_deactivated: bool

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
        extra = pydantic.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}
