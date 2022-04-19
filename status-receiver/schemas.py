from typing import Dict


def driver_changes_status(driver_id: str, status: str, timestamp: float) -> Dict:
    return {
        "event": "DRIVER_CHANGES_STATUS",
        "driver": {
            "id": driver_id,
        },
        "status": status,
        "timestamp": timestamp,
    }
