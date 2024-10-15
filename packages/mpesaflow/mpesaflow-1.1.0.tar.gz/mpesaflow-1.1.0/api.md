# Payments

Types:

```python
from mpesaflow.types import PaymentPaybillResponse
```

Methods:

- <code title="post /paybill">client.payments.<a href="./src/mpesaflow/resources/payments.py">paybill</a>(\*\*<a href="src/mpesaflow/types/payment_paybill_params.py">params</a>) -> <a href="./src/mpesaflow/types/payment_paybill_response.py">PaymentPaybillResponse</a></code>

# Transactions

Types:

```python
from mpesaflow.types import TransactionStatus, TransactionListResponse
```

Methods:

- <code title="get /transaction-status/{transactionId}">client.transactions.<a href="./src/mpesaflow/resources/transactions.py">retrieve</a>(transaction_id) -> <a href="./src/mpesaflow/types/transaction_status.py">TransactionStatus</a></code>
- <code title="get /transactions">client.transactions.<a href="./src/mpesaflow/resources/transactions.py">list</a>() -> <a href="./src/mpesaflow/types/transaction_list_response.py">TransactionListResponse</a></code>
