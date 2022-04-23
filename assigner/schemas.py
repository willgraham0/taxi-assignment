from typing import Dict


def assign_customer_to_driver(customer_id: str, driver_id: str, timestamp: float) -> Dict:
    return {
        "event": "ASSIGN_CUSTOMER_TO_DRIVER",
        "customer": {
            "id": customer_id,
        },
        "driver": {
            "id": driver_id,
        },
        "timestamp": timestamp,
    }


def customer_request_rejected(request: Dict, timestamp: float) -> Dict:
    return {
        "event": "CUSTOMER_REQUEST_REJECTED",
        "request": request,
        "timestamp": timestamp,
    }
