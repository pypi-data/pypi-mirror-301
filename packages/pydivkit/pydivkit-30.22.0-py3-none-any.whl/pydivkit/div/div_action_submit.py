# Generated code. Do not modify.
# flake8: noqa: F401, F405, F811

from __future__ import annotations

import enum
import typing

from pydivkit.core import BaseDiv, Expr, Field

from . import div_action


# Sends variables from the container via a url. The data sending configuration can
# be determined by the host application. By default, variables are passed in body
# in json format, the request method is POST.
class DivActionSubmit(BaseDiv):

    def __init__(
        self, *,
        type: str = "submit",
        container_id: typing.Optional[typing.Union[Expr, str]] = None,
        on_fail_actions: typing.Optional[typing.Sequence[div_action.DivAction]] = None,
        on_success_actions: typing.Optional[typing.Sequence[div_action.DivAction]] = None,
        request: typing.Optional[DivActionSubmitRequest] = None,
        **kwargs: typing.Any,
    ):
        super().__init__(
            type=type,
            container_id=container_id,
            on_fail_actions=on_fail_actions,
            on_success_actions=on_success_actions,
            request=request,
            **kwargs,
        )

    type: str = Field(default="submit")
    container_id: typing.Union[Expr, str] = Field(
        description=(
            "The identifier of the container that contains variables to "
            "submit."
        ),
    )
    on_fail_actions: typing.Optional[typing.Sequence[div_action.DivAction]] = Field(
        description="Actions in case of unsuccessful submit.",
    )
    on_success_actions: typing.Optional[typing.Sequence[div_action.DivAction]] = Field(
        description="Actions in case of successful submit.",
    )
    request: DivActionSubmitRequest = Field(
        description=(
            "The HTTP request parameters that are used to configure how "
            "data is sent."
        ),
    )


class DivActionSubmitParameter(BaseDiv):

    def __init__(
        self, *,
        name: typing.Optional[typing.Union[Expr, str]] = None,
        value: typing.Optional[typing.Union[Expr, str]] = None,
        **kwargs: typing.Any,
    ):
        super().__init__(
            name=name,
            value=value,
            **kwargs,
        )

    name: typing.Union[Expr, str] = Field(
    )
    value: typing.Union[Expr, str] = Field(
    )


DivActionSubmitParameter.update_forward_refs()


# The HTTP request parameters that are used to configure how data is sent.
class DivActionSubmitRequest(BaseDiv):

    def __init__(
        self, *,
        headers: typing.Optional[typing.Sequence[DivActionSubmitParameter]] = None,
        method: typing.Optional[typing.Union[Expr, RequestMethod]] = None,
        query_parameters: typing.Optional[typing.Sequence[DivActionSubmitParameter]] = None,
        url: typing.Optional[typing.Union[Expr, str]] = None,
        **kwargs: typing.Any,
    ):
        super().__init__(
            headers=headers,
            method=method,
            query_parameters=query_parameters,
            url=url,
            **kwargs,
        )

    headers: typing.Optional[typing.Sequence[DivActionSubmitParameter]] = Field(
        description="The HTTP request headers.",
    )
    method: typing.Optional[typing.Union[Expr, RequestMethod]] = Field(
        description="The HTTP request method.",
    )
    query_parameters: typing.Optional[typing.Sequence[DivActionSubmitParameter]] = Field(
        description="Query parameters.",
    )
    url: typing.Union[Expr, str] = Field(
        format="uri", 
        description="The url to which data from the container is sent.",
    )


class RequestMethod(str, enum.Enum):
    G_E_T = "GET"
    P_O_S_T = "POST"
    P_U_T = "PUT"
    P_A_T_C_H = "PATCH"
    D_E_L_E_T_E = "DELETE"
    H_E_A_D = "HEAD"
    O_P_T_I_O_N_S = "OPTIONS"


DivActionSubmitRequest.update_forward_refs()


DivActionSubmit.update_forward_refs()
