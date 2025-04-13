import logging
from dapr.ext.workflow import WorkflowRuntime, DaprWorkflowContext
from dapr.ext.workflow.workflow_activity_context import WorkflowActivityContext

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("workflow")

wfr = WorkflowRuntime()

@wfr.activity(name="deliver_product")
def deliver_product(ctx: WorkflowActivityContext, payload: dict) -> str:
    logger.info(f"📦 Delivering product to payload {payload}")
    return f"Product delivered to {payload}"

@wfr.activity(name="notify_user")
def notify_user(ctx: WorkflowActivityContext, msg: str) -> str:
    logger.info(f"📬 Notifying user: {msg}")
    return "Notification sent"

@wfr.workflow(name="order_fulfillment_wf")
def order_fulfillment_workflow(ctx: DaprWorkflowContext, payload: dict):
    logger.info(f"🧭 Workflow started with payload: {payload}")
    result = yield ctx.call_activity(deliver_product, input=payload['data'])
    logger.info("🚚 Delivery finished")
    yield ctx.call_activity(notify_user, input=result)
    logger.info("📢 Notification sent")
    return {"status": "complete"}
