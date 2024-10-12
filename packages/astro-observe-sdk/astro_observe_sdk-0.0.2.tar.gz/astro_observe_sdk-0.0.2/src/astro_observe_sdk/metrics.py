"User-facing methods to interact with the Metrics API"

import os
from typing import Unpack

import pendulum

from airflow.operators.python import get_current_context

from astro_observe_sdk.clients.config import TypedCommonConfig
from astro_observe_sdk.clients.metrics import Metric, MetricCategory
from astro_observe_sdk.clients.metrics import log_metric as _log_metric

from airflow.providers.openlineage.plugins.macros import lineage_run_id


def log_metric(
    name: str,
    value: float,
    asset_id: str | None = None,
    timestamp: pendulum.DateTime | None = None,
    **kwargs: Unpack[TypedCommonConfig],
) -> None:
    """
    Log a single metric to the Metrics API. Automatically pulls in task context.
    """
    context = get_current_context()
    task_instance = context.get("task_instance")
    if not task_instance:
        raise ValueError(
            "Task context not found. Please run this function within an Airflow task."
        )

    deployment_id = os.getenv("ASTRO_DEPLOYMENT_ID")
    if not deployment_id:
        raise ValueError(
            "Deployment ID not found. This should be automatically set by Astro."
        )

    namespace = os.getenv("ASTRO_DEPLOYMENT_NAMESPACE")
    dag_id = task_instance.dag_id
    task_id = task_instance.task_id

    asset_id = f"{namespace}.{dag_id}.{task_id}" if not asset_id else asset_id
    run_id = lineage_run_id(task_instance)

    metric = Metric(
        asset_id=asset_id,
        deployment_id=deployment_id,
        run_id=run_id,
        category=MetricCategory.CUSTOM,
        name=name,
        value=value,
        timestamp=timestamp,
    )

    _log_metric(metric, **kwargs)
