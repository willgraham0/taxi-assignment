from typing import Dict


def customer_requests_taxi(customer_id: str, timestamp: float) -> Dict:
    return {
        "event": "CUSTOMER_REQUESTS_TAXI",
        "customer": {
            "id": customer_id,
        },
        "timestamp": timestamp,
    }
