from concurrent import futures
import grpc

from apps.payment_service.proto import order_pb2_grpc
from proto import order_pb2


class PaymentServicer(order_pb2_grpc.PaymentServiceServicer):
    def ProcessPayment(self, request, context):
        print(f"[gRPC] Processing payment for order {request.order_id} amount {request.amount}")
        return order_pb2.PaymentResponse(success=True, message="Payment succeeded")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_pb2_grpc.add_PaymentServiceServicer_to_server(PaymentServicer(), server)
    server.add_insecure_port("[::]:50052")
    print("Starting gRPC Payment Server on port 50052...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()