from fastapi.testclient import TestClient
from src.backend.main import app
import src.backend.main as main_module

"""
Integration tests for the FastAPI backend
This module uses FastAPI's TestClient to simulate HTTP requests to the API
ensuring that the endpoints correctly process incoming telemetry data
"""

client = TestClient(app)


def valid_packet():
    """Provides a valid telemetry packet"""
    from datetime import datetime, timezone
    return {
        "packet_id": "a3f1c",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "simulator",
        "thermal": {"temperature_c": 23.4},
        "power": {"voltage_v": 12.1, "current_ma": 480.0},
        "attitude": {"roll_deg": 1.2, "pitch_deg": -0.4, "yaw_deg": 0.0}
    }


def test_receive_packet_success():
    """
        Test receiving a valid packet
        Expects HTTP 201 and verifies that the packet is saved in memory
    """
    packet = valid_packet()
    main_module.latest_packet = {}
    response = client.post("/telemetry", json=packet)

    assert response.status_code == 201
    assert response.json() == {"status": "received"}
    assert main_module.latest_packet == packet


def test_receive_packet_error():
    """
        Test receiving an invalid packet.
        Expects HTTP 422 and verifies memory remains unchanged
    """
    packet = valid_packet()
    del packet["power"]
    main_module.latest_packet = {}
    response = client.post("/telemetry", json=packet)

    assert response.status_code == 422
    assert response.json() == {"error": "missing field: power"}
    assert main_module.latest_packet == {}
