import grpc
from concurrent import futures
from quant_proto import quant_pb2, quant_pb2_grpc, QuantAgentServicer


# Test for Protobuf message creation
def test_hello_request_creation():
    request = quant_pb2.HelloRequest(name="Alice")
    assert request.name == "Alice"


def test_hello_response_creation():
    response = quant_pb2.HelloResponse(message="Hello, Alice!")
    assert response.message == "Hello, Alice!"


# Test for Protobuf message serialization/deserialization
def test_hello_request_serialization():
    request = quant_pb2.HelloRequest(name="Bob")
    serialized_request = request.SerializeToString()
    assert isinstance(serialized_request, bytes)


def test_hello_request_deserialization():
    original_request = quant_pb2.HelloRequest(name="Charlie")
    serialized_request = original_request.SerializeToString()
    new_request = quant_pb2.HelloRequest()
    new_request.ParseFromString(serialized_request)
    assert new_request == original_request


def test_hello_response_serialization():
    response = quant_pb2.HelloResponse(message="Hi, Bob!")
    serialized_response = response.SerializeToString()
    assert isinstance(serialized_response, bytes)


def test_hello_response_deserialization():
    original_response = quant_pb2.HelloResponse(message="Hi, Charlie!")
    serialized_response = original_response.SerializeToString()
    new_response = quant_pb2.HelloResponse()
    new_response.ParseFromString(serialized_response)
    assert new_response == original_response


# Test for the presence of the service stub and servicer
def test_service_stub_presence():
    assert hasattr(quant_pb2_grpc, 'QuantAgentStub')
    assert hasattr(quant_pb2_grpc, 'QuantAgentServicer')


# Test for the gRPC server-side implementation
def test_say_hello_servicer():
    servicer = QuantAgentServicer()
    request = quant_pb2.HelloRequest(name="Alice")
    context = None  # In advanced tests, you can use a mock context
    response = servicer.SayHello(request, context)
    assert response.message == "Hello, Alice!"


# Test the full gRPC client-server interaction
def test_say_hello_grpc():
    # Start a gRPC server for testing
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    quant_pb2_grpc.add_QuantAgentServicer_to_server(QuantAgentServicer(), server)
    port = server.add_insecure_port('localhost:0')
    server.start()

    # Create a gRPC channel and stub
    with grpc.insecure_channel(f'localhost:{port}') as channel:
        stub = quant_pb2_grpc.QuantAgentStub(channel)
        request = quant_pb2.HelloRequest(name="Alice")
        response = stub.SayHello(request)

    assert response.message == "Hello, Alice!"
    server.stop(None)


# Test for edge cases and boundary conditions
def test_empty_name():
    request = quant_pb2.HelloRequest(name="")
    assert request.name == ""


def test_long_name():
    long_name = "a" * 1000  # Test with a very long name
    request = quant_pb2.HelloRequest(name=long_name)
    assert request.name == long_name
