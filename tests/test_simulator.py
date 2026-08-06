from unittest.mock import patch

import pytest
import requests
import logging

from src.simulator.config import BACKEND_URL
from src.simulator.simulator import generate_data, MAX_TEMP, update, MIN_TEMP, MAX_TEMP_DRIFT, send_packet

"""
Unit and integration tests for the telemetry simulator
This module tests mathematical drift logic, data structure generation and sending packets.
"""


def test_generate_data():
    """Ensures that the generated packet contains all required keys"""
    packet = generate_data()
    assert "packet_id" in packet
    assert packet["packet_id"] != ""
    assert "timestamp" in packet
    assert "thermal" in packet
    assert "temperature_c" in packet["thermal"]
    assert "power" in packet
    assert "voltage_v" in packet["power"]
    assert "current_ma" in packet["power"]
    assert "attitude" in packet
    assert "roll_deg" in packet["attitude"]
    assert "pitch_deg" in packet["attitude"]
    assert "yaw_deg" in packet["attitude"]


# We use the @patch to mock the built-in functions
# This replaces function call with our mock object
# By forcing a specific return value instead of a random number we make our
# tests predictable and reproducible

@patch("src.simulator.simulator.uniform")
def test_update_clamps_to_max(mock_uniform):
    """Verifies that sensor drift cannot exceed the predefined limits"""
    # Force the random drift to generate a huge positive number
    mock_uniform.return_value = 300.0
    val = MAX_TEMP - 10.0
    result = update(val, MAX_TEMP_DRIFT, MIN_TEMP, MAX_TEMP)
    assert result == MAX_TEMP


@patch("src.simulator.simulator.uniform")
def test_update_clamps_to_min(mock_uniform):
    """Verifies that sensor drift cannot fall below the predefined limits"""
    # Force the random drift to generate a huge negative number
    mock_uniform.return_value = -300.0
    val = MIN_TEMP + 10.0
    result = update(val, MAX_TEMP_DRIFT, MIN_TEMP, MAX_TEMP)
    assert result == MIN_TEMP


# Here we mock network calls
# Thanks to that our tests won't fail just because the real server is offline
# Moreover we can easily simulate edge cases (like Timeouts or 500 Server Errors)

@patch("src.simulator.simulator.requests.post")
def test_send_packet_success(mock_post, caplog):
    """
        Test the successful transmission of a telemetry packet
        Ensures that the correct URL, payload, and timeout are used
        and that no errors or warnings are logged
    """
    mock_post.return_value.status_code = 201
    packet = {"test": "data"}
    with caplog.at_level(logging.WARNING):
        send_packet(packet)

    mock_post.assert_called_once_with(BACKEND_URL, json=packet, timeout=2)
    mock_post.return_value.raise_for_status.assert_called_once()
    assert len(caplog.records) == 0


@patch("src.simulator.simulator.requests.post")
def test_send_packet_handles_timeout(mock_post, caplog):
    """
        Test network failure handling
        Simulates a Timeout exception to ensure the simulator logs the error
    """
    mock_post.side_effect = requests.exceptions.Timeout("Timeout")
    packet = {"test": "data"}

    with caplog.at_level(logging.WARNING):
        send_packet(packet)

    assert len(caplog.records) > 0
    assert "timed out" in caplog.text
    assert "Skipping send" in caplog.text
