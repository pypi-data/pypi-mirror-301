# MyFunded gRPC API Proto Python Package

This package contains the Python-generated code from the Protocol Buffer definitions for the MyFunded gRPC API.

## Installation

You can install this package using pip:

```bash
pip install my-funded-grpc-api-proto
```

To install a specific version:

```bash
pip install my-funded-grpc-api-proto==2023.05.15-1234567
```

Replace `2023.05.15-1234567` with the actual version you want to install.

## Usage

After installation, you can import and use the generated classes in your Python code. Here's a basic example:

```python
import time

from google.protobuf.timestamp_pb2 import Timestamp
from trading_account.v1 import cash_balance_pb2

message = cash_balance_pb2.TradingAccountCashBalanceMessage(
    event=cash_balance_pb2.TradingAccountCashBalanceEvent(
        event_type=cash_balance_pb2.EVENT_TYPE_CREATED,
        entity_type=cash_balance_pb2.ENTITY_TYPE_TRADING_ACCOUNT_CASH_BALANCE,
        environment=cash_balance_pb2.ENVIRONMENT_LIVE,
        stage=cash_balance_pb2.STAGE_EVALUATION,
        entity=cash_balance_pb2.TradingAccountCashBalance(
            trading_account_id="acc123",
            balance=10000.50,
            date=Timestamp().FromSeconds(int(time.time())),
            realized_pnl=500.75,
            environment=cash_balance_pb2.ENVIRONMENT_LIVE,
            stage=cash_balance_pb2.STAGE_EVALUATION,
            broker="TestBroker"
        ),
    ),
    topic="trading/cash_balance"
)

print(message)
```
```shell
event {
  event_type: EVENT_TYPE_CREATED
  entity_type: ENTITY_TYPE_TRADING_ACCOUNT_CASH_BALANCE
  environment: ENVIRONMENT_LIVE
  stage: STAGE_EVALUATION
  entity {
    trading_account_id: "acc123"
    balance: 10000.5
    realized_pnl: 500.75
    environment: ENVIRONMENT_LIVE
    stage: STAGE_EVALUATION
    broker: "TestBroker"
  }
}
topic: "trading/cash_balance"
```

## Available Modules

The package includes the following modules:

- `my_funded_grpc_api_proto.v1.trading_pb2`: Contains message classes
- `my_funded_grpc_api_proto.v1.trading_pb2_grpc`: Contains gRPC service classes

(Add more modules as necessary)

## Development

This package is automatically generated from the Protocol Buffer definitions in the [MyFunded gRPC API Proto repository](https://github.com/MyFunded/my-funded-grpc-api-proto). If you need to make changes, please submit a pull request to that repository.

## License

[Specify your license here]

## Contact

For any questions or issues, please [open an issue](https://github.com/MyFunded/my-funded-grpc-api-proto/issues) on the GitHub repository.