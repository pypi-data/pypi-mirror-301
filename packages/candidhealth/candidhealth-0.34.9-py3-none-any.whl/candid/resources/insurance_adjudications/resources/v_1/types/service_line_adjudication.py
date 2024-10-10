# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ......core.datetime_utils import serialize_datetime
from ......core.pydantic_utilities import deep_union_pydantic_dicts
from .....service_lines.resources.v_2.types.denial_reason_content import DenialReasonContent
from .....x_12.resources.v_1.types.claim_adjustment_reason_code import ClaimAdjustmentReasonCode
from .....x_12.resources.v_1.types.remittance_advice_remark_code import RemittanceAdviceRemarkCode
from .service_line_adjudication_id import ServiceLineAdjudicationId


class ServiceLineAdjudication(pydantic.BaseModel):
    service_line_adjudication_id: ServiceLineAdjudicationId
    denial_reason: typing.Optional[DenialReasonContent] = pydantic.Field(default=None)
    """
    Will be treated as a denial if present
    """

    insurance_allowed_amount_cents: typing.Optional[int] = None
    insurance_paid_amount_cents: typing.Optional[int] = None
    deductible_amount_cents: typing.Optional[int] = None
    coinsurance_amount_cents: typing.Optional[int] = None
    copay_amount_cents: typing.Optional[int] = None
    carcs: typing.List[ClaimAdjustmentReasonCode]
    rarcs: typing.List[RemittanceAdviceRemarkCode]

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
