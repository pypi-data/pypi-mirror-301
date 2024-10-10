# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ....core.datetime_utils import serialize_datetime
from ....core.pydantic_utilities import deep_union_pydantic_dicts
from .identifier_base import IdentifierBase
from .identifier_id import IdentifierId


class Identifier(IdentifierBase):
    """
    Examples
    --------
    import uuid

    from candid import (
        Identifier,
        IdentifierCode,
        IdentifierValue_MedicareProviderIdentifier,
        State,
    )

    Identifier(
        identifier_id=uuid.UUID(
            "123e4567-e89b-12d3-a456-426614174000",
        ),
        identifier_code=IdentifierCode.MCR,
        identifier_value=IdentifierValue_MedicareProviderIdentifier(
            state=State.CA,
            provider_number="1234567890",
        ),
    )
    """

    identifier_id: IdentifierId

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
