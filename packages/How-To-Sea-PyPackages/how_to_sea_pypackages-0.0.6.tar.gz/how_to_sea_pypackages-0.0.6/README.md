# Introduction
This repository contains the python bindings for gRPC Services used in the How To Sea project. gRPC is used in the project for inter-service communications, and as such is an internal API.

Several services are likely to be clients of another one. To prevent code duplication in re-implementing the gRPC client stub in each of these services, we have packaged these implementations, and are available on PyPi.

Note: This package is hosted on the public PyPi server. If it were to contain sensitive information, a private PyPi server would be set up to maintain privacy.

# Structure


## Python implementation
You will need the following 
```
grpcio~=1.66
grpcio-tools~=1.66
```

Generate the python bindings with
```bash
python -m grpc_tools.protoc -I./proto --python_out=./proto --pyi_out=./proto --grpc_python_out=./proto ./proto/<filename>.proto
```