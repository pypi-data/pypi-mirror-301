# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["TransactionStatus"]


class TransactionStatus(BaseModel):
    result_desc: Optional[str] = FieldInfo(alias="resultDesc", default=None)
    """Detailed description of the transaction result"""

    status: Optional[Literal["pending", "completed", "failed"]] = None
    """The current status of the transaction"""

    transaction_id: Optional[str] = FieldInfo(alias="transactionId", default=None)
    """Unique identifier for the transaction"""
