from datetime import datetime

from sentry.utils import json
from google.oauth2.service_account import Credentials
from google.cloud.bigquery import Client, SchemaField, Table


class BigQueryClient:
    """
    Args:
        project_id (str):
        account_info (str):
    """
    def __init__(self, project_id: str, account_info: str):
        self._project_id = project_id
        account_info = json.loads(account_info)
        credentials = Credentials.from_service_account_info(account_info)
        self._client = Client(project=project_id, credentials=credentials)

    """
    Args:
        name (str):
    Returns:
        google.cloud.bigquery.table.Table
    """
    def get_table(self, name: str):
        schema = [
            SchemaField("id", "STRING"),
            SchemaField("group_id", "STRING"),
            SchemaField("event_id", "STRING"),
            SchemaField("project_id", "STRING"),
            SchemaField("entries", "STRING"),
            SchemaField("message", "STRING"),
            SchemaField("title", "STRING"),
            SchemaField("user", "STRING"),
            SchemaField("contexts", "STRING"),
            SchemaField("sdk", "STRING"),
            SchemaField("context", "STRING"),
            SchemaField("tags", "STRING"),
            SchemaField("platform", "STRING"),
            SchemaField("errors", "STRING"),
            SchemaField("crashFile", "STRING"),
            SchemaField("created_at", "DATETIME", mode="REQUIRED"),
            SchemaField("raw_payload", "STRING", mode="REQUIRED"),
        ]

        table = Table('%s.%s' % (self._project_id, name), schema=schema)

        return self._client.create_table(table, exists_ok=True)

    """
    Args:
        name (google.cloud.bigquery.table.Table):
        payload (dict):
    """
    def insert_payload(self, table: Table, payload: dict):
        row = {
            "id": payload.get("id", ""),
            "group_id": payload.get("groupID", ""),
            "event_id": payload.get("eventID", ""),
            "project_id": payload.get("projectID", ""),
            "entries": json.dumps(payload.get("entries", "")),
            "message": payload.get("message", ""),
            "title": payload.get("title", ""),
            "user": json.dumps(payload.get("user", "")),
            "contexts": json.dumps(payload.get("contexts", "")),
            "context": json.dumps(payload.get("context", "")),
            "sdk": json.dumps(payload.get("sdk", "")),
            "tags": json.dumps(payload.get("tags", "")),
            "platform": payload.get("platform", ""),
            "errors": json.dumps(payload.get("errors", "")),
            "crashFile": payload.get("crashFile", ""),
            'created_at': datetime.now(),
            'raw_payload': json.dumps(payload),
        }
        self._client.insert_rows(table, [row])

