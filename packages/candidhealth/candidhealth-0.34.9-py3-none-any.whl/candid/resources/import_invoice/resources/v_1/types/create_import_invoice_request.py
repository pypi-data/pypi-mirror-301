# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ......core.datetime_utils import serialize_datetime
from ......core.pydantic_utilities import deep_union_pydantic_dicts
from .....commons.types.patient_external_id import PatientExternalId
from .....invoices.resources.v_2.types.invoice_item_create import InvoiceItemCreate
from .....invoices.resources.v_2.types.invoice_status import InvoiceStatus
from .....payment_account_configs.types.payment_account_config_id import PaymentAccountConfigId


class CreateImportInvoiceRequest(pydantic.BaseModel):
    external_payment_account_config_id: PaymentAccountConfigId
    patient_external_id: PatientExternalId
    external_customer_identifier: str = pydantic.Field()
    """
    Id of the customer in the source system
    """

    note: typing.Optional[str] = None
    due_date: typing.Optional[dt.date] = pydantic.Field(default=None)
    """
    If given as None, days_until_due in the payment config will be used to create a default date
    """

    items: typing.List[InvoiceItemCreate]
    status: InvoiceStatus
    external_identifier: str = pydantic.Field()
    """
    Id of the invoice being imported in the source system. Warning - This field CANNOT be updated.
    """

    customer_invoice_url: typing.Optional[str] = pydantic.Field(default=None)
    """
    Link to the patient view of the invoice in the third-party service
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
        extra = pydantic.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}
