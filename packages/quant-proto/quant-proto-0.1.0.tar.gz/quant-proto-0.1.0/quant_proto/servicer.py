from quant_proto import quant_pb2, quant_pb2_grpc


class QuantAgentServicer(quant_pb2_grpc.QuantAgentServicer):
    def SayHello(self, request, context):
        response = quant_pb2.HelloResponse(message=f"Hello, {request.name}!")
        return response
