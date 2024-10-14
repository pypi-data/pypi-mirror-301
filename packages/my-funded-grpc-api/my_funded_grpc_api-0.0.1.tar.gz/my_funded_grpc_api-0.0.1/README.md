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
from my_funded_grpc_api_proto.v1 import trading_pb2, trading_pb2_grpc

# Example: Create a TradingAccountCashBalance message
balance = trading_pb2.TradingAccountCashBalance(
    trading_account_id="123456",
    balance=1000.00,
    realized_pnl=50.00,
    broker="ExampleBroker"
)

# Use the message in your gRPC client code
# ...
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