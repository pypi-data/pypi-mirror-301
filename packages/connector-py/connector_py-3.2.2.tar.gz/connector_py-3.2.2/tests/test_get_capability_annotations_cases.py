"""Test cases for ``get_capability_annotations`` function."""

import typing as t

import pytest_cases
from connector.serializers.request import (
    ConnectorSettings,
    Request,
    RequestData,
    ValidateCredentialsRequest,
)
from connector.serializers.response import Response, ResponseData, ValidateCredentialsResponse

Case: t.TypeAlias = tuple[
    t.Callable[[Request[RequestData, ConnectorSettings]], Response[ResponseData]],
    tuple[type[Request[RequestData, ConnectorSettings]], type[Response[ResponseData]]] | None,
]


@pytest_cases.case(tags=("correct",))
def case_correct_capability() -> Case:
    def capability(
        args: Request[ValidateCredentialsRequest, None],
    ) -> Response[ValidateCredentialsResponse]:
        return Response[ValidateCredentialsResponse](
            response=ValidateCredentialsResponse(valid=True),
            raw_data=None,
        )

    expected_annotations = (
        Request[ValidateCredentialsRequest, None],
        Response[ValidateCredentialsResponse],
    )
    return capability, expected_annotations


@pytest_cases.case(tags=("missing_annotation",))
def case_missing_argument_annotation() -> Case:
    def capability(args) -> Response[ValidateCredentialsResponse]:
        return Response[ValidateCredentialsResponse](
            response=ValidateCredentialsResponse(valid=True),
            raw_data=None,
        )

    return capability, None


@pytest_cases.case(tags=("missing_annotation",))
def case_missing_return_annotation() -> Case:
    def capability(args: Request[ValidateCredentialsRequest, None]):
        return Response[ValidateCredentialsResponse](
            response=ValidateCredentialsResponse(valid=True),
            raw_data=None,
        )

    return capability, None


@pytest_cases.case(tags=("missing_annotation",))
def case_missing_annotations() -> Case:
    def capability(args):
        return Response[ValidateCredentialsResponse](
            response=ValidateCredentialsResponse(valid=True),
            raw_data=None,
        )

    return capability, None
