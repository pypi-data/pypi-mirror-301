import os
import numpy as np
import socketio
import pandas as pd
from typing import Callable

from detectorclient.db import Database
from detectorclient.datasets import Dataset
from detectorclient.metrics import PerformanceMonitor, StepResult, TransactionMetrics


class DetectorClient:
    """
    A client for detecting fraud in transaction data using a specified handler.
    """

    def __init__(self, name: str, handler: Callable, dataset: Dataset, socket_io: socketio.Client = socketio.Client()):
        """
        Initialize the DetectorClient.

        Args:
            name (str): The name of the detector.
            handler (Callable): The function to process data.
            dataset (Dataset): The dataset to use.
            socket_io (socketio.Client): The Socket.IO client instance.
        """
        self.name = name
        self.handler = handler
        self.dataset = dataset
        self.socket = socket_io

        self.socket.on("connect", self.on_connect)
        self.socket.on("disconnect", self.on_disconnect)
        self.socket.on("step", self.on_start_step)

        if not self.socket.connected:
            socket_uri = os.environ.get("SOCKET_URI", "http://localhost:3000")
            self.socket.connect(socket_uri)

        self.db = Database()
        self.db.connect()

    def on_connect(self):
        print("Connected to server")
        self.socket.emit("register", self.name)

    def on_disconnect(self):
        print("Disconnected from server")

    def start(self):
        print("Started and waiting")
        self.socket.wait()

    def on_start_step(self, step: int):
        try:
            with self.db.Session() as session:
                txns = self._get_transactions(session, step)

            filtered_txns = txns.drop(columns=self.dataset.hidden_fields, axis="columns")
            with PerformanceMonitor() as monitor:
                handler_result = self.handler(filtered_txns)

            if not isinstance(handler_result, np.ndarray):
                raise TypeError("Handler must return a NumPy ndarray.")

            performance_metrics = monitor.get_metrics()
            transaction_metrics = self.calculate_metrics(txns, handler_result)
            result = StepResult(transaction_metrics, performance_metrics)
            self.socket.emit("finishedStep", result.to_dict())
        except Exception as e:
            print(f"Error processing step {step}: {e}")
            self.socket.emit("error", {"step": step, "error": str(e)})

    def _get_transactions(self, session, step: int) -> pd.DataFrame:
        column = getattr(self.dataset.sql_alchemy_model.__table__.c,
                         self.dataset.step_field)
        sql = (
            session.query(self.dataset.sql_alchemy_model)
            .filter(column == step)
            .statement
        )

        return pd.read_sql(sql, session.bind)  # type: ignore

    def calculate_metrics(
        self, df: pd.DataFrame, predictions: np.ndarray
    ) -> TransactionMetrics:
        if len(predictions) != len(df):
            raise ValueError("Length of predictions does not match the number of data samples.")
        actual_isfraud = df[self.dataset.fraud_field].values
        amounts = df[self.dataset.amount_field].values

        metrics = TransactionMetrics()
        metrics.true_positives = int(np.sum((predictions == 1) & (actual_isfraud == 1)))
        metrics.false_positives = int(
            np.sum((predictions == 1) & (actual_isfraud == 0))
        )
        metrics.true_negatives = int(np.sum((predictions == 0) & (actual_isfraud == 0)))
        metrics.false_negatives = int(
            np.sum((predictions == 0) & (actual_isfraud == 1))
        )
        metrics.total_transactions = len(df)
        metrics.blocked_amount = np.sum(amounts[(predictions == 1)])
        metrics.transacted_amount = np.sum(amounts[(predictions == 0)])
        metrics.lost_to_fraud = np.sum(
            amounts[(actual_isfraud == 1) & (predictions == 0)]
        )

        return metrics
