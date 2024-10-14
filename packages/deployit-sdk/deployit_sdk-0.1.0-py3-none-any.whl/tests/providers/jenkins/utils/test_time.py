import pytest

from deployit.providers.jenkins.utils.time import convert_duration, convert_timestamp


@pytest.mark.parametrize(
    "unix_time, expected_time",
    [
        (
            1725148800000,
            "2024-08-31 21:00:00",
        ),  # 2024-09-01 00:00:00 UTC, adjusted for UTC-3
        (
            1672531200000,
            "2022-12-31 21:00:00",
        ),  # 2023-01-01 00:00:00 UTC, adjusted for UTC-3
        (
            0,
            "1969-12-31 21:00:00",
        ),  # Unix epoch (1970-01-01 00:00:00 UTC), adjusted for UTC-3
    ],
)
def test_convert_timestamp(unix_time, expected_time):
    assert convert_timestamp(unix_time) == expected_time


@pytest.mark.parametrize(
    "duration_ms, expected_duration",
    [
        (60000, "1m 0s"),  # 1 minute
        (90000, "1m 30s"),  # 1 minute 30 seconds
        (0, "0m 0s"),  # 0 milliseconds
        (315000, "5m 15s"),  # 5 minutes 15 seconds
    ],
)
def test_convert_duration(duration_ms, expected_duration):
    assert convert_duration(duration_ms) == expected_duration
