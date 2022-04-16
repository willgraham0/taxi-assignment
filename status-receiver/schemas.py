from typing import Dict


def driver_changes_status(driver_id: str, driver_name: str, status: str, timestamp: float) -> Dict:
    return {
        "event": "DRIVER_CHANGES_STATUS",
        "driver": {
            "id": driver_id,
            "name": driver_name,
        },
        "status": status,
        "timestamp": timestamp,
    }
