from typing import Any,Callable
import forbiddenfruit
from opentelemetry.trace import SpanKind,Tracer
from wrapt.wrappers import _FunctionWrapperBase
from detail.client import stack
from detail.client.attrs import build_pure_attributes,is_active,set_attributes
from detail.client.disable import DisableDetail
from detail.client.logs import get_detail_logger,truncated_repr
from detail.client.models import Call
logger=get_detail_logger(__name__)
def get_pure_wrapper(tracer,library,empty_args=False,kind=SpanKind.INTERNAL):
	D=library
	def A(wrapped,instance,args,kwargs):
		C=kwargs;B=args;A=wrapped
		if DisableDetail.is_disabled():return A(*B,**C)
		E=stack.get_caller_path()
		if stack.is_ignored_caller(E):
			with DisableDetail():return A(*B,**C)
		H=f"{D}.{A.__qualname__}"
		with tracer.start_as_current_span(H,kind=kind)as G:
			F=A(*B,**C)
			if is_active(G):I=build_pure_attributes(D,A.__qualname__,B,C,F,E,empty_args=empty_args);set_attributes(G,I);logger.trace('%s: %s -> %s for %s',D,Call(A.__qualname__,B,C),truncated_repr(F),E)
			return F
	return A
class CopyableFunctionWrapperBase(_FunctionWrapperBase):
	def __copy__(A):return A
	def __deepcopy__(A,*B,**C):return A
def force_function_wrapper(target,name,wrapper,binding):C=binding;B=name;A=target;assert C in['function','classmethod','staticmethod'];D=getattr(A,B);E=A;F=getattr(A,'__dict__')[B];G=CopyableFunctionWrapperBase(D,E,wrapper,binding=C,parent=F);forbiddenfruit.curse(A,B,G)