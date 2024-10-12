"Methods to interact with the Metrics API"

from enum import Enum
from attr import define

import pendulum
import requests

from astro_observe_sdk.clients.config import AstroApiConfig, supply_config


class MetricCategory(Enum):
    """
    Enum to define the categories of metrics that can be logged.
    """

    BASIC = "BASIC"
    COST = "COST"
    CUSTOM = "CUSTOM"


@define
class Metric:
    asset_id: str
    deployment_id: str
    run_id: str
    category: MetricCategory
    name: str
    value: float
    timestamp: pendulum.DateTime | None = None

    @property
    def datetime_str(self) -> str | None:
        "Returns the timestamp formatted according to rf3339, if the timestamp exists."
        if not self.timestamp:
            return None

        return self.timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def to_dict(self) -> dict:
        return {
            "nodeFqdn": self.asset_id,
            "deploymentId": self.deployment_id,
            "runId": self.run_id,
            "category": self.category.value,
            "name": self.name,
            "value": self.value,
            "timestamp": self.timestamp,
        }


@supply_config
def log_metrics(metrics: list[Metric], config: AstroApiConfig) -> None:
    """
    Batch log metrics to the Metrics API.
    """
    url = f"{config.private_org_base_url}/metrics"
    response = requests.post(
        url, headers=config.headers, json=[metric.to_dict() for metric in metrics]
    )

    response.raise_for_status()


@supply_config
def log_metric(metric: Metric, config: AstroApiConfig) -> None:
    """
    Log a single metric to the Metrics API.
    """
    url = f"{config.private_org_base_url}/metrics"
    response = requests.post(url, headers=config.headers, json=metric.to_dict())

    response.raise_for_status()
