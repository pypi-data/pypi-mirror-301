# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ......core.datetime_utils import serialize_datetime
from ......core.pydantic_utilities import deep_union_pydantic_dicts
from .....commons.types.encounter_external_id import EncounterExternalId
from .....commons.types.organization_id import OrganizationId
from .....commons.types.patient_external_id import PatientExternalId
from .....commons.types.service_line_id import ServiceLineId
from .patient_payment_id import PatientPaymentId
from .patient_payment_source import PatientPaymentSource
from .patient_payment_status import PatientPaymentStatus


class PatientPayment(pydantic.BaseModel):
    """
    Examples
    --------
    import datetime
    import uuid

    from candid.resources.patient_payments.v_3 import (
        PatientPayment,
        PatientPaymentSource,
        PatientPaymentStatus,
    )

    PatientPayment(
        patient_payment_id="CF237BE1-E793-4BBF-8958-61D5179D1D0D",
        organization_id=uuid.UUID(
            "0788ca2a-b20d-4b8e-b8d4-07fa0b3b4907",
        ),
        source_internal_id="D1A76039-D5C5-4323-A2FC-B7C8B6AEF6A4",
        source=PatientPaymentSource.MANUAL_ENTRY,
        amount_cents=2000,
        payment_timestamp=datetime.datetime.fromisoformat(
            "2023-01-01 00:00:00+00:00",
        ),
        status=PatientPaymentStatus.PENDING,
        payment_name="John Doe",
        payment_note="test payment note",
        patient_external_id="B7437260-D6B4-48CF-B9D7-753C09F34E76",
        encounter_external_id="0F26B9C3-199F-4CBB-A166-B87EA7C631BB",
        service_line_id=uuid.UUID(
            "b557dc86-c629-478c-850a-02d45ac11783",
        ),
    )
    """

    patient_payment_id: PatientPaymentId
    organization_id: OrganizationId
    source_internal_id: str
    source: PatientPaymentSource
    amount_cents: int
    payment_timestamp: typing.Optional[dt.datetime] = None
    status: typing.Optional[PatientPaymentStatus] = None
    payment_name: typing.Optional[str] = None
    payment_note: typing.Optional[str] = None
    patient_external_id: typing.Optional[PatientExternalId] = None
    encounter_external_id: typing.Optional[EncounterExternalId] = None
    service_line_id: typing.Optional[ServiceLineId] = None

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
