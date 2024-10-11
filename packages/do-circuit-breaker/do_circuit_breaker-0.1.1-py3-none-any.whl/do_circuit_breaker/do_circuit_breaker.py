# do_circuit_breaker/do_circuit_breaker.py

import requests

class CircuitBreaker:
    def __init__(self, monitor_id, api_url='https://api.example.com/status', threshold=3):
        """
        Initialize the Circuit Breaker.
        
        :param monitor_id: The ID used to monitor the job.
        :param api_url: The API URL to fetch the job status.
        :param threshold: The number of consecutive failures to trigger the circuit breaker.
        """
        self.monitor_id = monitor_id
        self.api_url = api_url
        self.threshold = threshold
        self.failure_count = 0

    def _fetch_status(self):
        """
        Fetch the job status from the API.
        
        :return: A dictionary containing the status of the job.
        """
        response = requests.get(f"{self.api_url}/{self.monitor_id}")
        response.raise_for_status()
        return response.json()

    def should_continue(self):
        """
        Determine if the Airflow job should continue or break.
        
        :return: True if the job should continue, False otherwise.
        """
        try:
            status = self._fetch_status()
            if status.get('success'):
                self.failure_count = 0
                return True
            else:
                self.failure_count += 1
                if self.failure_count >= self.threshold:
                    return False
                return True
        except requests.RequestException as e:
            print(f"Error fetching status: {e}")
            self.failure_count += 1
            if self.failure_count >= self.threshold:
                return False
            return True
