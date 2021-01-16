from __future__ import absolute_import

import logging
from sentry_plugins.base import CorePluginMixin
from sentry.plugins.bases.data_forwarding import DataForwardingPlugin
from sentry.utils import metrics
from sentry.integrations import FeatureDescription, IntegrationFeatures
from sentry_bigquery.client import BigQueryClient

logger = logging.getLogger(__name__)

DESCRIPTION = """
Forward Sentry events to BigQuery.
"""


def track_response_metric(fn):
    def wrapper(*args, **kwargs):
        try:
            success = fn(*args, **kwargs)
            metrics.incr(
                "data-forwarding.http_response", tags={"plugin": "sentry_bigquery", "success": success}
            )
        except Exception:
            metrics.incr(
                "data-forwarding.http_response", tags={"plugin": "sentry_bigquery", "success": False}
            )
            raise
        return success

    return wrapper


class BigQueryPlugin(CorePluginMixin, DataForwardingPlugin):
    title = "BigQuery"
    slug = "bigquery"
    description = DESCRIPTION
    conf_key = "big-query"
    required_field = "queue_url"
    feature_descriptions = [
        FeatureDescription(
            """
            Forward Sentry errors and events to BigQuery.
            """,
            IntegrationFeatures.DATA_FORWARDING,
        )
    ]

    def get_config(self, project, **kwargs):
        return [
            {
                "name": "account_info",
                "label": "Account info",
                "type": "textarea",
                "required": True,
            },
            {
                "name": "project_id",
                "label": "Project ID",
                "type": "text",
                "required": True,
            },

        ]

    def get_rate_limit(self):
        return 0, 0

    @track_response_metric
    def forward_event(self, event, payload):
        logger.debug("Start forwarding event id '%s'" % event.event_id)

        project_id = self.get_option("project_id", event.project)
        account_info = self.get_option("account_info", event.project)

        logging_params = {
            "project_id": event.project_id,
            "organization_id": event.project.organization_id,
            "event_id": event.event_id,
            "issue_id": event.group_id
        }

        if not all((project_id, account_info)):
            logger.info("sentry_plugins.sentry_bigquery.skip_unconfigured", extra=logging_params)
            return

        try:
            client = BigQueryClient(project_id, account_info)
            table = client.get_table(event.project.name)
            client.insert_payload(table, payload)
        except Exception as e:
            logger.error(str(e))
            return False

        logger.debug("Success send event id '%s'" % event.event_id)
        return True
