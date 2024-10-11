from __future__ import annotations
import gc,json
from io import BytesIO
from typing import TYPE_CHECKING,Any
from urllib.parse import urlparse
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.trace import Span
from detail.client.attrs import Attributes,build_attributes,is_active,set_attributes
from detail.client.serialization import DetailEncoder
if TYPE_CHECKING:from django.http import HttpRequest,HttpResponse
class DetailDjangoInstrumentor(DjangoInstrumentor):
	def _instrument(B,**A):A['request_hook']=B.request_hook;A['response_hook']=B.response_hook;super()._instrument(**A)
	@staticmethod
	def request_hook(span,request):
		B=request;A=span
		if is_active(A):
			C=B._stream.read();B._stream=BytesIO(C);D={'request.body':C,'request.headers':json.dumps(list(B.headers.items()),cls=DetailEncoder)};E=A.attributes.get('http.url')
			if isinstance(E,str):D['target']=urlparse(E).path
			F=build_attributes('http',D);set_attributes(A,F)
	@staticmethod
	def response_hook(span,request,response):
		E='http.route';B=response;A=span
		if is_active(A):
			C={'status_code':B.status_code,'response.body':B.content};D=list(B.headers.items());D.extend([('Set-Cookie',A.output(header=''))for A in B.cookies.values()]);C['response.headers']=json.dumps(D,cls=DetailEncoder)
			if E in A.attributes:C['request.route']=A.attributes[E]
			F=build_attributes('http',C);set_attributes(A,F)
		gc.collect()