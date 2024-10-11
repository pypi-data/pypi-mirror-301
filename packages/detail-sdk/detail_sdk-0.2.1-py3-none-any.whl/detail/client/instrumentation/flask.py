_A='__call__'
import gc,json
from typing import Any
import flask
from flask import Response,request
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.utils import unwrap
from opentelemetry.trace import SpanKind,get_current_span,get_tracer
from wrapt import wrap_function_wrapper
from detail.client import sentry
from detail.client.attrs import Attributes,build_attributes,format_otel_span_id,is_active,set_attributes
from detail.client.context import ThreadIndex,WsgiSpanId
from detail.client.logs import get_detail_logger
from detail.client.serialization import DetailEncoder
logger=get_detail_logger(__name__)
def before_request():
	C='http.route';A=get_current_span()
	if is_active(A):
		B={'request.body':json.dumps(request.get_data(),cls=DetailEncoder),'request.headers':json.dumps(request.headers.to_wsgi_list(),cls=DetailEncoder)}
		if C in A.attributes:B['request.route']=A.attributes[C]
		D=build_attributes('http',B);set_attributes(A,D)
def after_request(response):A=response;B=get_current_span();C=build_attributes('http',{'status_code':A.status_code,'response.headers':json.dumps(A.headers.to_wsgi_list(),cls=DetailEncoder),'response.body':json.dumps(A.data,cls=DetailEncoder)});set_attributes(B,C);gc.collect();sentry.flush();return A
def call_wrapper(wrapped,instance,args,kwargs):
	A='wsgi'
	with get_tracer(A).start_as_current_span(A,kind=SpanKind.SERVER)as B:C=build_attributes(A,{});set_attributes(B,C);WsgiSpanId.set(format_otel_span_id(B.get_span_context().span_id));ThreadIndex.reset();return wrapped(*args,**kwargs)
def sentry_flask_setup_wrapper(wrapped,instance,args,kwargs):unwrap(flask.Flask,_A);A=wrapped(*args,**kwargs);wrap_function_wrapper(flask.Flask,_A,call_wrapper);logger.info('rewrapped flask around sentry');return A
class DetailFlaskInstrumentor(FlaskInstrumentor):
	def _instrument(D,**A):
		super()._instrument(**A)
		class B(flask.Flask):
			def __init__(A,*B,**C):super().__init__(*B,**C);A.before_request(before_request);A.after_request(after_request)
		flask.Flask=B;wrap_function_wrapper(flask.Flask,_A,call_wrapper)
		try:from sentry_sdk.integrations.flask import FlaskIntegration as C
		except ImportError:pass
		else:logger.info('sentry detected; monkeypatching FlaskIntegration.setup_once');wrap_function_wrapper(C,'setup_once',sentry_flask_setup_wrapper)