# Python Detector Client API

The Detector SDK is a Python library for building and evaluating fraud detection models in a simulated environment. It provides a client interface to connect to a simulation server, process transaction data, and report performance metrics.

## Installation

```bash
pip install detectorclient
```

## Quick Start
```py
from detectorclient import DetectorClient
from detectorclient.datasets import PaySimDataset

def fraud_detector(df):
    # Your fraud detection logic here
    return predictions

client = DetectorClient(
    name="MyDetector",
    handler=fraud_detector,
    dataset=PaySimDataset()
)

client.start()
```

### DetectorClient

The main class for interacting with the simulation server.

#### Constructor

```python
DetectorClient(name: str, handler: Callable, dataset: Dataset, socket_io: socketio.Client = socketio.Client())
```

- `name`: A unique identifier for your detector.
- `handler`: A function that takes a pandas DataFrame and returns fraud predictions.
- `dataset`: A Dataset object defining the structure of the transaction data.
- `socket_io`: (Optional) A custom SocketIO client instance.

#### Methods

- `start()`: Starts the client and waits for events from the server.

### Dataset

Base class for defining the structure of transaction datasets.

#### Available Datasets

- `PaySimDataset`: A dataset based on the PaySim simulation.

### Database

Handles database connections and queries.

### Metrics

- `TransactionMetrics`: Stores metrics related to fraud detection performance.
- `PerformanceMetrics`: Stores metrics related to computational performance.
- `PerformanceMonitor`: A context manager for measuring CPU and memory usage.

## Usage

1. Import the necessary components:

```python
from detectorclient import DetectorClient
from detectorclient.datasets import PaySimDataset
```

2. Define your fraud detection function:

```python
def fraud_detector(df):
    # Your fraud detection logic here
    return predictions
```

3. Create a DetectorClient instance:

```python
client = DetectorClient(
    name="MyDetector",
    handler=fraud_detector,
    dataset=PaySimDataset()
)
```

4. Start the client:

```python
client.start()
```

The client will automatically connect to the simulation server, process transaction data as it arrives, and report performance metrics.

## Environment Variables

- `SOCKET_URI`: The URI of the simulation server (default: `"http://localhost:3000"`)
- `DATABASE_URI`: The URI of the MySQL database (default: `"root:password@localhost/simulator"`)

## Notes

- Ensure that you have a MySQL database set up and accessible with the provided credentials.
- The simulation server should be running and accessible at the specified `SOCKET_URI`.


## Creating a New Dataset Using the SDK

To create a new dataset for use with the Fraud Detection Simulator, you'll need to define a new class that inherits from the `Dataset` base class. This process involves mapping your dataset's structure to a SQLAlchemy model and specifying key fields for the simulation.

### Steps to Create a New Dataset

1. Import necessary modules:

```python
from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
from detectorclient.datasets import Dataset

Base = declarative_base()
```

2. Define a SQLAlchemy model that represents your dataset's structure:

```python
class _YourDatasetModel(Base):
    __tablename__ = 'your_dataset_name'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # Define other columns based on your dataset structure
    # Example:
    timestamp = Column(Integer)
    transaction_type = Column(String(255))
    amount = Column(Numeric(16, 2))
    sender = Column(String(255))
    receiver = Column(String(255))
    is_fraud = Column(Integer)
    # Add more fields as necessary
```

3. Create a new class that inherits from `Dataset`:

```python
class YourDataset(Dataset):
    def __init__(self):
        super().__init__(
            sql_alchemy_model=_YourDatasetModel,
            fraud_field='is_fraud',
            amount_field='amount',
            step_field='timestamp',
            hidden_fields=['id', 'timestamp', 'is_fraud']
        )
```

### Key Parameters in Dataset Initialization

- `sql_alchemy_model`: The SQLAlchemy model class you defined for your dataset.
- `fraud_field`: The name of the column indicating whether a transaction is fraudulent.
- `amount_field`: The name of the column containing the transaction amount.
- `step_field`: The name of the column representing the time step or timestamp.
- `hidden_fields`: A list of field names that should be hidden from the fraud detection algorithm.

### Example: Creating a Custom Dataset

Here's an example of how to create a custom dataset for a credit card transaction dataset:

```python
from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base
from detectorclient.datasets import Dataset

Base = declarative_base()

class _CreditCardTransactionModel(Base):
    __tablename__ = 'credit_card_transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_datetime = Column(DateTime)
    card_number = Column(String(16))
    merchant_name = Column(String(255))
    merchant_category = Column(String(50))
    amount = Column(Numeric(10, 2))
    location = Column(String(255))
    is_fraud = Column(Integer)

class CreditCardDataset(Dataset):
    def __init__(self):
        super().__init__(
            sql_alchemy_model=_CreditCardTransactionModel,
            fraud_field='is_fraud',
            amount_field='amount',
            step_field='transaction_datetime',
            hidden_fields=['id', 'transaction_datetime', 'is_fraud', 'card_number']
        )
```

### Using Your Custom Dataset

Once you've defined your custom dataset, you can use it with the `DetectorClient`:

```python
from detectorclient import DetectorClient
from your_module import CreditCardDataset

def fraud_detector(df):
    # Your fraud detection logic here
    return predictions

client = DetectorClient(
    name="CreditCardFraudDetector",
    handler=fraud_detector,
    dataset=CreditCardDataset()
)

client.start()
```

Remember to update the database schema and import process to match your new dataset structure, as described in the "Changing the Dataset" section of this guide.
