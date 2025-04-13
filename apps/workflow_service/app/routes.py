import logging

from dapr.ext.workflow import DaprWorkflowClient
from fastapi import APIRouter, Request
from starlette.responses import JSONResponse

from workflow import order_fulfillment_workflow

router = APIRouter()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@router.post("/workflow/payment-success")
async def start_workflow(request: Request):
    logger.info("start_workflow")
    body = await request.json()
    wf_client = DaprWorkflowClient()
    instance_id = wf_client.schedule_new_workflow(
        workflow=order_fulfillment_workflow,
        input=body,
    )
    logger.info(f"workflow id: {instance_id}")
    return {"workflow_id": instance_id}
