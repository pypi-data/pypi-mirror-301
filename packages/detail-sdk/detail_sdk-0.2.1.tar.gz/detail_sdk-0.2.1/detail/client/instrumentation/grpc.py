import json
from typing import Any
from google.protobuf.message import Message
from opentelemetry.instrumentation.grpc import GrpcInstrumentorClient
from detail.client.attrs import Attributes,build_attributes,is_active,set_attributes
from detail.client.serialization import DetailEncoder
def request_hook(span,request):
	if is_active(span):A={'request.message':json.dumps(request,cls=DetailEncoder)};B=build_attributes('grpc',A);set_attributes(span,B)
def response_hook(span,response):
	if is_active(span):A={'response.message':json.dumps(response,cls=DetailEncoder)};B=build_attributes('grpc',A);set_attributes(span,B)
class DetailGrpcClientInstrumentor(GrpcInstrumentorClient):
	def _instrument(B,**A):A['request_hook']=request_hook;A['response_hook']=response_hook;super()._instrument(**A)