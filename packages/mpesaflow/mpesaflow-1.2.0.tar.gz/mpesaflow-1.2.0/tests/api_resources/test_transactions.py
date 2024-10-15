# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from mpesaflow import MpesaFlow, AsyncMpesaFlow
from tests.utils import assert_matches_type
from mpesaflow.types import TransactionStatus, TransactionListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTransactions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: MpesaFlow) -> None:
        transaction = client.transactions.retrieve(
            "transactionId",
        )
        assert_matches_type(TransactionStatus, transaction, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: MpesaFlow) -> None:
        response = client.transactions.with_raw_response.retrieve(
            "transactionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transaction = response.parse()
        assert_matches_type(TransactionStatus, transaction, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: MpesaFlow) -> None:
        with client.transactions.with_streaming_response.retrieve(
            "transactionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transaction = response.parse()
            assert_matches_type(TransactionStatus, transaction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: MpesaFlow) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            client.transactions.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: MpesaFlow) -> None:
        transaction = client.transactions.list()
        assert_matches_type(TransactionListResponse, transaction, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: MpesaFlow) -> None:
        response = client.transactions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transaction = response.parse()
        assert_matches_type(TransactionListResponse, transaction, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: MpesaFlow) -> None:
        with client.transactions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transaction = response.parse()
            assert_matches_type(TransactionListResponse, transaction, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTransactions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncMpesaFlow) -> None:
        transaction = await async_client.transactions.retrieve(
            "transactionId",
        )
        assert_matches_type(TransactionStatus, transaction, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncMpesaFlow) -> None:
        response = await async_client.transactions.with_raw_response.retrieve(
            "transactionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transaction = await response.parse()
        assert_matches_type(TransactionStatus, transaction, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncMpesaFlow) -> None:
        async with async_client.transactions.with_streaming_response.retrieve(
            "transactionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transaction = await response.parse()
            assert_matches_type(TransactionStatus, transaction, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncMpesaFlow) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transaction_id` but received ''"):
            await async_client.transactions.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncMpesaFlow) -> None:
        transaction = await async_client.transactions.list()
        assert_matches_type(TransactionListResponse, transaction, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncMpesaFlow) -> None:
        response = await async_client.transactions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transaction = await response.parse()
        assert_matches_type(TransactionListResponse, transaction, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncMpesaFlow) -> None:
        async with async_client.transactions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transaction = await response.parse()
            assert_matches_type(TransactionListResponse, transaction, path=["response"])

        assert cast(Any, response.is_closed) is True
