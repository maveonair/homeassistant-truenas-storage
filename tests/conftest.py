from typing import Any, Generator
from unittest.mock import MagicMock, patch

import pytest

pytest_plugins = "pytest_homeassistant_custom_component"


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(
    enable_custom_integrations,
) -> Generator[None, Any, None]:
    yield


@pytest.fixture
def mock_truenas_api_response() -> Generator[MagicMock, Any, None]:
    with patch("custom_components.truenas_storage.api.TrueNASAPI.get_pools") as mock:
        mock.return_value = [
            {
                "name": "tank",
                "guid": "123",
                "allocated": 6 * 1024**4,  # 6TB
                "free": 4 * 1024**4,  # 4TB
                "size": 10 * 1024**4,  # 10TB
            }
        ]
        yield mock
