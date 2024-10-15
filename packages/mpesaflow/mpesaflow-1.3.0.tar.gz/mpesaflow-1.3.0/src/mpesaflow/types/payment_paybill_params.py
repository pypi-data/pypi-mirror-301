# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["PaymentPaybillParams"]


class PaymentPaybillParams(TypedDict, total=False):
    account_reference: Required[Annotated[str, PropertyInfo(alias="accountReference")]]
    """A reference for the transaction"""

    amount: Required[float]
    """The amount to be paid"""

    phone_number: Required[Annotated[str, PropertyInfo(alias="phoneNumber")]]
    """The phone number of the payer"""

    transaction_desc: Required[Annotated[str, PropertyInfo(alias="transactionDesc")]]
    """A description of the transaction"""
