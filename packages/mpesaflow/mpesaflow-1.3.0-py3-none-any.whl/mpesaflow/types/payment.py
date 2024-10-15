# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Payment"]


class Payment(BaseModel):
    message: Optional[str] = None
    """Additional information about the transaction"""

    mpesa_request_id: Optional[str] = FieldInfo(alias="mpesaRequestId", default=None)
    """M-Pesa request identifier"""

    status: Optional[Literal["pending", "completed", "failed"]] = None
    """The status of the transaction"""

    transaction_id: Optional[str] = FieldInfo(alias="transactionId", default=None)
    """Unique identifier for the transaction"""
