# pa-proto

python3 -m grpc_tools.protoc -I proto --python_out=. --pyi_out=. --grpc_python_out=. com/hayatapps/pa/service/model/service.proto

python setup.py sdist bdist_wheel
pip install hayatapps_pa_proto-0.1-py3-none-any.whl
pip install hayatapps_pa_proto-0.1-py3-none-any.whl --force-reinstall