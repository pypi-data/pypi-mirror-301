# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ........core.datetime_utils import serialize_datetime
from ........core.pydantic_utilities import deep_union_pydantic_dicts
from .....appointments.resources.v_1.types.mutable_appointment import MutableAppointment
from .....coverages.resources.v_1.types.mutable_coverage import MutableCoverage
from .....patients.resources.v_1.types.patient import Patient


class PatientListItem(pydantic.BaseModel):
    patient: Patient
    primary_coverage: typing.Optional[MutableCoverage] = None
    next_appointment: typing.Optional[MutableAppointment] = None

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
