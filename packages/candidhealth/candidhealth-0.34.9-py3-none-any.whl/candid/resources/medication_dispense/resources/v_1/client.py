# This file was auto-generated by Fern from our API Definition.

import typing
from json.decoder import JSONDecodeError

from .....core.api_error import ApiError
from .....core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from .....core.pydantic_utilities import pydantic_v1
from .....core.request_options import RequestOptions
from ....commons.errors.entity_not_found_error import EntityNotFoundError
from ....commons.errors.http_request_validation_error import HttpRequestValidationError
from ....commons.types.entity_not_found_error_message import EntityNotFoundErrorMessage
from ....commons.types.request_validation_error import RequestValidationError
from ....encounters.resources.v_4.errors.encounter_external_id_uniqueness_error import (
    EncounterExternalIdUniquenessError,
)
from ....encounters.resources.v_4.errors.encounter_patient_control_number_uniqueness_error import (
    EncounterPatientControlNumberUniquenessError,
)
from ....encounters.resources.v_4.errors.schema_instance_validation_http_failure import (
    SchemaInstanceValidationHttpFailure,
)
from ....encounters.resources.v_4.types.encounter import Encounter
from ....encounters.resources.v_4.types.encounter_external_id_uniqueness_error_type import (
    EncounterExternalIdUniquenessErrorType,
)
from ....encounters.resources.v_4.types.encounter_patient_control_number_uniqueness_error_type import (
    EncounterPatientControlNumberUniquenessErrorType,
)
from ....encounters.resources.v_4.types.schema_instance_validation_failure import SchemaInstanceValidationFailure
from .types.medication_dispense_create import MedicationDispenseCreate

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class V1Client:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def create(
        self, *, request: MedicationDispenseCreate, request_options: typing.Optional[RequestOptions] = None
    ) -> Encounter:
        """
        Parameters
        ----------
        request : MedicationDispenseCreate

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        Encounter

        Examples
        --------
        import datetime

        from candid import ProcedureModifier, ServiceLineUnits
        from candid.client import CandidApiClient
        from candid.resources.medication_dispense.v_1 import MedicationDispenseCreate
        from candid.resources.service_lines.v_2 import (
            DrugIdentification,
            MeasurementUnitCode,
            ServiceIdQualifier,
        )

        client = CandidApiClient(
            client_id="YOUR_CLIENT_ID",
            client_secret="YOUR_CLIENT_SECRET",
        )
        client.medication_dispense.v_1.create(
            request=MedicationDispenseCreate(
                medication_dispense_external_id="string",
                patient_external_id="string",
                procedure_code="string",
                quantity="string",
                units=ServiceLineUnits.MJ,
                date_of_service=datetime.date.fromisoformat(
                    "2023-01-15",
                ),
                drug_identification=DrugIdentification(
                    service_id_qualifier=ServiceIdQualifier.EAN_UCC_13,
                    national_drug_code="string",
                    national_drug_unit_count="string",
                    measurement_unit_code=MeasurementUnitCode.MILLILITERS,
                    link_sequence_number="string",
                    pharmacy_prescription_number="string",
                    conversion_formula="string",
                    drug_description="string",
                ),
                description="string",
                modifiers=[ProcedureModifier.TWENTY_TWO],
            ),
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "api/medication-dispense/v1",
            base_url=self._client_wrapper.get_environment().candid_api,
            method="POST",
            json=request,
            request_options=request_options,
            omit=OMIT,
        )
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(Encounter, _response_json)  # type: ignore
        if "errorName" in _response_json:
            if _response_json["errorName"] == "HttpRequestValidationError":
                raise HttpRequestValidationError(
                    pydantic_v1.parse_obj_as(RequestValidationError, _response_json["content"])  # type: ignore
                )
            if _response_json["errorName"] == "EncounterExternalIdUniquenessError":
                raise EncounterExternalIdUniquenessError(
                    pydantic_v1.parse_obj_as(EncounterExternalIdUniquenessErrorType, _response_json["content"])  # type: ignore
                )
            if _response_json["errorName"] == "EncounterPatientControlNumberUniquenessError":
                raise EncounterPatientControlNumberUniquenessError(
                    pydantic_v1.parse_obj_as(EncounterPatientControlNumberUniquenessErrorType, _response_json["content"])  # type: ignore
                )
            if _response_json["errorName"] == "EntityNotFoundError":
                raise EntityNotFoundError(
                    pydantic_v1.parse_obj_as(EntityNotFoundErrorMessage, _response_json["content"])  # type: ignore
                )
            if _response_json["errorName"] == "SchemaInstanceValidationHttpFailure":
                raise SchemaInstanceValidationHttpFailure(
                    pydantic_v1.parse_obj_as(SchemaInstanceValidationFailure, _response_json["content"])  # type: ignore
                )
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncV1Client:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def create(
        self, *, request: MedicationDispenseCreate, request_options: typing.Optional[RequestOptions] = None
    ) -> Encounter:
        """
        Parameters
        ----------
        request : MedicationDispenseCreate

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        Encounter

        Examples
        --------
        import asyncio
        import datetime

        from candid import ProcedureModifier, ServiceLineUnits
        from candid.client import AsyncCandidApiClient
        from candid.resources.medication_dispense.v_1 import MedicationDispenseCreate
        from candid.resources.service_lines.v_2 import (
            DrugIdentification,
            MeasurementUnitCode,
            ServiceIdQualifier,
        )

        client = AsyncCandidApiClient(
            client_id="YOUR_CLIENT_ID",
            client_secret="YOUR_CLIENT_SECRET",
        )


        async def main() -> None:
            await client.medication_dispense.v_1.create(
                request=MedicationDispenseCreate(
                    medication_dispense_external_id="string",
                    patient_external_id="string",
                    procedure_code="string",
                    quantity="string",
                    units=ServiceLineUnits.MJ,
                    date_of_service=datetime.date.fromisoformat(
                        "2023-01-15",
                    ),
                    drug_identification=DrugIdentification(
                        service_id_qualifier=ServiceIdQualifier.EAN_UCC_13,
                        national_drug_code="string",
                        national_drug_unit_count="string",
                        measurement_unit_code=MeasurementUnitCode.MILLILITERS,
                        link_sequence_number="string",
                        pharmacy_prescription_number="string",
                        conversion_formula="string",
                        drug_description="string",
                    ),
                    description="string",
                    modifiers=[ProcedureModifier.TWENTY_TWO],
                ),
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "api/medication-dispense/v1",
            base_url=self._client_wrapper.get_environment().candid_api,
            method="POST",
            json=request,
            request_options=request_options,
            omit=OMIT,
        )
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(Encounter, _response_json)  # type: ignore
        if "errorName" in _response_json:
            if _response_json["errorName"] == "HttpRequestValidationError":
                raise HttpRequestValidationError(
                    pydantic_v1.parse_obj_as(RequestValidationError, _response_json["content"])  # type: ignore
                )
            if _response_json["errorName"] == "EncounterExternalIdUniquenessError":
                raise EncounterExternalIdUniquenessError(
                    pydantic_v1.parse_obj_as(EncounterExternalIdUniquenessErrorType, _response_json["content"])  # type: ignore
                )
            if _response_json["errorName"] == "EncounterPatientControlNumberUniquenessError":
                raise EncounterPatientControlNumberUniquenessError(
                    pydantic_v1.parse_obj_as(EncounterPatientControlNumberUniquenessErrorType, _response_json["content"])  # type: ignore
                )
            if _response_json["errorName"] == "EntityNotFoundError":
                raise EntityNotFoundError(
                    pydantic_v1.parse_obj_as(EntityNotFoundErrorMessage, _response_json["content"])  # type: ignore
                )
            if _response_json["errorName"] == "SchemaInstanceValidationHttpFailure":
                raise SchemaInstanceValidationHttpFailure(
                    pydantic_v1.parse_obj_as(SchemaInstanceValidationFailure, _response_json["content"])  # type: ignore
                )
        raise ApiError(status_code=_response.status_code, body=_response_json)
