_B='external-http'
_A='connect'
import json
from http.client import HTTPConnection,HTTPResponse,HTTPSConnection
from io import BytesIO
from typing import Collection
from opentelemetry.trace import SpanKind,get_tracer
from wrapt import ObjectProxy,wrap_function_wrapper
from detail.client import stack
from detail.client.attrs import build_attributes,format_otel_span_id,is_active,set_attributes
from detail.client.disable import DisableDetail
from detail.client.instrumentor import Instrumentor
from detail.client.logs import get_detail_logger
from detail.client.serialization import DetailEncoder
logger=get_detail_logger(__name__)
def get_head(raw_request):return raw_request.split(b'\r\n\r\n')[0]
def endheaders_wrapper(wrapped,connection,args,kwargs):
	res=wrapped(*args,**kwargs)
	if DisableDetail.is_disabled():return res
	caller_path=stack.get_caller_path()
	if stack.is_ignored_caller(caller_path):return res
	socket_proxy=connection.sock;request_data=b''.join(socket_proxy._self_buffer);request_head=get_head(request_data)
	with get_tracer('http').start_as_current_span(f"{connection._method} {connection.host} {connection.port}",kind=SpanKind.CLIENT)as span:
		if is_active(span):connection._detail_request_span_id=span.get_span_context().span_id;attrs=build_attributes(_B,{'method':connection._method,'host':connection.host,'port':connection.port,'request_head':json.dumps(request_head,cls=DetailEncoder)});set_attributes(span,attrs)
	socket_proxy._self_buffer=[];return res
def getresponse_wrapper(wrapped,connection,args,kwargs):
	if DisableDetail.is_disabled():return wrapped(*args,**kwargs)
	caller_path=stack.get_caller_path()
	if stack.is_ignored_caller(caller_path):return wrapped(*args,**kwargs)
	orig_response_class=connection.response_class
	class ConnectionResponse(connection.response_class):
		def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);self._connection=connection
	connection.response_class=ConnectionResponse;res=wrapped(*args,**kwargs);connection.response_class=orig_response_class;return res
def begin_wrapper(wrapped,response,args,kwargs):
	A=None
	if DisableDetail.is_disabled():return wrapped(*args,**kwargs)
	caller_path=stack.get_caller_path()
	if stack.is_ignored_caller(caller_path):return wrapped(*args,**kwargs)
	connection=getattr(response,'_connection',A)
	if connection is A:logger.warning('failed to patch through _connection; not tracing response');return wrapped(*args,**kwargs)
	if getattr(connection,'_detail_request_span_id',A)is A:logger.warning("getresponse span id wasn't available; not tracing response");return wrapped(*args,**kwargs)
	buffered_fp=BufferingProxy(response.fp);response.fp=buffered_fp;result=wrapped(*args,**kwargs);raw_headers=b''.join(buffered_fp._self_buffer);buffered_fp._self_buffer=[];body_length=response.length;response.read();response.length=body_length;raw_body=b''.join(buffered_fp._self_buffer);response.fp=BytesIO(raw_body);raw_response=raw_headers+raw_body
	with get_tracer('http').start_as_current_span(f"{connection._method} {connection.host} {connection.port}",kind=SpanKind.CLIENT)as span:
		if is_active(span):attrs=build_attributes(_B,{'request_span_id':format_otel_span_id(connection._detail_request_span_id),'response':json.dumps(raw_response,cls=DetailEncoder)});set_attributes(span,attrs)
	return result
class BufferingProxy(ObjectProxy):
	def __init__(self,wrapped):super().__init__(wrapped);self._self_buffer=[]
	def sendall(self,data):self._self_buffer.append(data);return self.__wrapped__.sendall(data)
	def readline(self,*args,**kwargs):r=self.__wrapped__.readline(*args,**kwargs);self._self_buffer.append(r);return r
	def read(self,*args,**kwargs):r=self.__wrapped__.read(*args,**kwargs);self._self_buffer.append(r);return r
	def readinto(self,buffer):
		num_bytes=self.__wrapped__.readinto(buffer)
		if num_bytes:self._self_buffer.append(buffer[-num_bytes:])
		return num_bytes
	def read1(self,*args,**kwargs):r=self.__wrapped__.read1(*args,**kwargs);self._self_buffer.append(r);return r
def connect_wrapper(wrapped,connection,args,kwargs):
	with DisableDetail():res=wrapped(*args,**kwargs)
	if DisableDetail.is_disabled():return res
	caller_path=stack.get_caller_path()
	if stack.is_ignored_caller(caller_path):return res
	socket_proxy=BufferingProxy(connection.sock);connection.sock=socket_proxy;return res
class HttpInstrumentor(Instrumentor):
	httplib_connection_methods=['endheaders',_A,'getresponse'];httplib_httpsconnection_methods=[_A];urllib3_connection_methods=[_A];httpresponse_methods=['begin']
	def instrumentation_dependencies(self):return[]
	def _instrument(self,**kwargs):
		A='_wrapper'
		for method in self.httplib_connection_methods:wrapper=globals()[method+A];wrap_function_wrapper(HTTPConnection,method,wrapper)
		for method in self.httplib_httpsconnection_methods:wrapper=globals()[method+A];wrap_function_wrapper(HTTPSConnection,method,wrapper)
		for method in self.httpresponse_methods:wrapper=globals()[method+A];wrap_function_wrapper(HTTPResponse,method,wrapper)
		try:from urllib3.connection import HTTPConnection as HTTPConnectionUrllib3,HTTPSConnection as HTTPSConnectionUrllib3
		except ImportError:pass
		else:
			for method in self.urllib3_connection_methods:wrapper=globals()[method+A];wrap_function_wrapper(HTTPConnectionUrllib3,method,wrapper);wrap_function_wrapper(HTTPSConnectionUrllib3,method,wrapper)
	def _uninstrument(self,**kwargs):0