from benchling_api_client.v2.beta.api.audit import audit_log
from benchling_api_client.v2.beta.models.audit_log_export import AuditLogExport

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.models import AsyncTaskLink
from benchling_sdk.services.v2.base_service import BaseService


class V2BetaAuditService(BaseService):
    """
    V2-Beta Audit Service.

    Export audit log data for Benchling objects.

    https://benchling.com/api/v2-beta/reference#/Audit
    """

    @api_method
    def get_audit_log(self, object_id: str, export: AuditLogExport) -> AsyncTaskLink:
        """
        Export an audit log file for a Benchling object.

        This endpoint launches a long-running task and returns the Task ID of the
        launched task. The task response contains a link to download the exported audit
        log file from Amazon S3. This endpoint is subject to a rate limit of 500 requests
        per hour, in conjunction with the global request rate limit. Export throughput
        will additionally be rate limited around the scale of 70,000 total audit events
        exported in csv format or 30,000 total audit events exported in pdf format per hour.

        Example of submitting an export request and then getting the download URL from
        the completed task:

            task_link = benchling.v2.beta.audit.get_audit_log(object_id, export)
            task = benchling.tasks.wait_for_task(task_link.task_id)
            url = task.response["downloadURL"]

        See https://benchling.com/api/v2-beta/reference#/Audit/auditLog
        """
        response = audit_log.sync_detailed(client=self.client, object_id=object_id, json_body=export)
        return model_from_detailed(response)
