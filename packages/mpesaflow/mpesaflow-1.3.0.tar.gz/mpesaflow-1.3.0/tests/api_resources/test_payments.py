# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from mpesaflow import MpesaFlow, AsyncMpesaFlow
from tests.utils import assert_matches_type
from mpesaflow.types import PaymentPaybillResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPayments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_paybill(self, client: MpesaFlow) -> None:
        payment = client.payments.paybill(
            account_reference="accountReference",
            amount=0,
            phone_number="phoneNumber",
            transaction_desc="transactionDesc",
        )
        assert_matches_type(PaymentPaybillResponse, payment, path=["response"])

    @parametrize
    def test_raw_response_paybill(self, client: MpesaFlow) -> None:
        response = client.payments.with_raw_response.paybill(
            account_reference="accountReference",
            amount=0,
            phone_number="phoneNumber",
            transaction_desc="transactionDesc",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment = response.parse()
        assert_matches_type(PaymentPaybillResponse, payment, path=["response"])

    @parametrize
    def test_streaming_response_paybill(self, client: MpesaFlow) -> None:
        with client.payments.with_streaming_response.paybill(
            account_reference="accountReference",
            amount=0,
            phone_number="phoneNumber",
            transaction_desc="transactionDesc",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment = response.parse()
            assert_matches_type(PaymentPaybillResponse, payment, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncPayments:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_paybill(self, async_client: AsyncMpesaFlow) -> None:
        payment = await async_client.payments.paybill(
            account_reference="accountReference",
            amount=0,
            phone_number="phoneNumber",
            transaction_desc="transactionDesc",
        )
        assert_matches_type(PaymentPaybillResponse, payment, path=["response"])

    @parametrize
    async def test_raw_response_paybill(self, async_client: AsyncMpesaFlow) -> None:
        response = await async_client.payments.with_raw_response.paybill(
            account_reference="accountReference",
            amount=0,
            phone_number="phoneNumber",
            transaction_desc="transactionDesc",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        payment = await response.parse()
        assert_matches_type(PaymentPaybillResponse, payment, path=["response"])

    @parametrize
    async def test_streaming_response_paybill(self, async_client: AsyncMpesaFlow) -> None:
        async with async_client.payments.with_streaming_response.paybill(
            account_reference="accountReference",
            amount=0,
            phone_number="phoneNumber",
            transaction_desc="transactionDesc",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            payment = await response.parse()
            assert_matches_type(PaymentPaybillResponse, payment, path=["response"])

        assert cast(Any, response.is_closed) is True
