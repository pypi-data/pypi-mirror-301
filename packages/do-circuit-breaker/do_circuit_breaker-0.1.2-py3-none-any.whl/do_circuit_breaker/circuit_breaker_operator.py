# circuit_breaker_operator.py

from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from do_circuit_breaker import CircuitBreaker
from airflow.exceptions import AirflowException

class CircuitBreakerOperator(BaseOperator):
    @apply_defaults
    def __init__(self, monitor_id, threshold=3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.monitor_id = monitor_id
        self.threshold = threshold

    def execute(self, context):
        circuit_breaker = CircuitBreaker(self.monitor_id, self.threshold)
        if not circuit_breaker.should_continue():
            raise AirflowException(f"Circuit breaker triggered for monitor ID {self.monitor_id}.")
