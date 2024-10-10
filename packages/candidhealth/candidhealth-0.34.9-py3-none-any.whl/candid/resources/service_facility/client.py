# This file was auto-generated by Fern from our API Definition.

import typing
from json.decoder import JSONDecodeError

from ...core.api_error import ApiError
from ...core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ...core.jsonable_encoder import jsonable_encoder
from ...core.pydantic_utilities import pydantic_v1
from ...core.request_options import RequestOptions
from .types.encounter_service_facility import EncounterServiceFacility
from .types.encounter_service_facility_update import EncounterServiceFacilityUpdate
from .types.service_facility_id import ServiceFacilityId

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class ServiceFacilityClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def update(
        self,
        service_facility_id: ServiceFacilityId,
        *,
        request: EncounterServiceFacilityUpdate,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> EncounterServiceFacility:
        """
        Parameters
        ----------
        service_facility_id : ServiceFacilityId

        request : EncounterServiceFacilityUpdate

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        EncounterServiceFacility

        Examples
        --------
        import uuid

        from candid import EncounterServiceFacilityUpdate, State, StreetAddressLongZip
        from candid.client import CandidApiClient

        client = CandidApiClient(
            client_id="YOUR_CLIENT_ID",
            client_secret="YOUR_CLIENT_SECRET",
        )
        client.service_facility.update(
            service_facility_id=uuid.UUID(
                "d5e9c84f-c2b2-4bf4-b4b0-7ffd7a9ffc32",
            ),
            request=EncounterServiceFacilityUpdate(
                organization_name="Test Organization",
                address=StreetAddressLongZip(
                    address_1="123 Main St",
                    address_2="Apt 1",
                    city="New York",
                    state=State.NY,
                    zip_code="10001",
                    zip_plus_four_code="1234",
                ),
            ),
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"api/service_facility/v2/{jsonable_encoder(service_facility_id)}",
            base_url=self._client_wrapper.get_environment().candid_api,
            method="PATCH",
            json=request,
            request_options=request_options,
            omit=OMIT,
        )
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(EncounterServiceFacility, _response_json)  # type: ignore
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncServiceFacilityClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def update(
        self,
        service_facility_id: ServiceFacilityId,
        *,
        request: EncounterServiceFacilityUpdate,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> EncounterServiceFacility:
        """
        Parameters
        ----------
        service_facility_id : ServiceFacilityId

        request : EncounterServiceFacilityUpdate

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        EncounterServiceFacility

        Examples
        --------
        import asyncio
        import uuid

        from candid import EncounterServiceFacilityUpdate, State, StreetAddressLongZip
        from candid.client import AsyncCandidApiClient

        client = AsyncCandidApiClient(
            client_id="YOUR_CLIENT_ID",
            client_secret="YOUR_CLIENT_SECRET",
        )


        async def main() -> None:
            await client.service_facility.update(
                service_facility_id=uuid.UUID(
                    "d5e9c84f-c2b2-4bf4-b4b0-7ffd7a9ffc32",
                ),
                request=EncounterServiceFacilityUpdate(
                    organization_name="Test Organization",
                    address=StreetAddressLongZip(
                        address_1="123 Main St",
                        address_2="Apt 1",
                        city="New York",
                        state=State.NY,
                        zip_code="10001",
                        zip_plus_four_code="1234",
                    ),
                ),
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"api/service_facility/v2/{jsonable_encoder(service_facility_id)}",
            base_url=self._client_wrapper.get_environment().candid_api,
            method="PATCH",
            json=request,
            request_options=request_options,
            omit=OMIT,
        )
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(EncounterServiceFacility, _response_json)  # type: ignore
        raise ApiError(status_code=_response.status_code, body=_response_json)
