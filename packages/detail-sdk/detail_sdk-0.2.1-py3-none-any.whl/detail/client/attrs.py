_A=False
import json,os,threading,typing
from typing import Any
from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.trace import Span
from opentelemetry.trace.span import format_span_id
from opentelemetry.util.types import AttributeValue
from typing_extensions import TypeGuard
from detail.client import logs
from detail.client.context import ThreadIndex,WsgiSpanId
from detail.client.instrumentation import NS
from detail.client.serialization import DetailEncoder
logger=logs.get_detail_logger(__name__)
Attributes=typing.MutableMapping[(str,AttributeValue)]
class AttributedSpan(ReadableSpan):
	@property
	def attributes(self):A=super().attributes;assert A;return A
def is_active(span):
	B=True;A=span
	if not A.is_recording():logger.warning('span %r is not recording and may cause tracing information to be lost',A,stack_info=B);return _A
	if not isinstance(A,ReadableSpan):logger.warning('span %r is unreadable and may cause tracing information to be lost',A,stack_info=B);return _A
	if A.attributes is None:logger.warning('span %r has None attributes and may cause tracing information to be lost',A,stack_info=B);return _A
	return B
def format_otel_span_id(int_span_id):return f"0x{format_span_id(int_span_id)}"
def build_attributes(library,library_attrs):
	A=library;B={f"{NS}.library":A,f"{NS}.context.thread_index":ThreadIndex.get(),f"{NS}.context.thread_id":threading.get_ident(),f"{NS}.context.pid":os.getpid(),f"{NS}.context.ppid":os.getppid(),f"{NS}.context.wsgi_span_id":WsgiSpanId.get()or''}
	for(C,D)in library_attrs.items():B[f"{NS}.{A}.{C}"]=D
	return B
def build_pure_attributes(library,qualname,args,kwargs,result,caller_path,empty_args=_A):C=empty_args;B=kwargs;A=args;A,B=(tuple(),{})if C else(A,B);return build_attributes(library,{'qualname':qualname,'args':json.dumps(A,cls=DetailEncoder),'kwargs':json.dumps(B,cls=DetailEncoder),'emptied':C,'return':json.dumps(result,cls=DetailEncoder),'callerpath':caller_path})
def set_attributes(span,attrs):
	for(A,B)in attrs.items():span.set_attribute(A,B)