from contextlib import contextmanager
import grpc

from briton.errors import HTTPException


@contextmanager
def grpc_error_handling():
    try:
        yield 
    except grpc.RpcError as rpc_error:
        # Handle gRPC errors here
        status_code = rpc_error.code()
        details = rpc_error.details()
        print(f"gRPC error: {status_code}, {details}")
        
        if status_code == grpc.StatusCode.UNAVAILABLE:
            print("Server is unavailable, please try again later.")
        elif status_code == grpc.StatusCode.INTERNAL:
            print("Internal server error occurred.")
        else:
            print(f"An unexpected error occurred: {status_code}")
        raise HTTPException(status_code=500, detail="Briton error during inference")
