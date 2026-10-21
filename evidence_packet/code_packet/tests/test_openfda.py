import httpx
import pytest

from app.connectors.openfda import (
    OpenFDAConnectionError,
    OpenFDAConnector,
    OpenFDAResponseError,
)


def test_rejects_empty_drug_name():
    connector = OpenFDAConnector()

    with pytest.raises(ValueError):
        connector.search_drug("")


def test_rejects_invalid_limit():
    connector = OpenFDAConnector()

    with pytest.raises(ValueError):
        connector.search_drug("aspirin", limit=0)


def test_handles_network_failure(monkeypatch):
    def mock_get(*args, **kwargs):
        raise httpx.ConnectError("connection failed")

    monkeypatch.setattr(httpx, "get", mock_get)

    connector = OpenFDAConnector()

    with pytest.raises(OpenFDAConnectionError):
        connector.search_drug("aspirin")


def test_handles_malformed_json(monkeypatch):
    class FakeResponse:
        status_code = 200
        url = "https://example.com"

        def json(self):
            raise ValueError("invalid json")

    monkeypatch.setattr(
        httpx,
        "get",
        lambda *args, **kwargs: FakeResponse(),
    )

    connector = OpenFDAConnector()

    with pytest.raises(OpenFDAResponseError):
        connector.search_drug("aspirin")


def test_handles_malformed_results(monkeypatch):
    class FakeResponse:
        status_code = 200
        url = "https://example.com"

        def json(self):
            return {
                "results": "not-a-list"
            }

    monkeypatch.setattr(
        httpx,
        "get",
        lambda *args, **kwargs: FakeResponse(),
    )

    connector = OpenFDAConnector()

    with pytest.raises(OpenFDAResponseError):
        connector.search_drug("aspirin")