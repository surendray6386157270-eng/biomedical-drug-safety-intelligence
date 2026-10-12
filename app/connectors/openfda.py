from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import httpx


OPENFDA_ADVERSE_EVENT_URL = (
    "https://api.fda.gov/drug/event.json"
)


class OpenFDAError(Exception):
    """Base exception for openFDA connector errors."""


class OpenFDAConnectionError(OpenFDAError):
    """Raised when the openFDA service cannot be reached."""


class OpenFDAResponseError(OpenFDAError):
    """Raised when the openFDA response is malformed or invalid."""


class OpenFDAConnector:
    """Connector for retrieving adverse-event records from openFDA."""

    def __init__(
        self,
        base_url: str = OPENFDA_ADVERSE_EVENT_URL,
        timeout: float = 20.0,
    ) -> None:
        self.base_url = base_url
        self.timeout = timeout

    def search_drug(
        self,
        drug_name: str,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Search FAERS/openFDA adverse-event records for a drug."""

        if not drug_name or not drug_name.strip():
            raise ValueError("drug_name must not be empty")

        if limit < 1 or limit > 100:
            raise ValueError("limit must be between 1 and 100")

        query = f'patient.drug.medicinalproduct:"{drug_name.strip()}"'

        params = {
            "search": query,
            "limit": limit,
        }

        retrieved_at = datetime.now(timezone.utc)

        try:
            response = httpx.get(
                self.base_url,
                params=params,
                timeout=self.timeout,
            )
        except httpx.RequestError as exc:
            raise OpenFDAConnectionError(
                f"Unable to reach openFDA: {exc}"
            ) from exc

        if response.status_code == 404:
            return {
                "results": [],
                "total": 0,
                "retrieved_at": retrieved_at,
                "source": "FDA FAERS / openFDA",
                "source_url": str(response.url),
            }

        if response.status_code != 200:
            raise OpenFDAResponseError(
                f"openFDA returned HTTP {response.status_code}"
            )

        try:
            payload = response.json()
        except ValueError as exc:
            raise OpenFDAResponseError(
                "openFDA returned invalid JSON"
            ) from exc

        if not isinstance(payload, dict):
            raise OpenFDAResponseError(
                "openFDA response must be a JSON object"
            )

        results = payload.get("results")

        if results is None:
            results = []

        if not isinstance(results, list):
            raise OpenFDAResponseError(
                "openFDA 'results' must be a list"
            )

        return {
            "results": results,
            "total": payload.get("meta", {})
            .get("results", {})
            .get("total", len(results)),
            "retrieved_at": retrieved_at,
            "source": "FDA FAERS / openFDA",
            "source_url": str(response.url),
        }