import threading
from typing import Collection
from opentelemetry.trace import SpanKind,get_tracer
from wrapt import wrap_function_wrapper
from detail.client import stack
from detail.client.attrs import build_attributes,set_attributes
from detail.client.instrumentor import Instrumentor
def thread_start_wrapper(wrapped,instance,args,kwargs):A=instance;A.__dict__.update({'_detail_parent_thread_id':threading.get_ident(),'_detail_caller_path':stack.get_caller_path()});wrap_function_wrapper(A,'run',thread_run_wrapper);return wrapped(*args,**kwargs)
def thread_run_wrapper(wrapped,instance,args,kwargs):
	D=wrapped;C='thread';A=instance;B={A:B for(A,B)in A.__dict__.items()if A.startswith('_detail')}
	for G in B:del A.__dict__[G]
	B={A[len('_detail_'):]:B for(A,B)in B.items()};E=A._target or D;H=(E.__module__ or'')+f".{E.__qualname__}"
	with get_tracer(C).start_as_current_span(C,kind=SpanKind.CLIENT)as I:F={'name':A._name or'','target_name':H};F.update(B);J=build_attributes(C,F);set_attributes(I,J);return D(*args,**kwargs)
class ThreadInstrumentor(Instrumentor):
	def instrumentation_dependencies(A):return[]
	def _instrument(A,**B):wrap_function_wrapper(threading.Thread,'start',thread_start_wrapper)
	def _uninstrument(A,**B):0