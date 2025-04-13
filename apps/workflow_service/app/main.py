from fastapi import FastAPI
from routes import router
from workflow import wfr, order_fulfillment_workflow, deliver_product, notify_user

app = FastAPI()
app.include_router(router)

# wfr.register_workflow(order_fulfillment_workflow)
# wfr.register_activity(deliver_product)
# wfr.register_activity(notify_user)
wfr.start()