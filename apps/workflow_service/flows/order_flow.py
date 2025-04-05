# apps/workflow_service/flows/order_flow.py

from dapr.ext.workflow import WorkflowRuntime

runtime = WorkflowRuntime()

@runtime.activity(name="ProcessPaymentActivity")
async def process_payment(ctx, order_id: str):
    print(f"[Activity] Processing payment for {order_id}")
    return True

@runtime.activity(name="CreateOrderRecordActivity")
async def create_order_record(ctx, order_id: str):
    print(f"[Activity] Creating order record for {order_id}")
    return f"record-{order_id}"

@runtime.activity(name="SendNotificationActivity")
async def send_notification(ctx, order_id: str):
    print(f"[Activity] Sending notification for {order_id}")
    return "notified"

@runtime.workflow(name="ChildWorkflow")
async def child_workflow(ctx, order_id: str):
    print(f"[ChildWorkflow] Starting for {order_id}")
    result = await ctx.call_activity("SendNotificationActivity", order_id)
    print(f"[ChildWorkflow] Done: {result}")
    return result

@runtime.workflow(name="OrderWorkflow")
async def order_workflow(ctx, order_id: str):
    print(f"[Workflow] Order processing started for: {order_id}")

    await ctx.call_activity("ProcessPaymentActivity", order_id)
    await ctx.call_activity("CreateOrderRecordActivity", order_id)

    # 呼叫子流程
    child_result = await ctx.call_child_workflow("ChildWorkflow", order_id)

    return {"status": "completed", "order_id": order_id, "notified": child_result}
