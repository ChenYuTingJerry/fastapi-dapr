python -m grpc_tools.protoc -I. \
  --python_out=./apps/payment_service \
  --grpc_python_out=./apps/payment_service \
  ./proto/order.proto