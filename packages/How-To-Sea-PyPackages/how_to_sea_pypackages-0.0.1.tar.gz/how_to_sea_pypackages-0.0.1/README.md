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